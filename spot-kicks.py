def corner(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.Corner:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if player_y > 0:
            if Action.TopRight not in obs["sticky_actions"]:
                return Action.TopRight
        else:
            if Action.BottomRight not in obs["sticky_actions"]:
                return Action.BottomRight
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def free_kick(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.FreeKick:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if player_x > 0.5:
            if player_y > 0:
                if Action.TopRight not in obs["sticky_actions"]:
                    return Action.TopRight
            else:
                if Action.BottomRight not in obs["sticky_actions"]:
                    return Action.BottomRight
            return Action.Shot
        else:
            if Action.Right not in obs["sticky_actions"]:
                return Action.Right
            return Action.HighPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def goal_kick(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.GoalKick:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if (random.random() < 0.5 and
                Action.TopRight not in obs["sticky_actions"] and
                Action.BottomRight not in obs["sticky_actions"]):
            return Action.TopRight
        else:
            if Action.BottomRight not in obs["sticky_actions"]:
                return Action.BottomRight
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def kick_off(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.KickOff:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if player_y > 0:
            if Action.Top not in obs["sticky_actions"]:
                return Action.Top
        else:
            if Action.Bottom not in obs["sticky_actions"]:
                return Action.Bottom
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def penalty(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.Penalty:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if (random.random() < 0.5 and
                Action.TopRight not in obs["sticky_actions"] and
                Action.BottomRight not in obs["sticky_actions"]):
            return Action.TopRight
        else:
            if Action.BottomRight not in obs["sticky_actions"]:
                return Action.BottomRight
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def throw_in(obs, player_x, player_y):
    def environment_fits(obs, player_x, player_y):
        if obs['game_mode'] == GameMode.ThrowIn:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        if Action.Right not in obs["sticky_actions"]:
            return Action.Right
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}
