import numpy as np
import math
import sys
import os
dirname = os.path.dirname(__file__)
sys.path.insert(0, dirname)
from action import *
from move_to import *
from orbit_ball import *
from helper_functions import *

#Attempts to gain control of the ball
class intercept_ball(action):
  def __init__(self, iterations = 3):
    action.__init__(self)
    self.pid = move_to()
    self.robot = False
    self.target_loc = False
    
    #number of iterations to refine result
    self.iterations = iterations
    
    #used to calculate time to point this should be abstracted into a helper_function call
    self.robot_actual_speed = 600
    
    #should inherit from global
    self.robot_radius = 90
    self.ball_radius = 25
    
    #orbit action used for part of the interception process
    self.orbit = orbit_ball()
  def add(self, robot, game):
    self.robot = robot
    self.pid.robot = robot
    
    self.orbit.add(robot, game)
    action.add(self, robot, game)
  def run(self):
    '''
    Start with the closest point that would put you in the path of the ball and refine based on projected positions
    '''
  
    ball = self.game.ball
    ball_speed = np.linalg.norm(ball.velocity)
    robot = self.robot
    if ball_speed < 20:
      #if the ball is moving slowly just move to it
      target_loc = ball.loc
    else:
    
      #set the target loc to be the closest point that would lie on the ball's path
      target_loc = drop_perpendicular(self.robot.loc, ball.loc, ball.velocity)
      
      ball_loc = ball.loc + ball.velocity
      off_by = np.linalg.norm(ball_loc - target_loc)
      old_distance = np.linalg.norm(ball.loc - target_loc)
      
      # If the ball is moving away from us orbit around it until we are in front
      # this is so that we don't hit the ball on transit
      if off_by > old_distance:
        self.orbit.target_loc = ball.loc - ball.velocity
        return(self.orbit.run())
        
      #Otherwise, Iteratively refine our target_loc
      for i in range(self.iterations):
        travel_time = time_to_point(robot, target_loc, self.robot_actual_speed)
        ball_loc = ball.loc + ball.velocity * travel_time
        off_by = np.linalg.norm(ball_loc - target_loc)
        ball_vel_normalized = ball.velocity/ball_speed
        
        #if ball passed target_loc
        if (off_by + travel_time*ball_speed > old_distance):
          if self.robot_actual_speed - ball_speed > 0:
            #if the ball will have gone past you run back to catch it
            shortening_rate = self.robot_actual_speed - ball_speed
            target_loc = target_loc + off_by/shortening_rate*ball_vel_normalized
          else:
            #if we can't run down the ball just do your best
            target_loc = ball_loc
        else:
          #if ball hasn't reached target move target_point forward to meet it
          shortening_rate = self.robot_actual_speed + ball_speed
          target_loc = target_loc - off_by/shortening_rate*ball_vel_normalized*self.robot_actual_speed
          
    #move up to the ball not on top of the ball
    hold_offset = self.robot.loc - ball.loc
    if np.linalg.norm(hold_offset) > .1:
      hold_offset = hold_offset / np.linalg.norm(hold_offset)
      #print(self.robot_radius + self.ball_radius - ball_speed/100, self.game.ball.controler)
      offset = self.robot_radius + self.ball_radius
      if not self.game.ball.controler:
        offset -= ball_speed/5
      hold_offset = hold_offset * offset
      target_loc = target_loc + hold_offset + ball.velocity * 0.2
      
    #use move_to to do move to target loc and look at the ball
    point_dir = robot.loc - ball.loc
    target_rot = -normalize_angle(math.pi + math.atan2(point_dir[1], point_dir[0]))
    self.pid.set_target(target_loc, target_rot)
    actions = self.pid.run()
    self.actions = actions
    self.target_loc = target_loc
    return actions

    
#simple test case
if __name__ == "__main__":
  max_bots_per_team = 6
  game = Ball_Intercept_PYGym(max_bots_per_team)
  intercept_action = intercept_ball()
  clock = pygame.time.Clock()
  clock.tick(60)
  ttime = clock.tick()
  game.add_action(intercept_action, 0, False)
  
  while 1:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    new_time = clock.tick()
    game.step()
    ttime = new_time


