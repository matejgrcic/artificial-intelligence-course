import os

correct = 0
incorrectMazes = []
for i in range(0,30):
    command = "pacman.py -l lay{} -p PacardAgent -a fn=logicBasedSearch -g WumpusGhost".format(i)
    x = os.system(command)
    if x == 0:
        correct = correct + 1
    else:
        incorrectMazes.append('lay{}'.format(i))

print "{}/30 succeded".format(correct)
print incorrectMazes
