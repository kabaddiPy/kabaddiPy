<p align="center">
  <img src="docs/assets/kabaddi_api_logo.png" alt="Kabaddi Data Aggregator Logo" width="200"/>
</p>

<h1 align="center">Kabaddi Data Aggregator</h1>

<p align="center">
  <strong>Comprehensive data collection and analysis tools for professional Kabaddi leagues</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

Kabaddi Data Aggregator is a Python module that provides tools for collecting and analyzing data from professional Kabaddi leagues. It uses web scraping techniques to gather information about teams, players, and match statistics from various online sources.

## Features

- Retrieve team names and URLs
- Fetch player information and statistics
- Get current season standings
- Extract team line-up data
- Analyze team-level statistics
- Gather player performance data

## Installation

You can install the Kabaddi Data Aggregator using pip:

```
pip install kabaddi_data_aggregator
```

## Requirements

- Python 3.7+
- Selenium WebDriver
- Firefox browser (for Selenium WebDriver)

## Usage

Here's a quick example of how to use the Kabaddi Data Aggregator:

```python
from kabaddi_data_aggregator import KabaddiDataAggregator

# Initialize the aggregator
aggregator = KabaddiDataAggregator()

# Get all team names
team_names = aggregator.get_all_team_names()
print("Team Names:", team_names)

# Get current season standings
standings = aggregator.team_season_standings()
print("Season Standings:", standings)

# Get player information
players_info = aggregator.get_players_team_info_and_profile_url()
print("Players Info:", players_info[:5])  # Print first 5 players

# Get team line-up data
line_up_data = aggregator.team_line_up()
print("Team Line-up Data:", line_up_data)
```

For more detailed usage instructions and API documentation, please refer to our [documentation page](https://your-documentation-url.com).

## Contributing

We welcome contributions to the Kabaddi Data Aggregator project! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

Please make sure to update tests as appropriate and adhere to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Pro Kabaddi League for providing the data sources
- Selenium WebDriver for enabling web scraping capabilities
- All contributors who have helped to improve this project

## Contact

If you have any questions, feel free to reach out to [Aniruddha Mukherjee] at [mukh.aniruddha@gmail.com] or open an issue in the GitHub repository.

---

<p align="center">
  Made with ❤️ for Kabaddi enthusiasts and data analysts
</p>

Remember to star this repository if you find it helpful! Your support is greatly appreciated.
