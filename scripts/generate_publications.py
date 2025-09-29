import dateparser
import os
import requests
from collections import defaultdict
from datetime import datetime, timezone

# Constants for Zotero API
GROUP_ID = "5816477"
COLLECTION_KEYS = ["CVB532F5", "DKDV3KN4"]
API_URL_TEMPLATE = f"https://api.zotero.org/groups/{GROUP_ID}/collections/{{}}/items"
HEADERS = {"Accept": "application/json"}

OUTPUT_FILE = "publications.md"

def remove_duplicate_items(items):
    """
    Remove duplicates based on DOI.
    Items without a DOI are always included as unique.
    """
    seen_dois = set()
    unique_items = []

    for item in items:
        doi = item.get("data", {}).get("DOI")
        if doi:
            if doi not in seen_dois:
                seen_dois.add(doi)
                unique_items.append(item)
        else:
            unique_items.append(item)

    return unique_items

def fetch_all_items():
    items = []

    for collection_key in COLLECTION_KEYS:
        start = 0
        limit = 100
        while True:
            response = requests.get(
                API_URL_TEMPLATE.format(collection_key),
                headers=HEADERS,
                params={"format": "json", "limit": limit, "start": start}
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch Zotero items for collection {collection_key}: {response.status_code}")

            page_items = response.json()
            if not page_items:
                break

            items.extend(page_items)
            start += len(page_items)

    return remove_duplicate_items(items)

def format_authors(creators):
    authors = [f"{c['lastName']}, {c['firstName'][0]}." for c in creators if c.get("creatorType") == "author" and c.get("lastName")]
    if not authors:
        authors = [f"{c['lastName']}, {c['firstName'][0]}." for c in creators if c.get("creatorType") == "editor" and c.get("lastName")]
    return ", ".join(authors)

def extract_year(data):
    """
    Extracts the year from a Zotero 'date' field.
    Returns 'Unknown' if the date is missing or cannot be parsed.
    """
    date_str = data.get("date")
    if not date_str:
        return "Unknown"
    
    parsed_date = dateparser.parse(
        date_str,
        settings = {
            'PREFER_DAY_OF_MONTH': 'first',
            'RELATIVE_BASE': datetime(1900, 1, 1, tzinfo=timezone.utc), 
            'TIMEZONE': 'UTC',  
            'TO_TIMEZONE': 'UTC'
        }
    )
    return str(parsed_date.year) if parsed_date else "Unknown"

def extract_metadata(item):
    data = item.get("data", {})
    creators = data.get("creators", [])
    authors = format_authors(creators)
    title = data.get("title", "Untitled")
    publication = data.get("publicationTitle", data.get("journalAbbreviation", ""))
    year = extract_year(data)
    doi = data.get("DOI", None)
    url = f"https://doi.org/{doi}" if doi else data.get("url", "")
    if year == 'Unknown':
        print(item)
    return year, f'{authors}, [{title}]({url}), {publication}, {year}'

def generate_md(grouped_by_year):
    lines = []
    for year in sorted(grouped_by_year.keys(), reverse=True):
        n_pub = len(grouped_by_year[year])
        lines.append(f'\n### {year} ({n_pub} publication{"s" if n_pub != 1 else ""})\n')
        for entry in sorted(grouped_by_year[year]):
            lines.append(f' * {entry}')
    return "\n".join(lines)

def header(total_pub):
    return f'''---\nlayout: page\ntitle: Publications\n---\n
If you plan to submit publications using Med-CORDEX simulations, please refer it with a simple sentence in the Acknowledgment: _"This work is part of the Med-CORDEX initiative (www.medcordex.eu)"_ or _"The simulations used in this work were downloaded from the Med-CORDEX database (www.medcordex.eu)"_.\n\nWe strongly encourage people downloading data from the Med-CORDEX database to contact the model data producers in order to give feedback on the model simulations, interact on the scientific studies and/or propose co-authorships.

{{% include toc %}}

## Publications based on Med-CORDEX simulations (total: {total_pub})
'''

def main():
    items = fetch_all_items()
    publications_by_year = defaultdict(list)

    for item in items:
        try:
            year, entry = extract_metadata(item)
            publications_by_year[year].append(entry)
        except Exception as e:
            print(f"Skipping item due to error: {e}")

    md = header(total_pub = len(items)) + generate_md(publications_by_year)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Generated {OUTPUT_FILE} with {sum(len(v) for v in publications_by_year.values())} publications.")

main()