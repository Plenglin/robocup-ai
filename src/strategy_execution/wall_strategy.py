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
from basic_skills.source.MoveTo import MoveTo
from util import assign_robot_positions, get_wall_positions

class wall_strategy(state):
    # assigns actions to robots when the enemy has the ball  
    state_number = 1
    def __init__(self, id, team):
        state.__init__(self, id)
        self.team = team
        self.perm = list(range(len(team.field_players)))
        self.positions = [r.loc for r in self.team.field_players]
        self.move_tos = [MoveTo(p) for p in self.positions]
        for i, mt in enumerate(self.move_tos):
            self.team.game.add_action(mt, i, self.team.is_blue)

    def setup(self):
        print("wall", "blue" if self.team.is_blue else "yellow")

    def assign_robot_positions(self):
        ball_pos = self.team.game.ball.loc
        goal_pos = self.team.my_goal
        wall_pos = get_wall_positions(ball_pos, goal_pos, 500, len(self.team.field_players))
        robot_pos = [r.loc for r in self.team.field_players]
        self.perm = assign_robot_positions(robot_pos, wall_pos, 10, self.perm)

    def update(self):
        self.assign_robot_positions()
        for p, mt in zip(self.perm, self.move_tos):
            mt.target_loc = self.positions[p]

        # state machine transition 
        if self.team.ball_controler is not None and self.team.ball_controler.is_blue == self.team.is_blue:
            return OFFENSIVE_STRATEGY_STATE_NUMBER
            
        elif self.team.ball_controler is None:
            return NEUTRAL_STRATEGY_STATE_NUMBER
            
        return DEFENSIVE_STRATEGY_STATE_NUMBER

