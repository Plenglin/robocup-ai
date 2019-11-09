import numpy as np
import random
import os
import sys
dirname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dirname+'/..')
from basic_skills.source.helper_functions import scale_to, rotate_vector
import math


def dist(a, b):
    delta = a - b
    return np.linalg.norm(delta)


def pick_2_indices(count):
    """
    Pick 2 integers in [0, count) without replacement.
    """
    i = random.randrange(count)
    j = random.randrange(count - 1)
    if j >= i:
        j += 1
    return i, j


def assign_robot_positions(from_pos, to_pos, optimize_iterations=10, perm=None):
    """
    The robots start at from_pos and end at to_pos. Returns a permutation list
    that optimizes for total distance travelled by all robots.
    """
    if perm is None:
        perm = list(range(len(from_pos)))
    for _ in range(optimize_iterations):
        f, t = pick_2_indices(len(perm))
        fa = from_pos[perm[f]]
        ta = to_pos[perm[f]]
        da = dist(fa, ta)
        fb = from_pos[perm[t]]
        tb = to_pos[perm[t]]
        db = dist(fb, tb)

        # Swapped items
        sda = dist(fa, tb)
        sdb = dist(fb, ta)

        # If swapping the assignments is more optimal, then do it
        if sda + sdb < da + db:
            perm[f], perm[t] = perm[t], perm[f]
    return perm


def get_wall_positions(ball_pos, goal_pos, spacing, robot_count):
    """
    Returns a list of positions to move the robots to.
    """
    delta = goal_pos - ball_pos
    delta_norm = scale_to(delta, 1)
    delta_perp_norm = rotate_vector(delta_norm, np.pi / 2)
    wall_center = ball_pos + delta / 2
    wall_step = delta_perp_norm * spacing
    wall_len = spacing * (robot_count - 1)

    wall_start = wall_center - delta_perp_norm * wall_len / 2

    pos = wall_start
    return [wall_start + i * wall_step for i in range(robot_count)], [delta_norm, delta_perp_norm]


def assign_wall_positions(robot_pos, p_to, basis):
    """
    Returns a permutation OF THE ROBOTS, not the targets!
    """

    remapped = np.dot(np.linalg.inv(basis), robot_pos.T)
    sort_key = remapped[1]
    perm = np.argsort(sort_key)
    return perm


if __name__ == "__main__":
    """
    Test the line assignment
    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    fig = plt.figure()
    ax = plt.subplot(111)
    p_from = np.random.rand(6, 2)
    p_to, basis = get_wall_positions(np.array([0, 0.5], dtype=np.float32), np.array(
        [1, 0.5], dtype=np.float32), 0.1, 6)
    p_to = np.array(p_to, dtype=np.float32)
    print(p_from)
    for p in p_from:
        ax.scatter(*p)
    ax.scatter(*p_to.T, color='black')
    perm = assign_wall_positions(p_from, p_to, np.array(basis, dtype=np.float32).T)
    for tp, fi in zip(p_to, perm):
        out = np.array([tp, p_from[fi]]).T
        line = Line2D(*out)
        ax.add_line(line)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.show()
    
