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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

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
          state: Search state

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def add_to_frontier(frontier, state, plan_cost):
    """
    Add state to frontier; state consists of a three-tuple: location, cost, path-as-list-of-directions.
    Cost used for storage is the plan_cost, which may be augmented with the heuristic
    """
    if isinstance(frontier, util.PriorityQueue):
        frontier.update(state, plan_cost)
    else:
        frontier.push(state)

def genericTreeSearch(problem: SearchProblem, frontier):
    """
    Generic search algorithm. The type of search depends on the 
    frontier provided. Supplying a stack yields DFS, a queue results in BFS 
    and a priorityqueue will do UCS.
    """
    add_to_frontier(frontier, (problem.getStartState(), 0, []), 0)
    visited = set()

    # frontier contains tuples of location, cost, path-to-location

    while not frontier.isEmpty():
        loc, cost, path = frontier.pop()
        if problem.isGoalState(loc):
            return path
        if loc not in visited:
            visited.add(loc)
            for (c_location, c_direction, c_cost) in problem.getSuccessors(loc):
                if c_location not in visited:
                    cost_to_child = cost + c_cost
                    child_state = (c_location, cost_to_child, path + [c_direction])
                    add_to_frontier(frontier, child_state, cost_to_child)
                else:
                    pass # for now .. may need to update best-path
    return []


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return genericTreeSearch(problem, util.Stack())


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return genericTreeSearch(problem, util.Queue())


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return genericTreeSearch(problem, util.PriorityQueue())

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    add_to_frontier(frontier, (problem.getStartState(), 0, []), 0)
    visited = set()
    while not frontier.isEmpty():
        loc, cost, path = frontier.pop()
        if problem.isGoalState(loc):
            return path
        if loc not in visited:
            visited.add(loc)
            for (c_location, c_direction, c_cost) in problem.getSuccessors(loc):
                child_cost =  cost + c_cost
                child_state = (c_location, child_cost, path + [c_direction])
                """
                Actual cost is stored as part of the frontier node, however the heuristic cost
                is used for its priority!
                """
                heuristic_cost = child_cost + heuristic(c_location, problem)
                add_to_frontier(frontier, child_state, heuristic_cost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
