| <img width="200" alt="kabaddi_api_logo" src="https://github.com/user-attachments/assets/e074c4c2-18b3-4580-a9dd-1aa40f9495b0"> | <h2> KabaddiPy - Data collection and analysis tools for professional Kabaddi leagues</h3><p align="center"><a href="#features">Features</a> • <a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#contributing">Contributing</a> • <a href="#license">License</a> • <a href="https://annimukherjee.github.io/ProKabaddi_API/">Documentation</a></p> |
|:---:|:---|

---

Kabaddi Data Aggregator is a Python module that provides tools for collecting and analyzing data from professional Kabaddi leagues. It uses web scraping techniques to gather information about teams, players, and match statistics from various online sources.

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

Here's a quick minimal example of how to get started with the Kabaddi Data Aggregator:

```python
import kabaddiPy


# Get all player information for a specific team
players_info = api.get_team_matches(7, 4)
```

For more detailed usage instructions and API documentation, please refer to our [documentation page](https://github.com/kabaddiPy/kabaddiPy).

## Features
Here are our current features. New and better features are actively being developed!!



### Current season standings

```python
standings = aggregator.team_season_standings(team=None, rank=None)
```
Return the current season rankings of all teams by default
#### **Parameters**
- team (str, optional): Get season rank by team name
- rank (int, optional): Get team by season rank

### Player Performance
```python
stats = aggregator.player_performance("team="Bengal Warriors")
```
Returns career level player metrics. `team` should be specified.

### Loading Lifetime Data

```python
player_df = aggregator.load_data(PlayerDetails=True, TeamDetails = False, TeamMembers = False)
```
Defaults to loading lifetime player data for all teams.
#### **Parameters**
- PlayerDetails (bool): Loads player details into a DataFrame. Default is `True`.
- TeamDetails (bool): Loads team-level statistics into a DataFrame. Default is `False`.
- TeamMembers (bool): Loads the details of current team members into a DataFrame. Default is `False`.

### Team level stats
```python
teamstats = aggregator.team_level_stats(season=None)
```
Returns team-level stats by season. Defaults to latest season.



## Contributing

We welcome contributions to the Kabaddi Data Aggregator project! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/<your-feature-name>`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/<your-feature-name>`)
6. Create a new Pull Request


## License

This project is licensed under the GPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the various website owners for providing the data sources

## Contact

If you have any questions, feel free to reach out to [Aniruddha Mukherjee](mailto:mukh.aniruddha@gmail.com) or [Bhaskar Lalwani](mailto:bhaskarlalwani2040@gmail.com) or open an issue in the GitHub repository.

---

<p align="center">
  Made with ❤️ for Kabaddi enthusiasts and data analysts

  Please ⭐️ this repository if you found it helpful! Your support is greatly appreciated. :)
</p>

