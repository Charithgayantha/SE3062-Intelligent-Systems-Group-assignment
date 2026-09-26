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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    from util import Stack
    
    # Initialize the fringe as a Stack (LIFO)
    fringe = Stack()
    # Push the starting state and an empty list of actions
    fringe.push((problem.getStartState(), []))
    
    # Keep track of states we have already expanded to avoid loops
    expanded = set()
    
    while not fringe.isEmpty():
        # Pop the current state and the path taken to get there
        current_state, path = fringe.pop()
        
        # If we reached the goal, return the path
        if problem.isGoalState(current_state):
            return path
            
        # If we haven't expanded this state yet
        if current_state not in expanded:
            expanded.add(current_state)
            
            # Get all successors: (next_state, action, stepCost)
            for next_state, action, cost in problem.getSuccessors(current_state):
                if next_state not in expanded:
                    # Push the successor and the updated path onto the stack
                    fringe.push((next_state, path + [action]))
                    
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue
    
    # Initialize the fringe as a Queue (FIFO)
    fringe = Queue()
    # Push the starting state and an empty list of actions
    fringe.push((problem.getStartState(), []))
    
    # Keep track of states we have already expanded to avoid loops
    expanded = set()
    
    while not fringe.isEmpty():
        # Pop the current state and the path taken to get there
        current_state, path = fringe.pop()
        
        # If we reached the goal, return the path
        if problem.isGoalState(current_state):
            return path
            
        # If we haven't expanded this state yet
        if current_state not in expanded:
            expanded.add(current_state)
            
            # Get all successors: (next_state, action, stepCost)
            for next_state, action, cost in problem.getSuccessors(current_state):
                if next_state not in expanded:
                    # Push the successor and the updated path onto the queue
                    fringe.push((next_state, path + [action]))
                    
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    from util import PriorityQueue
    
    # Initialize the fringe as a Priority Queue
    fringe = PriorityQueue()
    
    # Push the starting state, empty path, and 0 initial cost
    # Format: fringe.push((state, path, current_cost), priority)
    fringe.push((problem.getStartState(), [], 0), 0)
    
    # Keep track of expanded states
    expanded = set()
    
    while not fringe.isEmpty():
        # Pop the state with the lowest cost
        current_state, path, current_cost = fringe.pop()
        
        # If we reached the goal, return the path
        if problem.isGoalState(current_state):
            return path
            
        # If we haven't expanded this state yet
        if current_state not in expanded:
            expanded.add(current_state)
            
            # Get all successors: (next_state, action, stepCost)
            for next_state, action, cost in problem.getSuccessors(current_state):
                if next_state not in expanded:
                    new_cost = current_cost + cost
                    # The priority is just the new total cost (g)
                    fringe.push((next_state, path + [action], new_cost), new_cost)
                    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    
    # Initialize the fringe as a Priority Queue
    fringe = PriorityQueue()
    start_state = problem.getStartState()
    
    # Initial heuristic value
    start_heuristic = heuristic(start_state, problem)
    
    # Push the starting state, empty path, and 0 initial cost
    # Format: fringe.push((state, path, current_cost), priority = cost + heuristic)
    fringe.push((start_state, [], 0), start_heuristic)
    
    # Keep track of expanded states
    expanded = set()
    
    while not fringe.isEmpty():
        # Pop the state with the lowest f(n) = g(n) + h(n)
        current_state, path, current_cost = fringe.pop()
        
        # If we reached the goal, return the path
        if problem.isGoalState(current_state):
            return path
            
        # If we haven't expanded this state yet
        if current_state not in expanded:
            expanded.add(current_state)
            
            # Get all successors: (next_state, action, stepCost)
            for next_state, action, cost in problem.getSuccessors(current_state):
                if next_state not in expanded:
                    new_cost = current_cost + cost
                    # The priority is total cost (g) + heuristic (h)
                    f_cost = new_cost + heuristic(next_state, problem)
                    
                    fringe.push((next_state, path + [action], new_cost), f_cost)
                    
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch