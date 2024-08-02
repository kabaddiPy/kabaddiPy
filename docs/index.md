---
title: ProKabaddi API Docs
layout: default
has_toc: false
has_children: true
---


# Prokabaddi API

This documentation covers the main functions of the `KabaddiDataAggregator` class that return useful data for Kabaddi statistics and information.

**Note**: This documentation is actively being developed alongwith the API.

## Table of Contents

- [Prokabaddi API](#prokabaddi-api)
  - [Team Functions](team_docs/index.md)
  - [Player Functions](player_docs/index.md)
  - [Endpoints API](#endpoints-api)
  - [Planned functions]()
---

## Endpoints API
This is how you set up your endpoints.

---
## load_data

Loads files into pandas DataFrames based on provided boolean parameters.

### Usage

```python
data_loader = KabaddiDataAggregator()
player_df, team_df, members_df = data_loader.load_data(TeamDetails=True, TeamMembers=True, PlayerDetails=True)
```
### Parameters
- `TeamDetails` (bool): Loads the details of every team. Default is True.
- `TeamMembers` (bool): Loads the members of all teams for the recent season. Default is True.
- `PlayerDetails` (bool): Loads all individual attributes of players. Default is True.
---
### Returns
- `tuple`: A tuple containing the loaded DataFrames in the order (player_details_df, team_details_df, team_members_df).

---


