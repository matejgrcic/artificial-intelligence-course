import util

class Storage:

    def addNode(self, node, index):
        util.raiseNotDefined()

    def getNode(self):
        util.raiseNotDefined()

    def addVisitedState(self, state, cost):
        util.raiseNotDefined()

class StackStorage(Storage):

    def __init__(self):
        self.visitedStates = {}
        self._collection = util.Stack()

    def addNode(self, node, index):
        if not (node.position in self.visitedStates):
            self._collection.push(node)

    def getNode(self):
        return self._collection.pop()


    def addVisitedState(self, nodePosition, cost):
        self.visitedStates[nodePosition] = cost

class ListStorage(Storage):

    def __init__(self):
        self.visitedStates = {}
        self._collection = []

    def addNode(self, node, index):
        if not (node.position in self.visitedStates):
            self._collection.append(node)

    def getNode(self):
        self._collection = self._collection[::-1]
        node = self._collection.pop()
        self._collection = self._collection[::-1]
        return node

    def addVisitedState(self, nodePosition, cost):
        self.visitedStates[nodePosition] = cost

class PriorityQueueStorage(Storage):

    def __init__(self):
        self.visitedStates = {}
        self._collection = util.PriorityQueue()

    def addNode(self, node, index):
        if not (node.position in self.visitedStates):
            self._collection.push(node, index)


    def getNode(self):
        return self._collection.pop()


    def addVisitedState(self, nodePosition, cost):
        self.visitedStates[nodePosition] = cost

class PriorityQueueStorageWithFunction(Storage):
    def __init__(self, heuristic, problem):
        self.visitedStates = {}
        self._collection = util.PriorityQueue()
        self.heuristic = heuristic
        self.problem = problem
        self.openStates = {}

    # ako stavimo cost index ne treba
    def addNode(self, node, index):
        # if node.position in self.visitedStates:
        #     return
        heuristic = self.heuristic(node.position, self.problem)
        node.heuristic = heuristic

        if node.position in self.visitedStates:
            if self.visitedStates[node.position] > node.cost:
                del self.visitedStates[node.position]
            else:
                return;
        if node.position in self.openStates:
            if self.openStates[node.position] > node.cost:
                del self.openStates[node.position]
            else:
                return

        self._collection.push(node, heuristic + index)
        self.openStates[node.position] = node.cost

    def getNode(self):
        while True:
            node =  self._collection.pop()
            if self.openStates[node.position] != node.cost:
                continue
            del self.openStates[node.position]
            return node

    def addVisitedState(self, nodePosition, cost):
        self.visitedStates[nodePosition] = cost




