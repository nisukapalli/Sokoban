##############
# Homework 3 #
##############

import astar
import numpy as np


# a_star performs the A* algorithm with the start_state (numpy array), goal_test (function), successors (function) and
# heuristic (function). a_star prints the solution from start_state to goal_state (path), calculates the number of
# generated nodes (node_generated) and expanded nodes (node_expanded), and the solution depth (len(path)-1). a_star
# also provides the following functions for printing states and moves: prettyMoves(path): Translate the solution to a
# list of moves printlists(path): Visualize the solution and Print a list of states
def a_star(start_state, goal_test, successors, heuristic):
    goal_node, node_generated, node_expanded = astar.a_star_search(start_state, goal_test, successors, heuristic)
    if goal_node:
        node = goal_node
        path = [node.state1]
        while node.parent:
            node = node.parent
            path.append(node.state1)
        path.reverse()

        # print('My path:{}'.format(path))
        # print(prettyMoves(path))
        # printlists(path)
        print('Nodes Generated by A*: {}'.format(node_generated))
        print('Nodes Expanded by A*: {}'.format(node_expanded))
        print('Solution Depth: {}'.format(len(path) - 1))
    else:
        print('no solution found')


# A shortcut function
# Transform the input state to numpy array. For other functions, the state s is presented as a numpy array.
# Goal-test and next-states stay the same throughout the assignment
# You can just call sokoban(init-state, heuristic function) to test the result
def sokoban(s, h):
    return a_star(np.array(s), goal_test, next_states, h)


# Define some global variables
blank = 0
wall = 1
box = 2
keeper = 3
star = 4
boxstar = 5
keeperstar = 6


# Some helper functions for checking the content of a square
def isBlank(v):
    return (v == blank)


def isWall(v):
    return (v == wall)


def isBox(v):
    return (v == box)


def isKeeper(v):
    return (v == keeper)


def isStar(v):
    return (v == star)


def isBoxstar(v):
    return (v == boxstar)


def isKeeperstar(v):
    return (v == keeperstar)


