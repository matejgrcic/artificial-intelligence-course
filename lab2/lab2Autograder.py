import os
from time import time

correct = 0
total_played = 0
incorrectMazes = []
start = time()
for i in range(0,30):
    command = "pacman.py -l lay{} -p PacardAgent -a fn=logicBasedSearch -g WumpusGhost -q".format(i)
    x = os.system(command)
    if x == 0:
        correct = correct + 1
    else:
        incorrectMazes.append('lay{}'.format(i))
    total_played = total_played + 1
print "{}/{} succeded".format(correct, total_played)
print "Time elapsed {}".format(time() - start)
print incorrectMazes
