import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

def get_free_space_mb():
    partitions = psutil.disk_partitions()
  
    for partition in partitions:
        if partition.device == 'C:\\':
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                free_space_mb = usage.free / (1024 * 1024)  # Convert bytes to megabytes
                return free_space_mb
            except PermissionError:
                continue
    return 0

# Sliding window
max_length = 200
free_space_deque = deque([get_free_space_mb()], maxlen=max_length)

def update(frame, line, label):
  
    free_space_info = get_free_space_mb()
    free_space_deque.append(free_space_info)
  
    line.set_data(range(len(free_space_deque)), free_space_deque)
    label.set_text("{:.2f} MB".format(free_space_deque[-1]))
  
    ax.relim()
    ax.autoscale_view()
  
    return line, label



if __name__ == "__main__":
    initial_free_space = get_free_space_mb()
    fig, ax = plt.subplots()
    line, = ax.plot(range(max_length), [initial_free_space] * max_length, color='blue')
    ax.set_ylabel('Free Space (MB)')
    ax.set_title('Free Disk Space on Volume C:\\')
    label = ax.text(0.8, 0.9, '{:.2f} MB'.format(initial_free_space), transform=ax.transAxes)
    ani = animation.FuncAnimation(fig, update, fargs=(line, label), interval=1000)  # Update every 1 second
    plt.show()
