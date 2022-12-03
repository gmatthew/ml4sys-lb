import time
def do_memory_intensive_work():
  # do some memory allocation stuff that takes up space
  d = {}
  i = 0
  for j in range(0,10):
    for i in range(0, 10000000):
      d[i] = 'A'*1024
      if i % 10000 == 0:
        print(i)
        c = i

if __name__ == '__main__':
    do_memory_intensive_work()
    #print(c)