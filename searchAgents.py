# searchAgents.py
# ---------------
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


from game import Directions
from game import Agent
from game import Actions
from layout import Layout, CORNER_LOCATION
import util
import time
import search


def cornersHeuristic(state, problem):
    position, visited_corners = state
    corners = problem.corners  # the coordinates of the corners
    unvisited_corners = [corner for i, corner in enumerate(corners) if not visited_corners[i]]

    # If all corners are visited, the heuristic cost is zero.
    if not unvisited_corners:
        return 0

    # Calculate heuristic as the sum of minimum distances between unvisited corners.
    heuristic_cost = 0
    current_position = position

    while unvisited_corners:
        # Find the closest corner from the current position.
        distances = [(util.manhattanDistance(current_position, corner), corner) for corner in unvisited_corners]
        min_distance, closest_corner = min(distances)

        # Accumulate the minimum distance and update current position.
        heuristic_cost += min_distance
        current_position = closest_corner

        # Remove the visited corner from unvisited_corners.
        unvisited_corners.remove(closest_corner)

    return heuristic_cost


#######################################################
#                DONT CHANGE THIS PART                #
#######################################################
class SearchAgent(Agent):
    """
    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):

        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


#######################################################
#                DONT CHANGE THIS PART                #
#######################################################
class PositionSearchProblem(search.SearchProblem):
    """
    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y] : return 999999
            cost += self.costFn((x, y))
        return cost


#######################################################
#                DONT CHANGE THIS PART                #
#######################################################
class CornersProblem(search.SearchProblem):
    def __init__(self, startingGameState):

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()

        corners = set(CORNER_LOCATION)
        self.corners = tuple(corners)

        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded

        self.startingGameState = startingGameState
        cornersVisited = [False for _ in range(len(self.corners))]
        self.startingState = (self.startingPosition, tuple(cornersVisited))

    def getStartState(self):
        return self.startingState

    def isGoalState(self, state):
        all_corner_state = state[1]
        if False in all_corner_state:
            return False
        return True

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:

            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if not hitsWall:

                nextState = (nextx, nexty)
                cost = 1

                cornersVisited = list(state[1])

                for i, corner_state in enumerate(self.corners):
                    if nextState == corner_state:
                        cornersVisited[i] = True
                        cost -= 1

                successors.append(((nextState, tuple(cornersVisited)), action, cost))

        self._expanded += 1
        return successors

    def getCostOfActions(self, actions):

        if actions is None:
            return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)
