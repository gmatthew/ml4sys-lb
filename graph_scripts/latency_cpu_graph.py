import matplotlib.pyplot as plt
import numpy as np

files = ["CPU_latency_files/rr_5m_latency.txt", "CPU_latency_files/least_req_5m_latency.txt", "CPU_latency_files/random_5m_latency.txt", "CPU_latency_files/ma_lb_5m_latency.txt"]
#files = ["CPU_latency_files/rr_1m_latency.txt", "CPU_latency_files/least_req_1m_latency.txt", "CPU_latency_files/random_1m_latency.txt", "CPU_latency_files/ma_lb_1m_latency.txt"]

line_colour = ["green", "blue", "red", "purple"]
labels = ["Round Robin", "Least Request", "Random", "Metric Aware"]
i = 0

plt.xticks(np.arange(5, 270, 5))
fig, ax = plt.subplots()

for file in files: 
    f=open(file,"r")
    lines=f.readlines()
    t = []
    s = []

    for x in lines:
        spl = x.split()
        t.append(float(spl[0]))
        s.append(float(spl[1]))
    f.close()
    
    line2, = ax.plot(t, s, color=line_colour[i], label=labels[i])
    ax.legend()
    i = i+1

    ax.set(xlabel='Latency (s)', ylabel='Percentile')
    #ax.set(xlabel='Latency (s)', ylabel='Percentile',
        #title='Latency cumulative distribution when running CPU intensive task')
        
plt.savefig("CPU-5m-latency.jpg")