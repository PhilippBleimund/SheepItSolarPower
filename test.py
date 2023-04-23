from KSEM import *
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    result = read('192.168.178.116', 502)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(result['activePower'])

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks([])
    #plt.subplots_adjust(bottom=0.30)
    plt.ylim([-2000, 1000])
    plt.title('Home usage over time')
    plt.ylabel('power (Watts)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
plt.show()