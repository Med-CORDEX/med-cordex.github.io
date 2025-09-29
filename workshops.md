---
layout: page
title: Workshops
permalink: /workshops.html
---

# Med-CORDEX Workshops

Below is a list of Med-CORDEX workshops. Click on a workshop title to view more details.

{% for workshop in site.workshops %}
- [{{ workshop.title }}]({{ workshop.url }})
  {%- if workshop.date and workshop.date_end -%}
    - {{ workshop.date | date: "%B %d, %Y" }} – {{ workshop.date_end | date: "%B %d, %Y" }}
  {%- elsif workshop.date -%}
    - {{ workshop.date | date: "%B %d, %Y" }}
  {%- endif -%}
  {%- if workshop.location %} ({{ workshop.location }}){% endif %}
{% endfor %}
