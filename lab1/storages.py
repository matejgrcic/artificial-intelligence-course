import util

class Storage:
    def addNode(self, node):
        util.raiseNotDefined()

    def getNode(self):
        util.raiseNotDefined()

class StackStorage(Storage):

    def __init__(self):
        self._collection = util.Stack()

    def addNode(self, node):
        self._collection.push(node)

    def getNode(self):
        return self._collection.pop()

class ListStorage(Storage):

    def __init__(self):
        self._collection = []

    def addNode(self, node):
        self._collection.append(node)

    def getNode(self):
        self._collection = self._collection[::-1]
        node = self._collection.pop()
        self._collection = self._collection[::-1]
        return node

