# Sokoban
A Japanese puzzle game coded as an A* search problem.

In this game, the player controls the warehouse keeper (sokoban) who is placed in a closed warehouse with a number of boxes that need to be put in some predefined goal locations. The keeper can walk around the warehouse and push boxes around in order to get them into goal positions. The goal of this game is to put all boxes into goal positions in the fewest number of moves. The whole game (the warehouse) is on a grid. In each step, the keeper can move in any of the four basic directions (up, down, left, right). The keeper cannot walk into a wall or into a box. However, the keeper can push a box if the square next to the box (in the pushing direction) is either a goal or an empty square. Only one box can be pushed in any given step. In the case of multiple goals, there is no specific goal that a box has to be in. Boxes can be placed in goals in any order. A box can also be pushed out of a goal if needed (to make way for other moves). The game ends as soon as every box is in a goal position (even if there are more goals than boxes). In general, the minimum number of moves is not strictly required by the actual Sokoban game, because even finding a solution to the problem is already hard for a human player. Nevertheless, it is an objective of this program.

The program includes heuristic functions to optimize the A* search engine.

Each square may contain one of the following:
* Nothing (empty floor)
* A wall
* The box
* The keeper
* A goal
* A box on top of a goal
* The keeper on top of a goal

How each type of content is represented in the test cases included in hw3.py:

Content, Integer, ACII
blank, 0, ' ' (blank space)
wall, 1, '#'
box, 2, '$'
keeper, 3, '@'
goal, 4, '.'
box+goal, 5, '*'
keeper+goal, 6, '+'
