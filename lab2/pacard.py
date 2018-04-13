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
    return [e, n, n]


def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?",
               \ problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?",
               \ problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?",
               \ problem.isTeleporterClose(problem.getStartState())

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
    startState = problem.getStartState()
    visitedStates.append(startState)

    safeStates = util.PriorityQueueWithFunction(stateWeight)
    safeStates.push(startState)
    safeStateDict = {}
    safeStateDict[startState] = True
    unsureStates = {}
    unsureStatesQueue = util.PriorityQueueWithFunction(stateWeight)

    unsecureStates = {}
    knowledgeBase = set()

    while True:
        currentstate = None

        if not safeStates.isEmpty():
            currentstate = safeStates.pop()
            del safeStateDict[currentstate]
        elif not unsureStatesQueue.isEmpty():
            currentstate = unsureStatesQueue.pop()
            if not currentstate in unsureStates:
                continue
        else:
            currentstate = problem.getStartState()
            return


        visitedStates.append(currentstate)
        print 'Visiting: {}'.format(currentstate)

        if problem.isGoalState(currentstate):
            print 'Game over: Teleported home!'
            return problem.reconstructPath(visitedStates)

        check_for_stench(currentstate, problem, knowledgeBase)
        check_for_fumes(currentstate, problem, knowledgeBase)
        check_for_glow(currentstate, problem, knowledgeBase)
        check_for_safe(currentstate,problem,knowledgeBase)


        successors = problem.getSuccessors(currentstate)
        # for successor in set(successors).union(unsecureStates):
        for successor in successors:
            if successor[0] in unsecureStates.keys() or successor[0] in visitedStates:
                continue
            currentKnowledge = []
            currentKnowledge.append(conclude_whumpus(successor[0], knowledgeBase, True))
            currentKnowledge.append(conclude_poison(successor[0], knowledgeBase, True))
            currentKnowledge.append(conclude_teleporter(successor[0], knowledgeBase, True))
            currentKnowledge.append(conclude_whumpus(successor[0], knowledgeBase, False))
            currentKnowledge.append(conclude_poison(successor[0], knowledgeBase, False))
            currentKnowledge.append(conclude_teleporter(successor[0], knowledgeBase, False))
            currentKnowledge.append(conclude_safe(successor[0], knowledgeBase, False))
            currentKnowledge.append(conclude_safe(successor[0], knowledgeBase, True))

            if currentKnowledge[0]:
                knowledgeBase.add(Clause(set([Literal(Labels.WUMPUS, successor[0], True)])))
                print 'Concluded: ~w{}'.format(successor[0])
            if currentKnowledge[1]:
                knowledgeBase.add(Clause(set([Literal(Labels.POISON, successor[0], True)])))
                print 'Concluded: ~p{}'.format(successor[0])
            if currentKnowledge[2]:
                knowledgeBase.add(Clause(set([Literal(Labels.TELEPORTER, successor[0], True)])))
                print 'Concluded: ~t{}'.format(successor[0])
            if currentKnowledge[3]:
                knowledgeBase.add(Clause(set([Literal(Labels.WUMPUS, successor[0], False)])))
                print 'Concluded: w{}'.format(successor[0])
            if currentKnowledge[4]:
                knowledgeBase.add(Clause(set([Literal(Labels.POISON, successor[0], False)])))
                print 'Concluded: p{}'.format(successor[0])
            if currentKnowledge[5]:
                knowledgeBase.add(Clause(set([Literal(Labels.TELEPORTER, successor[0], False)])))
                print 'Concluded: t{}'.format(successor[0])

            #safe
            if currentKnowledge[0] and currentKnowledge[1] :
                knowledgeBase.add(Clause(set([Literal(Labels.SAFE, successor[0], False)])))
                print 'Concluded: o{}'.format(successor[0])

                if not successor[0] in safeStateDict.keys():
                    safeStates.push(successor[0])
                    safeStateDict[successor[0]] = True

                if successor[0] in unsureStates.keys():
                    unsureStates.pop(successor[0])
            #ne znam sta je
            else:
                knowledgeBase.add(Clause(set([Literal(Labels.SAFE, successor[0], True)])))
                unsureStates[successor[0]] = True
                unsureStatesQueue.push(successor[0])

            if currentKnowledge[3] or currentKnowledge[4]:
                unsecureStates[successor[0]] = True
                if successor[0] in unsureStates.keys():
                    unsureStates.pop(successor[0])


def conclude_whumpus(state, knowledgeBase, isTrue):
    premise = Clause(set([Literal(Labels.WUMPUS, state, isTrue)]))
    return resolution(knowledgeBase, premise)


def conclude_poison(state, knowledgeBase, isTrue):
    premise = Clause(set([Literal(Labels.POISON, state, isTrue)]))
    return resolution(knowledgeBase, premise)


def conclude_teleporter(state, knowledgeBase, isTrue):
    premise = Clause(set([Literal(Labels.TELEPORTER, state, isTrue)]))
    return resolution(knowledgeBase, premise)

def conclude_safe(state, knowledgeBase, isTrue):
    premise = Clause(set([Literal(Labels.SAFE, state, isTrue)]))
    return resolution(knowledgeBase, premise)

def check_for_stench(state, problem, knowledgeBase):
    x = 's'
    if not problem.isWumpusClose(state):
        x = '~s'
    print "Sensed: {}{}".format(x, state)

    if problem.isWumpusClose(state):
        literals = set()
        for successor in problem.getSuccessors(state):
            literals.add(Literal(Labels.WUMPUS, successor[0], False))
        knowledgeBase.add(Clause(literals))
    else:
        for successor in problem.getSuccessors(state):
            knowledgeBase.add(Clause(set([Literal(Labels.WUMPUS, successor[0], True)])))

def check_for_safe(state, problem, knowledgeBase):

    if not problem.isWumpusClose(state) and not problem.isPoisonCapsuleClose(state):
        knowledgeBase.add(Clause(set([Literal(Labels.SAFE, state, False)])))
        for successor in problem.getSuccessors(state):
            knowledgeBase.add(Clause(set([Literal(Labels.SAFE, successor[0], False)])))


def check_for_glow(state, problem, knowledgeBase):
    x = 'g'
    if not problem.isTeleporterClose(state):
        x = '~g'
    print "Sensed: {}{}".format(x, state)
    if problem.isTeleporterClose(state):
        literals = set()
        for successor in problem.getSuccessors(state):
            literals.add(Literal(Labels.TELEPORTER, successor[0], False))
        knowledgeBase.add(Clause(literals))
    else:
        for successor in problem.getSuccessors(state):
            knowledgeBase.add(Clause(set([Literal(Labels.TELEPORTER, successor[0], True)])))


def check_for_fumes(state, problem, knowledgeBase):
    x = 'b'
    if not problem.isPoisonCapsuleClose(state):
        x = '~b'
    print "Sensed: {}{}".format(x, state)
    if problem.isPoisonCapsuleClose(state):
        literals = set()
        for successor in problem.getSuccessors(state):
            literals.add(Literal(Labels.POISON, successor[0], False))
        knowledgeBase.add(Clause(literals))
    else:
        for successor in problem.getSuccessors(state):
            knowledgeBase.add(Clause(set([Literal(Labels.POISON, successor[0], True)])))

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

"""
        ####################################
        ###                              ###
        ###      YOUR CODE EVERYWHERE    ###
        ###                              ###
        ####################################
"""


def priority_function(state):
    x, y = state
    return 20 * x + y


# Abbreviations
lbs = logicBasedSearch
