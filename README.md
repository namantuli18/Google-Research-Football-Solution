# Google-Research-Football-Solution

## Results
| Final Score | Final Rank | 
|----------|----------|
| 1192.4 | 44/1139 |

## Problem Statement  
The submissions from participants get a chance to compete against other competitors for an 11v11 contest. The submissions are also ranked by the metric `Skill Rating`.

## Evaluation Metric  
Submissions were evaluated based on their performance against other competitors on the Leaderboard.  
Additionally, each Submission has an estimated Skill Rating which is modeled by a `Gaussian N(μ,σ2)` where μ is the estimated skill and σ represents our uncertainty of that estimate which will decrease over time.

## Methodology

#### 
1. The approach involves modifying the current environment in the agent function and using memory patterns, which evaluate constraints on obs, player_x, and player_y, to select actions based on whether the environment fits the patterns.
2. We have used a function `get_action_of_agent` to get an appropriate action from the dictionary of memory patterns. The `get_action` field of the object returns the response for the pair of players (player_x,player_y).
  ```python
    def get_action_of_agent(obs, player_x, player_y):
        memory_patterns = find_patterns(obs, player_x, player_y)
        for get_pattern in memory_patterns:
            pattern = get_pattern(obs, player_x, player_y)
            if pattern["environment_fits"](obs, player_x, player_y):
                return pattern["get_action"](obs, player_x, player_y)
  ```
3. For both groups of memory patterns and individual memory patterns, they all share the same input arguments: obs, player_x, and player_y. They also return dictionaries containing at least two functions.
4. The first function within this dictionary for both groups of memory patterns and individual memory patterns is called environment_fits. This function evaluates specific conditions based on the current environment and returns either True or False.
   * If it returns `True`, the respective group of memory patterns or memory pattern is chosen for further processing.
   * If it returns `False`, the search for an appropriate group or pattern continues.
5. All the utility functions described, share the 3 common arguments i.e. `obs`, `player_x` and `player_y`.


