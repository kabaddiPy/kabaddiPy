---
layout: default
title: get_team_roster
parent: Team Functions
nav_order: 4
---
### `get_team_roster`

Gets the team roster for a specific team in a given season.


#### Parameters
{: .no_toc }
- **team_id**: `int`  
  The unique identifier for the team.

- **season**: `int`  
  The season number for which to build the roster.

#### Returns
{: .no_toc }

A `DataFrame` containing the team roster for the specified season. 

#### Usage
{: .no_toc }
```python
team_roster = pkl.get_team_roster(team_id=7,season=10)
print(team_roster)
Player ID	Name	                 Jersey  Captain Count	Played Count	Green Card Count	Yellow Card Count
0	3233	Pankaj Mohite	         12	    0	        22	1	0
1	4031	Nitin R	                 55	    0	        4	0	0
2	5116	Aditya Shinde	         11	    0	        12	0	0
3	5108	Badal Singh	         32	    0	        7	0	0
4	5151	Dadaso Pujari	         7	    0	        5	1	0
5	5152	Tushar Dattaray Adhavade 18	    0	        6	0	0
6	5256	Vahid RezaEimehr	 6	    0	        5	0	0
7	4960	Aslam Mustafa Inamdar	 3	    21	        23	3	0
8	4192	Abinesh Nadarajan        4	    0	        24	1	0
9	3234	Sanket Sawant	         10	    0	        22	4	1
10	4022	Mohit Goyat	         88	    0	        22	1	0
11	4959	Akash Shinde	         33	    0	        13	0	0
12	5128	Gaurav Khatri	         20	    0	        24	3	0
13	4925	Mohammadreza Chiyaneh	 8	    3	        24	2	0
14	5150	Vaibhav Kamble	         5	    0	        2	0	0
15	5194	Hardeep	                 77	    0	        0	0	0
16	5165	Ishwar	                 9	    0	        1	0	0
17	5193	Ahmed Enamdar	         99	    0	        1	0	0
```
#### Notes
{: .no_toc }

- The function reads match data from JSON files in the `./MatchData_pbp` directory.
- If no data is found for the specified season, an empty `DataFrame` is returned.
- The function aggregates data across all matches, updating player statistics cumulatively.