# Help function for get KeeperPosition
# Given state s (numpy array), return the position of the keeper by row, col
# The top row is the zeroth row
# The first (right) column is the zeroth column
def getKeeperPosition(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if (isKeeper(s[i, j]) or isKeeperstar(s[i, j])):
                return i, j


# For input list s_list, remove all None element
# For example, if s_list = [1, 2, None, 3], returns [1, 2, 3]
def cleanUpList(s_list):
    clean = []
    for state in s_list:
        if state is not None:
            clean.append(state)
    return clean


# Returns True if and only if s (numpy array) is a goal state of a Sokoban game.
# (no box is on a non-goal square)
# The number of goals can be larger than the number of boxes.

# Make sure each box is in a goal
def goal_test(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            # must not be any misplaced boxes
            if isBox(s[i, j]):
                return False
    return True

# Returns the list of successor states of s (numpy array).
#
# This is the top-level next-states (successor) function.
#
# You can define the function try-move and decide how to represent UP,DOWN,LEFT,RIGHT.
# Any None result in the list can be removed by cleanUpList.
#
# When generated the successors states, you may need to copy the current state s (numpy array).
# A shallow copy (e.g, direcly set s1 = s) constructs a new compound object and then inserts references 
# into it to the objects found in the original. In this case, any change in the numpy array s1 will also affect
# the original array s. Thus, you may need a deep copy (e.g, s1 = np.copy(s)) to construct an indepedent array.

# Return a list of states, one for each direction in which the keeper is moved.
def next_states(s):
    row, col = getKeeperPosition(s)
    s_list = []
    dirs = ['u', 'd', 'l', 'r']
    # find next states for each direction
    for dir in dirs:
        s_list.append(try_move(np.copy(s), dir))
    return cleanUpList(s_list)


# This helper function for next_states() updates the grid after moving the keeper in the specified direction.
def try_move(s, d):
    r, c = getKeeperPosition(s)
    # val is either 3 (keeper) or 6 (keeperstar)
    val = s[r, c]
    
    # up
    if d == 'u':
        # must be in bounds
        if r-1 >= 0:
            v = s[r-1, c]
            # blank
            if isBlank(v):
                s[r-1, c] = keeper
            # goal
            elif isStar(v):
                s[r-1, c] = keeperstar
            # keeper pushes a box
            elif isBox(v) or isBoxstar(v):
                # must be in bounds
                if r-2 >= 0:
                    w = s[r-2, c]
                    # push box into a blank square
                    if isBlank(w):
                        s[r-2, c] = box
                    # push box into a goal
                    elif isStar(w):
                        s[r-2, c] = boxstar
                    else:
                        return None
                    
                    # move keeper into the blank square once the box is moved
                    if isBox(v):
                        s[r-1, c] = keeper
                    # move keeper into the goal once the box is moved
                    else:
                        s[r-1, c] = keeperstar
                else:
                    return None
            else:
                return None
        else:
            return None

    # down
    elif d == 'd':
        # must be in bounds
        if r+1 < s.shape[0]:
            v = s[r+1, c]
            # blank
            if isBlank(v):
                s[r+1, c] = keeper
            # goal
            elif isStar(v):
                s[r+1, c] = keeperstar
            # keeper pushes a box
            elif isBox(v) or isBoxstar(v):
                # must be in bounds
                if r+2 < s.shape[0]:
                    w = s[r+2, c]
                    # push box into a blank square
                    if isBlank(w):
                        s[r+2, c] = box
                    # push box into a goal
                    elif isStar(w):
                        s[r+2, c] = boxstar
                    else:
                        return None
                    
                    # move keeper into the blank square once the box is moved
                    if isBox(v):
                        s[r+1, c] = keeper
                    # move keeper into the goal once the box is moved
                    else:
                        s[r+1, c] = keeperstar
                else:
                    return None
            else:
                return None
        else:
            return None
    
    # left
    elif d == 'l':
        # must be in bounds
        if c-1 >= 0:
            v = s[r, c-1]
            # blank
            if isBlank(v):
                s[r, c-1] = keeper
            # goal
            elif isStar(v):
                s[r, c-1] = keeperstar
            # keeper pushes a box
            elif isBox(v) or isBoxstar(v):
                # must be in bounds
                if c-2 >= 0:
                    w = s[r, c-2]
                    # push box into a blank square
                    if isBlank(w):
                        s[r, c-2] = box
                    # push box into a goal
                    elif isStar(w):
                        s[r, c-2] = boxstar
                    else:
                        return None
                    
                    # move keeper into the blank square once the box is moved
                    if isBox(v):
                        s[r, c-1] = keeper
                    # move keeper into the goal once the box is moved
                    else:
                        s[r, c-1] = keeperstar
                else:
                    return None
            else:
                return None
        else:
            return None
    
    # right
    elif d == 'r':
        # must be in bounds
        if c+1 < s.shape[1]:
            v = s[r, c+1]
            # blank
            if isBlank(v):
                s[r, c+1] = keeper
            # goal
            elif isStar(v):
                s[r, c+1] = keeperstar
            # keeper pushes a box
            elif isBox(v) or isBoxstar(v):
                # must be in bounds
                if c+2 < s.shape[1]:
                    w = s[r, c+2]
                    # push box into a blank square
                    if isBlank(w):
                        s[r, c+2] = box
                    # push box into a goal
                    elif isStar(w):
                        s[r, c+2] = boxstar
                    else:
                        return None
                    
                    # move keeper into the blank square once the box is moved
                    if isBox(v):
                        s[r, c+1] = keeper
                    # move keeper into the goal once the box is moved
                    else:
                        s[r, c+1] = keeperstar
                else:
                    return None
            else:
                return None
        else:
            return None
    
    # update keeper's starting position
    if isKeeper(val):
        s[r, c] = blank
    else:
        s[r, c] = star
    return s


# Trivial admissible heuristic.
def h0(s):
    return 0


# Computes the number of misplaced boxes in state s (numpy array).

# This heuristic is admissible because it always returns a lower bound for the number of moves needed to reach a goal state.
# For instance, if there are 2 misplaced boxes, it will always take a minimum of 2 moves to reach the goal state.
# It is impossible for the real cost to be less than the number returned by this heuristic.
def h1(s):
    row = s.shape[0]
    col = s.shape[1]
    count = 0
    for i in range(row):
        for j in range(col):
            # increment number of misplaced boxes
            if isBox(s[i, j]):
                count += 1
    return count


# Computes an admissible heuristic value of s. 

# This heuristic finds a rough estimate of the total distance from each box to a goal,
# plus the distance from the keeper to the farthest box. This heuristic is admissible
# because it provides a lower bound for the number of moves needed to move the keeper to
# the farthest box, and move each box to a goal.
def h905565602(s):

    # get positions of keeper and all boxes and goals
    boxes = []
    goals = []
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if isBox(s[i, j]):
                boxes.append((i, j))
            elif isStar(s[i, j]):
                goals.append((i, j))
            elif isKeeper(s[i, j]):
                k = (i, j)
            elif isKeeperstar(s[i, j]):
                goals.append((i, j))
                k = (i, j)
    
    # total distance
    dist = 0
    if len(boxes) > 0:

        # find the closest goal to the first box (more likely to be the farthest away from center)
        b = boxes[0]
        min_dist = np.abs(goals[0][0]-b[0]) + np.abs(goals[0][1]-b[1])
        closest_goal = goals[0]
        for g in goals:
            if g != goals[0]:
                temp = np.abs(g[0]-b[0]) + np.abs(g[1]-b[1])
                if temp < min_dist:
                    min_dist = temp
                    closest_goal = g
        
        # this distance represents the minimum number of vertical and horizontal moves needed
        dist += min_dist
        # keeper to first box distance
        dist += np.abs(k[0]-b[0]) + np.abs(k[1]-b[1])
        
        # assume this goal is the closest to all other boxes
        for box in boxes:
            if box != b:
                # box to goal distance
                dist += np.abs(closest_goal[0]-box[0]) + np.abs(closest_goal[1]-box[1])
    return dist


# Some predefined problems with initial state s (array). Sokoban function will automatically transform it to numpy
# array. For other function, the state s is presented as a numpy array. You can just call sokoban(init-state,
# heuristic function) to test the result Each problem can be visualized by calling prettyMoves(path) and printlists(
# path) in a_star function
#
# Problems are roughly ordered by their difficulties.
# For most problems, we also provide 2 additional number per problem:
#    1) # of nodes expanded by A* using our next-states and h0 heuristic.
#    2) the depth of the optimal solution.
# These numbers are located at the comments of the problems. For example, the first problem below 
# was solved by 80 nodes expansion of A* and its optimal solution depth is 7.
# 
# Your implementation may not result in the same number of nodes expanded, but it should probably
# give something in the same ballpark. As for the solution depth, any admissible heuristic must 
# make A* return an optimal solution. So, the depths of the optimal solutions provided could be used
# for checking whether your heuristic is admissible.
#
# Warning: some problems toward the end are quite hard and could be impossible to solve without a good heuristic!


# [80,7]
s1 = [[1, 1, 1, 1, 1, 1],
      [1, 0, 3, 0, 0, 1],
      [1, 0, 2, 0, 0, 1],
      [1, 1, 0, 1, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [110,10],
s2 = [[1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 2, 1, 4, 1],
      [1, 3, 0, 0, 1, 0, 1],
      [1, 1, 1, 1, 1, 1, 1]]

# [211,12],
s3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 2, 0, 3, 4, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [300,13],
s4 = [[1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 0, 0, 1, 4],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 1, 1, 0, 0],
      [0, 0, 1, 0, 0, 0, 0],
      [0, 2, 1, 0, 0, 0, 0],
      [0, 3, 1, 0, 0, 0, 0]]

# [551,10],
s5 = [[1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 4, 2, 2, 4, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 1, 3, 1, 1, 1],
      [1, 1, 1, 1, 1, 1]]

# [722,12],
s6 = [[1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 4, 1],
      [1, 0, 0, 0, 2, 2, 3, 1],
      [1, 0, 0, 1, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1, 1, 1]]

# [1738,50],
s7 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 1, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
      [0, 2, 1, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 0, 0, 0, 1, 4]]

# [1763,22],
s8 = [[1, 1, 1, 1, 1, 1],
      [1, 4, 0, 0, 4, 1],
      [1, 0, 2, 2, 0, 1],
      [1, 2, 0, 1, 0, 1],
      [1, 3, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [1806,41],
s9 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 0, 0, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 2, 0, 1],
      [1, 0, 1, 0, 0, 1, 2, 0, 1],
      [1, 0, 4, 0, 4, 1, 3, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [10082,51],
s10 = [[1, 1, 1, 1, 1, 0, 0],
       [1, 0, 0, 0, 1, 1, 0],
       [1, 3, 2, 0, 0, 1, 1],
       [1, 1, 0, 2, 0, 0, 1],
       [0, 1, 1, 0, 2, 0, 1],
       [0, 0, 1, 1, 0, 0, 1],
       [0, 0, 0, 1, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 1, 1]]

# [16517,48],
s11 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 4, 1],
       [1, 0, 2, 2, 1, 0, 1],
       [1, 0, 2, 0, 1, 3, 1],
       [1, 1, 2, 0, 1, 0, 1],
       [1, 4, 0, 0, 4, 0, 1],
       [1, 1, 1, 1, 1, 1, 1]]

# [22035,38],
s12 = [[0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
       [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
       [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 1, 4, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]]

# [26905,28],
s13 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 2, 0, 1],
       [1, 0, 2, 0, 0, 0, 0, 0, 4, 1],
       [1, 0, 3, 0, 0, 0, 0, 0, 2, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [41715,53],
s14 = [[0, 0, 1, 0, 0, 0, 0],
       [0, 2, 1, 4, 0, 0, 0],
       [0, 2, 0, 4, 0, 0, 0],
       [3, 2, 1, 1, 1, 0, 0],
       [0, 0, 1, 4, 0, 0, 0]]

# [48695,44],
s15 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 2, 2, 0, 1],
       [1, 0, 2, 0, 2, 3, 1],
       [1, 4, 4, 1, 1, 1, 1],
       [1, 4, 4, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0]]

# [91344,111],
s16 = [[1, 1, 1, 1, 1, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [1, 2, 1, 0, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 5, 0, 5, 0, 1],
       [1, 0, 5, 0, 1, 0, 1, 1],
       [1, 1, 1, 0, 3, 0, 1, 0],
       [0, 0, 1, 1, 1, 1, 1, 0]]

# [3301278,76],
# Warning: This problem is very hard and could be impossible to solve without a good heuristic!
s17 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 3, 0, 0, 1, 0, 0, 0, 4, 1],
       [1, 0, 2, 0, 2, 0, 0, 4, 4, 1],
       [1, 0, 2, 2, 2, 1, 1, 4, 4, 1],
       [1, 0, 0, 0, 0, 1, 1, 4, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]]

# [??,25],
s18 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 4, 1, 0, 0, 0, 0]]

