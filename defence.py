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
        
    def get_action(obs, berzerker_x, berzerker_y):
        return Action.Slide
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][1] > player_y and
                abs(obs["ball"][0] - player_x) < 0.01):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.Bottom
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom_left(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] < player_x and
                obs["ball"][1] > player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.BottomLeft
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom_right(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] > player_x and
                obs["ball"][1] > player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.BottomRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_left(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] < player_x and
                abs(obs["ball"][1] - player_y) < 0.01):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.Left
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_right(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] > player_x and
                abs(obs["ball"][1] - player_y) < 0.01):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.Right
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][1] < player_y and
                abs(obs["ball"][0] - player_x) < 0.01):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.Top
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top_left(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] < player_x and
                obs["ball"][1] < player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.TopLeft
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top_right(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if (obs["ball"][0] > player_x and
                obs["ball"][1] < player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        return Action.TopRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}
