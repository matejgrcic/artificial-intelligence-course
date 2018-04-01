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
import copy

class SearchNode:
    """
    This class represents a node in the graph which represents the search problem.
    The class is used as a basic wrapper for search methods - you may use it, however
    you can solve the assignment without it.

    REMINDER: You need to fill in the backtrack function in this class!
    """

    def __init__(self, position, parent=None, transition=None, cost=0, heuristic=0):
        """
        Basic constructor which copies the values. Remember, you can access all the
        values of a python object simply by referencing them - there is no need for
        a getter method.
        """
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.transition = transition

    def __eq__(self, other):
        if other == None:
            return False
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def isRootNode(self):
        """
        Check if the node has a parent.
        returns True in case it does, False otherwise
        """
        return self.parent == None

    def unpack(self):
        """
        Return all relevant values for the current node.
        Returns position, parent node, cost, heuristic value
        """
        return self.position, self.parent, self.cost, self.heuristic


    def backtrack(self):
        """
        Reconstruct a path to the initial state from the current node.
        Bear in mind that usually you will reconstruct the path from the
        final node to the initial.
        """
        moves = []
        # make a deep copy to stop any referencing isues.
        node = copy.deepcopy(self)

        if node.isRootNode():
            # The initial state is the final state
            return moves

        from game import Directions
        s = Directions.SOUTH
        w = Directions.WEST
        n = Directions.NORTH
        e = Directions.EAST

        while node.parent != None:
            moves.append(node.transition)
            node = node.parent
        moves = moves[::-1]
        return moves



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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    startState = problem.getStartState()
    startNode = SearchNode(startState, None, None, 0, 0)
    front = [startNode]
    visitedStates = []
    while len(front) != 0:
        node = front.pop()
        if node in visitedStates:
            continue
        if problem.isGoalState(node.position):
            return node.backtrack()
        visitedStates.append(node)
        successors = problem.getSuccessors(node.position)
        for i in range(0, len(successors)):
            successor = successors[i]
            successorNode = SearchNode(successor[0], node, successor[1], successor[2], 0)
            front.append(successorNode)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    startNode = SearchNode(startState, None, None, 0, 0)
    front = util.Queue()
    front.push(startNode)
    visitedStates = []

    while not front.isEmpty():
        node = front.pop()
        if node in visitedStates:
            continue
        if problem.isGoalState(node.position):
            return node.backtrack()
        visitedStates.append(node)
        successors = problem.getSuccessors(node.position)
        for i in range(0, len(successors)):
            successor = successors[i]
            successorNode = SearchNode(successor[0], node, successor[1], successor[2], 0)
            front.push(successorNode)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    startNode = SearchNode(startState, None, None, 0, 0)
    front = util.PriorityQueue()
    front.push(startNode, startNode.cost)
    visitedStates = []

    while not front.isEmpty():
        node = front.pop()
        if node in visitedStates:
            continue
        if problem.isGoalState(node.position):
            return node.backtrack()
        visitedStates.append(node)
        successors = problem.getSuccessors(node.position)
        for i in range(0, len(successors)):
            successor = successors[i]
            successorNode = SearchNode(successor[0], node, successor[1], successor[2] + node.cost, 0)
            front.push(successorNode, successorNode.cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    startState = problem.getStartState()
    startNode = SearchNode(startState, None, None, 0, 0)
    front = util.PriorityQueue()
    front.push(startNode, startNode.cost)
    visitedStates = {}
    open = {}
    open[startNode.position] = 0

    while not front.isEmpty():
        node = front.pop()
        if node in visitedStates:
            continue
        if problem.isGoalState(node.position):
            return node.backtrack()
        visitedStates[node] = True
        successors = problem.getSuccessors(node.position)
        for i in range(0, len(successors)):
            successor = successors[i]
            successorNode = SearchNode(successor[0], node, successor[1], successor[2] + node.cost, 0)
            if successorNode.position in open:
                if open[successorNode.position] < successorNode.cost:
                    continue
                else:
                    del open[successorNode.position]
            totalCost = max(successorNode.cost + heuristic(successorNode.position, problem), node.heuristic)
            successorNode.heuristic = totalCost
            front.push(successorNode, totalCost)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