# [??,21],
s19 = [[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 4],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 2, 0, 4, 1, 0, 0, 0]]


# Utility functions for printing states and moves.
# You do not need to understand any of the functions below this point.


# Helper function of prettyMoves
# Detect the move from state s --> s1
def detectDiff(s, s1):
    row, col = getKeeperPosition(s)
    row1, col1 = getKeeperPosition(s1)
    if (row1 == row + 1):
        return 'Down'
    if (row1 == row - 1):
        return 'Up'
    if (col1 == col + 1):
        return 'Right'
    if (col1 == col - 1):
        return 'Left'
    return 'fail'


# Translates a list of states into a list of moves
def prettyMoves(lists):
    initial = 0
    action = []
    for states in (lists):
        if (initial != 0):
            action.append(detectDiff(previous, states))
        initial = 1
        previous = states
    return action


# Print the content of the square to stdout.
def printsquare(v):
    if (v == blank):
        print(' ', end='')
    if (v == wall):
        print('#', end='')
    if (v == box):
        print('$', end='')
    if (v == keeper):
        print('@', end='')
    if (v == star):
        print('.', end='')
    if (v == boxstar):
        print('*', end='')
    if (v == keeperstar):
        print('+', end='')


# Print a state
def printstate(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            printsquare(s[i, j])
        print('\n')


# Print a list of states with delay.
def printlists(lists):
    for states in (lists):
        printstate(states)
        print('\n')


if __name__ == "__main__":

    sokoban(s1, h905565602)

    sokoban(s2, h905565602)

    sokoban(s3, h905565602)

    sokoban(s4, h905565602)

    sokoban(s5, h905565602)

    sokoban(s6, h905565602)

    sokoban(s7, h905565602)

    sokoban(s8, h905565602)