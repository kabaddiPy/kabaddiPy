---
layout: default
title: get_player_rvd
parent: Player Functions
nav_order: 3
---
## `get_player_rvd(player_id, season=None)`

Retrieve Raider vs. Defender (RVD) data for a specific player in a given season.

### Parameters:
{: .no_toc }

- `player_id` (int): The unique identifier for the player.
- `season` (int, optional): The season number for which to retrieve data. If not specified, the latest season available will be used.

### Returns:
{: .no_toc }

A DataFrame containing RVD data for the specified player and season.

### Usage
{: .no_toc}

```python
rvd_df = pkl.get_player_rvd(player_id=142, season=None)
print(rvd_df)


      Season_Number      Team Name  player-id     Raider Name  Number of Defenders  Total Raids Percentage of Raids Empty Raids Percentage Successful Raids Percentage
              6  Puneri Paltan        142  Sandeep Narwal                    1            2                  2%                    NaN                     100.00%
              6  Puneri Paltan        142  Sandeep Narwal                    2            1               1.00%                100.00%                         NaN
              6  Puneri Paltan        142  Sandeep Narwal                    3            7               8.00%                 85.70%                         NaN
              6  Puneri Paltan        142  Sandeep Narwal                    4            9              10.00%                 66.70%                      11.10%
              6  Puneri Paltan        142  Sandeep Narwal                    5           12              14.00%                 91.70%                         NaN
              6  Puneri Paltan        142  Sandeep Narwal                    6           17              20.00%                 88.20%                      11.80%
              6  Puneri Paltan        142  Sandeep Narwal                    7           38              44.00%                 50.00%                      31.60%
              7        U Mumba        142  Sandeep Narwal                    2            3               4.00%                 33.30%                      33.30%
              7        U Mumba        142  Sandeep Narwal                    3            7              10.00%                 85.70%                      14.30%
              7        U Mumba        142  Sandeep Narwal                    4            7              10.00%                 85.70%                         NaN
              7        U Mumba        142  Sandeep Narwal                    5            6               9.00%                100.00%                         NaN
              7        U Mumba        142  Sandeep Narwal                    6           19              28.00%                 47.40%                      31.60%
              7        U Mumba        142  Sandeep Narwal                    7           25              37.00%                 48.00%                      32.00%
              8   Dabang Delhi        142  Sandeep Narwal                    1            1                  1%                    NaN                     100.00%
              8   Dabang Delhi        142  Sandeep Narwal                    2            5               7.00%                 40.00%                      20.00%
              8   Dabang Delhi        142  Sandeep Narwal                    3            5               7.00%                 60.00%                      40.00%
              8   Dabang Delhi        142  Sandeep Narwal                    4            9              13.00%                 55.60%                      22.20%
              8   Dabang Delhi        142  Sandeep Narwal                    5            9              13.00%                100.00%                         NaN
              8   Dabang Delhi        142  Sandeep Narwal                    6            8              12.00%                 50.00%                      50.00%
              8   Dabang Delhi        142  Sandeep Narwal                    7           31              46.00%                 58.10%                      25.80%
              9      UP Yoddha        142  Sandeep Narwal                    2            1               3.00%                100.00%                         NaN
              9      UP Yoddha        142  Sandeep Narwal                    3            5              13.00%                 80.00%                      20.00%
              9      UP Yoddha        142  Sandeep Narwal                    4            1               3.00%                100.00%                         NaN
              9      UP Yoddha        142  Sandeep Narwal                    5            8              21.00%                 50.00%                      37.50%
              9      UP Yoddha        142  Sandeep Narwal                    6            6              16.00%                 66.70%                         NaN
              9      UP Yoddha        142  Sandeep Narwal                    7           17              45.00%                 58.80%                      23.50%
              5  Puneri Paltan        142  Sandeep Narwal                    1            1                  1%                    NaN                     100.00%
              5  Puneri Paltan        142  Sandeep Narwal                    2           16              14.00%                 31.30%                      62.50%
              5  Puneri Paltan        142  Sandeep Narwal                    3           29              25.00%                 65.50%                      27.60%
              5  Puneri Paltan        142  Sandeep Narwal                    4           15              13.00%                 80.00%                       6.70%
              5  Puneri Paltan        142  Sandeep Narwal                    5           13              11.00%                 92.30%                         NaN
              5  Puneri Paltan        142  Sandeep Narwal                    6           17              15.00%                 64.70%                      29.40%
              5  Puneri Paltan        142  Sandeep Narwal                    7           26              22.00%                 76.90%                      19.20%
```

---

#### Notes:
{: .no_toc }

- The function retrieves the RVD data from a CSV file and processes it to extract relevant RVD information.
- If the player_id is not found in the data, the function will print a message and return `None`.
