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


## Sample Attack
The below video exhibits our counter-attacking approach, when competing against a team on the leaderboard.  

![Game Process](https://github.com/namantuli18/Google-Research-Football-Solution/blob/main/media/counter.gif)


## Methodology

### Overview
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

### Attacking 
1. For the attacking-based actions like short pass, long pass, shot from close range, shot from distance, and dribbling, we have created a separate utility file `attack.py`.
2. All the functional utilities have distance (coordinate) and probabilistic thresholds for the actions.
3. Based on how pragmatic or possessional a style of football needs to be played, these thresholds can be tuned.
4. For instance, we tuned the following function based on coordinates for a player to take a shot when outside the 30-yard circle: 
```python
#Utility function for a shot taken from distance
def far_from_goal_shot(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if player_x < -0.6 or obs["ball_owned_player"] == 0:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if Action.Sprint in obs["sticky_actions"]:
            return Action.ReleaseSprint
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}
```

### Defence
1. Like attack, all the defensive functions were organized in the file `defence.py`.
2. For defence, the distance to the closest opponent player is important in order to execute an action like a `sliding tackle` or a `standing tackle`.
3. Although the `sliding tackle` seems super effective when closing down an opponent, it has the chance of giving a penalty kick away.
4. Based on the closing down distance and the future distance (when the tackle is being performed), we have a function that returns a `bool` value that tells whether a tackle will be executed or not.
```python
def khorne_slide(obs, berzerker_x, berzerker_y):
    def environment_fits(obs, berzerker_x, berzerker_y):
        if obs["ball_owned_team"] == 1:
            prey_x = obs["right_team"][obs["ball_owned_player"]][0]
            prey_y = obs["right_team"][obs["ball_owned_player"]][1]
            players_amount = 0
            for i in range(1, len(obs["left_team"])):
                if obs["left_team"][i][0] < prey_x:
                    players_amount += 1
            prey_x_direction = obs["right_team_direction"][obs["ball_owned_player"]][0]
            future_prey_x = prey_x + obs["right_team_direction"][obs["ball_owned_player"]][0]
            future_prey_y = prey_y + obs["right_team_direction"][obs["ball_owned_player"]][1]
            future_berzerker_x = berzerker_x + obs["left_team_direction"][obs["active"]][0]
            future_berzerker_y = berzerker_y + obs["left_team_direction"][obs["active"]][1]
            distance_to_prey = get_distance(berzerker_x, berzerker_y, prey_x, prey_y)
            future_distance_to_prey = get_distance(future_berzerker_x, future_berzerker_y, future_prey_x, future_prey_y)
            if ((berzerker_x > -0.65 or abs(berzerker_y) > 0.3) and
                    players_amount <= 7 and
                    future_distance_to_prey < 0.015 and
                    distance_to_prey > future_distance_to_prey):
                return True
        return False
```

### Spot Kicks
1. All the spot kick utilities are present in the file `spot-kicks.py`.
2. Although rare, penalty kicks and free kicks present an opportunity to take a lead on the opposition.
3. Additional actions like `throw ins`, `kick-offs` and `goal kicks` are also taken care of.
4. For `penalties`, instead of focusing on the extreme corners, our approach randomly predicts the coordinates to shoot the ball.
```python
def penalty(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.Penalty:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if (random.random() < 0.5 and Action.TopRight not in obs["sticky_actions"] and Action.BottomRight not in obs["sticky_actions"]):
            return Action.TopRight
        else:
            if Action.BottomRight not in obs["sticky_actions"]:
                return Action.BottomRight
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}
```


## Key Takeaways
1. Contrary to a reinforcement-learning-based approach, a functional approach can devise a more pragmatic and rigid approach.
2. The efficacy of this approach depends on the opponent one is facing.
3. When the opponent agent focused on a more possessional style of play, this approach restrained pressure and prevented them from outscoring.
4. Even against some highly ranked opponents (Top 10), our methodology was highly successful as we prevented the opponent from outscoring.

## Full Replay
This game shows how the team soaked pressure and prevented the opponent from scoring.
[![Watch the video](https://github.com/namantuli18/Google-Research-Football-Solution/blob/main/media/sample-match.png)](https://youtu.be/d9uF8aDyRYc)



