import logic
import os
import sys
import time

correct = 0


def resolveTest(path):
    global correct
    f = open(path)
    premises = set()

    solution = f.readline().strip()
    for line in f:
        literals = set()
        lineSplit = line.split()
        for lit in lineSplit:
            if lit.startswith('-'):
                literals.add(logic.Literal(lit[1:], (0, 0), True))
            else:
                literals.add(logic.Literal(lit, (0, 0), False))
        last = logic.Clause(literals)
        premises.add(last)
    goal = last
    premises.remove(last)
    resolution = logic.resolution(premises, goal)
    if str(resolution) == solution:
        correct += 1
    return 'Calculated: '+ str(resolution) + ' Correct solution: ' + solution


if __name__ == '__main__':
    total = 0
    cnt = 0
    for subdir, dirs, files in os.walk('./test/'):
        for file in files:
            filename = subdir + os.sep + file
            cnt = cnt + 1
            print 'test{}:'.format(cnt)
            print resolveTest(filename)
            print
            total += 1
    time.sleep(0.5)
    print >> sys.stderr, '+++++++++++++++++++++++++++++++++++++++++'
    print >> sys.stderr, 'Total: ' + str(correct) + '/' + str(total) + ' passed!'
