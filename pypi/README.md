| <img width="200" alt="kabaddi_api_logo" src="https://github.com/user-attachments/assets/e074c4c2-18b3-4580-a9dd-1aa40f9495b0"> | <h2>kabaddiPy - Data collection and analysis tools for professional Kabaddi leagues</h3><p align="center"><a href="#features">Features</a> • <a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#contributing">Contributing</a> • <a href="#license">License</a> • <a href="https://kabaddipy.github.io/kabaddiPy/">Documentation</a></p> |
|:---:|:---|


[![License](https://img.shields.io/pypi/l/kabaddiPy.svg)](https://github.com/kabaddiPy/kabaddiPy/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/kabaddiPy.svg)](https://badge.fury.io/py/kabaddiPy)
[![Python Versions](https://img.shields.io/pypi/pyversions/kabaddiPy.svg)](https://pypi.org/project/kabaddiPy/)


---

`kabaddiPy` is a Python module that provides tools for collecting and analyzing data from professional Kabaddi leagues. It uses web scraping techniques to gather information about teams, players, and match statistics from various online sources.

## Installation 

Please install the development version of `kabaddiPy` using pip:


```shell
pip install kabaddiPy
```

Deployed here: https://pypi.org/project/kabaddiPy/


## Quick Function Overview


<div align=center">
<img width="800" alt="Function Overview" src="https://github.com/user-attachments/assets/b1ceed1a-48d9-409c-8f6b-b188eaaf9733" >
</div>


## Usage

Here's a quick minimal example of how to get started with the `kabaddiPy` package:


```python
import kabaddiPy

pkl = PKL()

# Get roster for a specific team for a specific season
team_roster = pkl.build_team_roster(team_id=3, season=1)
print(team_roster)

```

For more detailed usage instructions and API documentation, please refer to our [documentation page](https://kabaddipy.github.io/kabaddiPy/).

For more complicated examples, check out the [examples](https://github.com/kabaddiPy/kabaddiPy/tree/main/examples) directory.


## Features

KabaddiPy offers a comprehensive set of features for analyzing Pro Kabaddi League (PKL) data. Here are some of the key functionalities:

### Season Standings

```python
standings = pkl.get_standings(season=9, qualified=True)
```
Retrieve PKL standings for a specific season, with options to filter for qualified teams.

### Match Data

```python
season_matches = pkl.get_season_matches(season=6)
```
Get detailed information about all matches in a specific season.

### Team Information

```python
team_rank, team_value, team_per_match, team_raider_skills, team_defender_skills = pkl.get_team_info(season=6, team_id=29)
```
Access comprehensive team statistics, including rankings, absolute values for statistics, and per-match metrics. Additionally get a summary of the various Raider/Defender Skills employed throught the season by the team.

### Player Information

```python
player_stats_rank, player_stats_value, player_stats_per_match = pkl.get_player_info(player_id=660, season=9)
```
Retrieve detailed player statistics, including rankings, performance metrics, and Raider vs. Defender (RVD) data.

### Match Details

```python
match_detail_df, events_df, zones_df, team1_df, team2_df, breakdown_df = pkl.load_match_details(season=9, match_id='2895')
```
Access comprehensive match data, including events, team performances, and breakdown statistics.

### Play-by-Play Data

```python
pbp_events_data = pkl.load_pbp(season=9, match_id='2895')
```
Get detailed play-by-play data for specific matches.

### Team Roster

```python
team_roster_df = pkl.get_team_roster(season=9, team_id=3)
```
Generate a comprehensive roster for a specific team in a given season.

### Visualization Tools

```python
pkl.plot_player_zones(player_id=143, season=5, zone_type='strong')
pkl.plot_team_zones(team_id=4, season=5, zone_type='weak')
pkl.plot_point_progression(season=10, match_id=3163)
```
Create visual representations of player and team performance, including zone analysis and point progression charts.

### Multi-Player Comparison

```python
pkl.plot_player_zones_grid([143, 12, 211, 160], season=5, zone_type='strong', max_cols=2)
```
Generate grid visualizations for comparing multiple players' performances.


These features provide a robust toolkit for analyzing PKL data, from high-level season statistics to detailed player and match analyses. 

The package offers both data retrieval and visualization capabilities, making it a versatile resource for kabaddi enthusiasts, analysts, and researchers.



## Contributing

We welcome contributions to the Kabaddi Data Aggregator project! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request


## License

This project is licensed under the GPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the various website owners for providing the data source
  

## Contact

If you have any questions, feel free to reach out to [Aniruddha Mukherjee](mailto:mukh.aniruddha@gmail.com) or [Bhaskar Lalwani](mailto:bhaskarlalwani2040@gmail.com) or open an issue in the GitHub repository.

---

<p align="center">
  Made with ❤️ for Kabaddi enthusiasts and data analysts

  Please ⭐️ this repository if you found it helpful! Your support is greatly appreciated. :)
</p>


