
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from logic import * 

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


def miniWumpusSearch(problem): 
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST 
    n = Directions.NORTH
    return  [e, n, n]

def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?", problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?", problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?",problem.isTeleporterClose(problem.getStartState())
    """
    (the slash '\\' is used to combine commands spanning through multiple lines - 
    you should remove it if you convert the commands to a single line)
    
    Feel free to create and use as many helper functions as you want.

    A couple of hints: 
        * Use the getSuccessors method, not only when you are looking for states 
        you can transition into. In case you want to resolve if a poisoned pill is 
        at a certain state, it might be easy to check if you can sense the chemicals 
        on all cells surrounding the state. 
        * Memorize information, often and thoroughly. Dictionaries are your friends and 
        states (tuples) can be used as keys.
        * Keep track of the states you visit in order. You do NOT need to remember the
        tranisitions - simply pass the visited states to the 'reconstructPath' method 
        in the search problem. Check logicAgents.py and search.py for implementation.
    """
    # array in order to keep the ordering
    visitedStates = []
    visited = {}
    opened = {}
    currentState = problem.getStartState()
    while True:
        visitedStates.append(currentState)
        visited[currentState] = True
        if problem.isGoalState(currentState):
            return reconstructPathFromStates(visitedStates)
        followingStates = problem.getSuccessors(currentState)
        attributes = {}
        attributes['W'] = []
        attributes['P'] = []
        attributes['T'] = []
        attributes['O'] = []
        for followingState in followingStates:
            state = followingState[0]
            if state in visited:
                continue
            if chech_is_W(state, problem) or chech_is_P(state, problem):
                continue
            if chech_is_T(state, problem):
                attributes['TTTT'] = state
                break
            if problem.isTeleporterClose(state):
                attributes['T'].append(state)
            if problem.isPoisonCapsuleClose(state):
                attributes['P'].append(state)
            if problem.isWumpusClose(state):
                attributes['W'].append(state)
            attributes['O'].append(state)

        if 'TTTT' in attributes.keys():
            currentState = attributes['TTTT']
        elif len(attributes['T']) > 0:
            currentState = get_best_from_list(attributes['T'], opened)
        elif len(attributes['O']) > 0:
            currentState = get_best_from_list(attributes['O'], opened)
        elif len(attributes['P']) > 0:
            currentState = get_best_from_list(attributes['P'], opened)
        else:
            currentState = get_best_from_list(attributes['W'], opened)

        for followingState in followingStates:
            opened[followingState[0]] = True


    return reconstructPathFromStates(visitedStates)






    """
    ####################################
    ###                              ###
    ###        YOUR CODE HERE        ###
    ###                              ###
    ####################################
    """

####################################
###                              ###
###        YOUR CODE THERE       ###
###                              ###
####################################


def reconstructPathFromStates(states):
    from game import Directions
    e = Directions.EAST
    n = Directions.NORTH
    s = Directions.SOUTH
    w = Directions.WEST
    path = []
    currentState = states[0]
    for i in range(1,len(states)):
        x1,y1 = currentState
        next = states[i]
        x2,y2 = next

        if x2<x1 and y1 == y2:
            path.append(w)
        elif x2 > x1 and y1 == y2:
            path.append(e)
        elif y2 > y1 and x1 == x2:
            path.append(n)
        else:
            path.append(s)
        currentState = next
    return path

def get_best_from_list(list, opened):
    min = 999999
    index = -1
    for i in range(0,len(list)):
        x,y = list[i]
        val = 20*x + y
        if val < min and not list[i] in opened.keys():
            min = val
            index = i
    if index != -1:
        return list[index]
    else:
        min = 999999
        index = -1
        for i in range(0, len(list)):
            x, y = list[i]
            val = 20 * x + y
            if val < min:
                min = val
                index = i

def chech_is_W(state, problem):
    followingStates = problem.getSuccessors(state)
    for state in followingStates:
        if not problem.isWumpusClose(state[0]):
            return False
    return True

def chech_is_P(state, problem):
    followingStates = problem.getSuccessors(state)
    for state in followingStates:
        if not problem.isPoisonCapsuleClose(state[0]):
            return False
    return True

def chech_is_T(state, problem):
    followingStates = problem.getSuccessors(state)
    for state in followingStates:
        if not problem.isTeleporterClose(state[0]):
            return False
    return True
"""
        ####################################
        ###                              ###
        ###      YOUR CODE EVERYWHERE    ###
        ###                              ###
        ####################################
"""

# Abbreviations
lbs = logicBasedSearch
