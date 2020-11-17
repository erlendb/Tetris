import matplotlib.pyplot as plt

log_file_name = 'model1.txt' # Plot this file

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

for i, d in enumerate(data):
    game.append( int(data[i][0]) )
    rounds.append( int(data[i][1]) )
    score.append( int(data[i][2]) )
    epsilon.append( float(data[i][3]) )

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

fig = plt.figure()
host = fig.add_subplot(111)
par1 = host.twinx()
par2 = host.twinx()

host.set_xlim(0, number_of_games)
host.set_ylim(min_rounds, max_rounds)
par1.set_ylim(min_score, max_score)
par2.set_ylim(min_epsilon, max_epsilon)

host.set_ylabel("Rounds")
par1.set_ylabel("Score")
par2.set_ylabel("Epsilon")

color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

p1, = host.plot(game, rounds, color=color1,label="Rounds")
p2, = par1.plot(game, score, color=color2, label="Score")
p3, = par2.plot(game, epsilon, color=color3, label="Epsilon")

lns = [p1, p2, p3]
host.legend(handles=lns, loc='best')

# right, left, top, bottom
par2.spines['right'].set_position(('outward', 60))

par2.xaxis.set_ticks(game)

# Sometimes handy, same for xaxis
#par2.yaxis.set_ticks_position('right')

host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())

plt.savefig(output_plot_file, bbox_inches='tight')