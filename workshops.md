---
layout: page
title: Workshops
permalink: /workshops.html
---

Below is a list of Med-CORDEX workshops. Click on a workshop title to view more details.

{% for workshop in site.workshops %}
  {% assign start_day = workshop.date | date: "%d" %}
  {% assign end_day = workshop.date_end | date: "%d" %}
  {% assign month = workshop.date | date: "%b" %}
  {% assign year = workshop.date | date: "%Y" %}
- [{{ workshop.title }}]({{ workshop.url }}), {% if workshop.date and workshop.date_end %}{{ start_day }}-{{ end_day }} {{ month }} {{ year }}{% elsif workshop.date %}{{ start_day }}-{{ end_day }} {{ month }} {{ year }}{% endif %}{% if workshop.location %} ({{ workshop.location }}){% endif %}
{% endfor %}
