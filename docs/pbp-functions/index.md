---
title: PlayByPlay_Data
layout: default
has_toc: true
has_children: true
nav_order: 5
---

#### Table of contents

{: .no_toc .text-delta }

1. TOC
{:toc}


### `load_match_details(season, match_id)`

Loads and processes detailed match information, including events, team performance, and zone breakdowns, returning six DataFrames with match metadata and statistics.

---

### `load_pbp(season, match_id)`

Retrieves the play-by-play (PBP) event data for a given match, detailing every event such as raids, tackles, and scores in a structured DataFrame.
