# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def depthFirstSearch(problem):
    initial_state = problem.getStartState()
    frontiers = util.Stack()
    frontiers.push((initial_state, []))
    reached_states = set()

    while not frontiers.isEmpty():
        state, path = frontiers.pop()

        if problem.isGoalState(state):
            return path

        if state not in reached_states:
            reached_states.add(state)
            for successor, action, _ in problem.getSuccessors(state):
                new_path = path + [action]
                frontiers.push((successor, new_path))

    raise Exception("404 not found")


def breadthFirstSearch(problem):
    initial_state = problem.getStartState()
    frontiers = util.Queue()
    frontiers.push((initial_state, []))
    reached_states = {initial_state}

    while not frontiers.isEmpty():
        state, path = frontiers.pop()

        if problem.isGoalState(state):
            return path

        for child, action, _ in problem.getSuccessors(state):
            if child not in reached_states:
                reached_states.add(child)
                frontiers.push((child, path + [action]))

    raise Exception("404 not found")


def uniformCostSearch(problem):
    initial_state = problem.getStartState()
    frontiers = util.PriorityQueue()
    frontiers.push((initial_state, []), 0)
    reached_states = {}

    while not frontiers.isEmpty():
        state, path = frontiers.pop()

        if problem.isGoalState(state):
            return path

        path_cost = problem.getCostOfActions(path)
        if state not in reached_states or path_cost < reached_states[state]:
            reached_states[state] = path_cost

            for successor, action, step_cost in problem.getSuccessors(state):
                new_path = path + [action]
                new_cost = problem.getCostOfActions(new_path)
                frontiers.push((successor, new_path), new_cost)

    raise Exception("404 not found")


def nullHeuristic(state, problem=None):
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    initial_state = problem.getStartState()
    frontiers = util.PriorityQueue()
    frontiers.push((initial_state, []), heuristic(initial_state, problem))
    reached_states = {}

    while not frontiers.isEmpty():
        state, path = frontiers.pop()

        if problem.isGoalState(state):
            return path

        path_cost = problem.getCostOfActions(path)
        if state not in reached_states or path_cost < reached_states[state]:
            reached_states[state] = path_cost

            for successor, action, step_cost in problem.getSuccessors(state):
                new_path = path + [action]
                new_cost = problem.getCostOfActions(new_path) + heuristic(successor, problem)
                frontiers.push((successor, new_path), new_cost)
    raise Exception("404 not found")


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
