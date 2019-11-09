import numpy as np
import random


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
    delta_perp = np.array([-delta[1], delta[0]], dtype=np.float32)
    wall_center = ball_pos + delta / 2
    wall_step = delta_perp * spacing / np.linalg.norm(delta_perp)
    wall_len = spacing * (robot_count - 1)

    wall_start = wall_center - wall_step * wall_len / 2

    pos = wall_start
    return [wall_start + i * wall_step for i in range(robot_count)]


if __name__ == "__main__":
    """
    Test the line assignment
    """
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    fig = plt.figure()
    ax = plt.subplot(111)
    p_from = np.random.rand(6, 2)
    p_to = np.random.rand(6, 2)
    ax.scatter(*p_from.T)
    ax.scatter(*p_to.T)
    perm = assign_robot_positions(p_from, p_to, 20)
    for f, t in enumerate(perm):
        out = np.array([p_from[perm[f]], p_to[perm[t]]]).T
        line = Line2D(*out)
        ax.add_line(line)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.show()
    
