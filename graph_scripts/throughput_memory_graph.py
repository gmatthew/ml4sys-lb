import matplotlib.pyplot as plt
import numpy as np


labels = ['Round Robin', 'Least Request', 'Random', 'Metric Aware']
one_min_vals = [62.145, 62.145, 59.98, 42.24]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, one_min_vals, width, label='1 minute')

ax.set_ylabel('Throughput (req/s)')
#ax.set_title('Throughput when running memory intensive tasks')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)

fig.tight_layout()

plt.savefig("Memory-throughput.jpg")