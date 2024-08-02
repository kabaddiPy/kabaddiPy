---
title: Team Functions
layout: default
has_toc: false
has_children: true
---

---

## get_all_team_names

Retrieves the names of all teams in the Pro Kabaddi League.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_names = aggregator.get_all_team_names()
```

### Returns

- `List[str]`: A list of team names.

---

## get_all_team_url

Retrieves the URLs for all team pages on the Pro Kabaddi website.

### Usage

```python
aggregator = KabaddiDataAggregator()
team_urls = aggregator.get_all_team_url()
```

### Returns

- `List[str]`: A list of URLs for team pages.