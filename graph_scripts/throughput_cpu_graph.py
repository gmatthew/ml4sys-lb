import matplotlib.pyplot as plt
import numpy as np


labels = ['Round Robin', 'Least Request', 'Random', 'Metric Aware']
one_min_vals = [3.345, 5.355, 2.99, 3.675]
five_min_vals = [3.14, 5.57, 3.09, 4.4]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, one_min_vals, width, label='1 minute')
rects2 = ax.bar(x + width/2, five_min_vals, width, label='5 minutes')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Throughput (req/s)')
#ax.set_title('Throughput when running CPU intensive tasks')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.savefig("CPU-throughput.jpg")