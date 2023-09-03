def bad_angle_short_pass(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if ((abs(player_y) > 0.15 and player_x > 0.85) or
                (player_x > 0.7 and player_y > 0.07 and obs["left_team_direction"][obs["active"]][1] > 0) or
                (player_x > 0.7 and player_y < -0.07 and obs["left_team_direction"][obs["active"]][1] < 0)):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if player_y > 0:
            if Action.Top not in obs["sticky_actions"]:
                return Action.Top
        else:
            if Action.Bottom not in obs["sticky_actions"]:
                return Action.Bottom
        if Action.Sprint in obs["sticky_actions"]:
            return Action.ReleaseSprint
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def close_to_goalkeeper_shot(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        goalkeeper_x = obs["right_team"][0][0] + obs["right_team_direction"][0][0] * 13
        goalkeeper_y = obs["right_team"][0][1] + obs["right_team_direction"][0][1] * 13
        if get_distance(player_x, player_y, goalkeeper_x, goalkeeper_y) < 0.3:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if player_y <= -0.03 or (player_y > 0 and player_y < 0.03):
            if Action.BottomRight not in obs["sticky_actions"]:
                return Action.BottomRight
        else:
            if Action.TopRight not in obs["sticky_actions"]:
                return Action.TopRight
        if Action.Sprint in obs["sticky_actions"]:
            return Action.ReleaseSprint
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def close_to_opponent_short_pass(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        for i in range(1, len(obs["right_team"])):
            distance_to_opponent = get_distance(player_x, player_y, obs["right_team"][i][0], obs["right_team"][i][1])
            if distance_to_opponent < 0.03:
                for j in range(1, len(obs["left_team"])):
                    distance_to_teammate = get_distance(player_x, player_y, obs["left_team"][j][0], obs["left_team"][j][1])
                    if distance_to_teammate < 0.2:
                        teammate_distance_to_goal = get_distance(obs["left_team"][j][0], obs["left_team"][j][1], 1, 0)
                        player_distance_to_goal = get_distance(player_x, player_y, 1, 0)
                        if teammate_distance_to_goal < player_distance_to_goal:
                            return True
                break
        return False
        
    def get_action(obs, player_x, player_y):
        if Action.Sprint in obs["sticky_actions"]:
            return Action.ReleaseSprint
        return Action.ShortPass

    return {"environment_fits": environment_fits, "get_action": get_action}

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

def far_from_goal_high_pass(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if player_x < -0.3 or obs["ball_owned_player"] == 0:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if Action.Right not in obs["sticky_actions"]:
            return Action.Right
        if Action.Sprint in obs["sticky_actions"]:
            return Action.ReleaseSprint
        return Action.HighPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def go_through_opponents(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        biggest_distance, final_opponents_amount = get_average_distance_to_opponents(obs, player_x + 0.01, player_y)
        obs["memory_patterns"]["go_around_opponent"] = Action.Right
        top_right, opponents_amount = get_average_distance_to_opponents(obs, player_x + 0.01, player_y - 0.01)
        if (top_right > biggest_distance and player_y > -0.15) or (top_right == 2 and player_y > 0.07):
            biggest_distance = top_right
            final_opponents_amount = opponents_amount
            obs["memory_patterns"]["go_around_opponent"] = Action.TopRight
        bottom_right, opponents_amount = get_average_distance_to_opponents(obs, player_x + 0.01, player_y + 0.01)
        if (bottom_right > biggest_distance and player_y < 0.15) or (bottom_right == 2 and player_y < -0.07):
            biggest_distance = bottom_right
            final_opponents_amount = opponents_amount
            obs["memory_patterns"]["go_around_opponent"] = Action.BottomRight
        if final_opponents_amount >= 3:
            obs["memory_patterns"]["go_around_opponent_surrounded"] = True
        else:
            obs["memory_patterns"]["go_around_opponent_surrounded"] = False
        return True
        
    def get_action(obs, player_x, player_y):
        if obs["memory_patterns"]["go_around_opponent_surrounded"]:
            return Action.HighPass
        if Action.Sprint not in obs["sticky_actions"]:
            return Action.Sprint
        return obs["memory_patterns"]["go_around_opponent"]
    
    return {"environment_fits": environment_fits, "get_action": get_action}