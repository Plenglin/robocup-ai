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


def assign_robot_positions(from_pos, to_pos, optimize_iterations=10):
    """
    The robots start at from_pos and end at to_pos. Returns a list of pairs (from_index, to_index, dist)
    that optimizes for total distance travelled by all robots.
    """
    outputs = [(i, i, dist(from_pos[i], to_pos[i]))
               for i, _ in enumerate(from_pos)]
    for _ in range(optimize_iterations):
        f, t = pick_2_indices(len(outputs))
        fa, ta, da = outputs[f]
        fb, tb, db = outputs[t]

        # Swapped items
        sda = dist(from_pos[fa], to_pos[tb])
        sdb = dist(from_pos[fb], to_pos[ta])

        # If swapping the assignments is more optimal, then do it
        if sda + sdb < da + db:
            outputs[f] = fa, tb, sda
            outputs[t] = fb, ta, sdb
    return outputs


def get_wall_positions(ball_pos, goal_pos, spacing, robot_count):
    """
    Returns a list of positions to move the robots to.
    """
    delta = goal_pos - ball_pos
    delta_perp = np.array(delta[-1], delta[0], dtype=np.float)
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
    assignments = assign_robot_positions(p_from, p_to, 20)
    for f, t, dist in assignments:
        print(f, t, dist)
        out = np.array([p_from[f], p_to[t]]).T
        line = Line2D(*out)
        ax.add_line(line)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.show()
    