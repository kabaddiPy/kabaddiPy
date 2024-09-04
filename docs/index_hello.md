# Prokabaddi API

This documentation covers the main functions of the `KabaddiDataAggregator` class that return useful data for Kabaddi statistics and information.

**Note**: This documentation is actively being developed alongwith the API.

## Table of Contents

- [Prokabaddi API](#prokabaddi-api)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [load\_data](#load_data)
    - [Usage](#usage)
    - [Parameters](#parameters)
    - [Returns](#returns)

---

## Installation 
Use the following command to install.

```shell
pip install pro_kabaddi_data
```

---
## load_data

Loads files into pandas DataFrames based on provided boolean parameters.

### Usage

```python
data_loader = KabaddiDataAggregator()
player_df, team_df, members_df = data_loader.load_data(TeamDetails=False, TeamMembers=False, PlayerDetails=True)
```
### Parameters
- `TeamDetails` (bool): Loads the details of every team. Default is `False`.
- `TeamMembers` (bool): Loads the members of all teams for the recent season. Default is `False`.
- `PlayerDetails` (bool): Loads all individual attributes of players. Default is `True`.

### Returns
- `tuple`: A tuple containing the loaded DataFrames in the order (player_details_df, team_details_df, team_members_df).

---