import sys
import os
import numpy as np
dirname = os.path.dirname(__file__)
sys.path.insert(0, dirname)
from state_machine import state
import random

dirname = os.path.dirname(__file__)
sys.path.insert(0, dirname)
from strategy_numbers import *

sys.path.insert(0, dirname+'/..')
from basic_skills.source.cover import cover
from basic_skills.source.helper_functions import get_closest, mag
from util import assign_robot_positions

class wall_strategy(state):
    # assigns actions to robots when the enemy has the ball  
    state_number = 1
    def __init__(self, id, team):
        state.__init__(self, id)
        self.team = team
        self.assigments = None

    def setup(self):
        print("wall", "blue" if self.team.is_blue else "yellow")
        positions = get_wall_positions(self.team.field_players)
        ball_pos = self.team.game.ball.loc
        #self.assignments = assign_robot_positions(get_wall_positions)

    def update(self):
        # state machine transition 
        if self.team.ball_controler is not None and self.team.ball_controler.is_blue == self.team.is_blue:
            return OFFENSIVE_STRATEGY_STATE_NUMBER
            
        elif self.team.ball_controler is None:
            return NEUTRAL_STRATEGY_STATE_NUMBER
            
        return DEFENSIVE_STRATEGY_STATE_NUMBER
