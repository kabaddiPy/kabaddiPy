---
title: Team Functions
layout: default
has_toc: true
has_children: true
---
# Team Functions

- [Table of Contents](#table-of-contents)
  - [get\_all\_team\_names](#get_all_team_names)
    - [Usage](#usage)
    - [Returns](#returns)
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