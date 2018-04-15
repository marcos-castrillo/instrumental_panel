import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# Here, the only new import is the matplotlib.animation as animation. This is the module that will allow us to animate the figure after it has been shown.

# Next, we'll add some code that you should be familiar with if you're following this series:

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
# Now we write the animation function:

def animate(i):
    graph_data = open('example.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)