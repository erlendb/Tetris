# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np

log_file_name = '1605696464.7455516-tester-pr-agent.txt' # Plot this file
plot_title = u'Tetris med trening på bare siste spill'
subtitle = True

input_log_file = 'logs/' + log_file_name
output_plot_file = 'plots/' + log_file_name + '.png'

data_starts_at_line = 5
header_line = data_starts_at_line - 1

file = open(input_log_file, 'r')
lines = file.readlines()
file.close()

header = lines[header_line - 1].split()
data = []
for index, line in enumerate(lines):
    if index < data_starts_at_line - 1:
        continue
    data.append(line.split())

#print(header)
#print(data)

game = []
rounds = []
score = []
epsilon = []
cleared_lines = []

for i, d in enumerate(data):
    game.append( int(data[i][0]) )
    rounds.append( int(data[i][1]) )
    score.append( int(data[i][2]) )
    epsilon.append( float(data[i][3]) )
    if (len(data[1]) > 4):
        cleared_lines.append( float(data[i][4]) )
    else:
        #cleared_lines.append(0)
        cl = int(data[i][2]) - int(data[i][1]) + 10 + 1
        cleared_lines.append(cl)

#print(game)
#print(rounds)
#print(score)
#print(epsilon)

number_of_games = len(data)
min_rounds = 0
max_rounds = max(rounds)
min_score = min(score)
max_score = max(score)
min_epsilon = 0
max_epsilon = 1
min_cleared_lines = 0
max_cleared_lines = max(cleared_lines)

fig = plt.figure()
host = fig.add_subplot(111)
par1 = host.twinx()
par2 = host.twinx()
par3 = host.twinx()

host.set_xlim(0, number_of_games)
host.set_ylim(min_rounds, max_rounds)
par1.set_ylim(min_score, max_score)
par2.set_ylim(min_epsilon, max_epsilon)
par3.set_ylim(min_cleared_lines, max_cleared_lines)

fig.suptitle(plot_title)
if subtitle:
    host.set_title("Games: " + str(max(game)))

host.set_xlabel("Game number")
host.set_ylabel("Rounds")
par1.set_ylabel("Score")
par2.set_ylabel("Epsilon")
par3.set_ylabel("Cleared lines")

color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)
color4 = plt.cm.viridis(.8)

p1, = host.plot(game, rounds, '.', color=color1,label="Rounds")
p2, = par1.plot(game, score, '.', color=color2, label="Score")
p3, = par2.plot(game, epsilon, color=color3, label="Epsilon")
p4, = par3.plot(game, cleared_lines, '.', color=color4, label="Cleared lines")

rounds_polyfit = np.polyfit(game, rounds, 1)
rounds_trend = np.poly1d(rounds_polyfit)
host.plot(game, rounds_trend(game), color=color1)

score_polyfit = np.polyfit(game, score, 1)
score_trend = np.poly1d(score_polyfit)
par1.plot(game, score_trend(game), color=color2)

cleared_lines_polyfit = np.polyfit(game, cleared_lines, 1)
cleared_lines_trend = np.poly1d(cleared_lines_polyfit)
#par1.plot(game, cleared_lines_trend(game), color=color4)

lns = [p1, p2, p3, p4]
host.legend(handles=lns, loc='best')

# right, left, top, bottom
par2.spines['right'].set_position(('outward', 120))
par3.spines['right'].set_position(('outward', 60))

par2.xaxis.set_ticks(game)
plt.locator_params(axis='x', nbins=5)

# Sometimes handy, same for xaxis
#par2.yaxis.set_ticks_position('right')

host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())
par3.yaxis.label.set_color(p4.get_color())

plt.savefig(output_plot_file, bbox_inches='tight')