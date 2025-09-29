---
layout: page
title: Workshops
permalink: /workshops.html
---

Below is a list of Med-CORDEX workshops. Click on a workshop title to view more details.

<ul class="workshop-list">
{% assign sorted_workshops = site.workshops | sort: 'date' | reverse %}
{% for workshop in sorted_workshops %}
  {% assign start_day = workshop.date | date: "%d" %}
  {% assign end_day = workshop.date_end | date: "%d" %}
  {% assign month = workshop.date | date: "%b" %}
  {% assign year = workshop.date | date: "%Y" %}
  <li>
    <a href="{{ workshop.url }}">{{ workshop.title }}</a>,
    {% if workshop.date_end %}
      {{ start_day }}-{{ end_day }} {{ month }} {{ year }}
    {% else %}
      {{ start_day }} {{ month }} {{ year }}
    {% endif %}
    {% if workshop.location %} ({{ workshop.location }}){% endif %}
  </li>
{% endfor %}
</ul>
