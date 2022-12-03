import numpy as np

def multiply_matrix(A,B):
  global C
  C = np.zeros((A.shape[0],B.shape[1]),dtype = int)
  if  A.shape[1] == B.shape[0]:
      for i in range(len(A)):
          for j in range(len(B[0])):
              for k in range(len(B)):
                  C[i][j] += A[i][k] * B[k][j]
  print(C[0][0])

def do_cpu_intensive_work():
  # do some metrics calculation over how many iterations
  np.random.seed(27)
  A = np.random.randint(1,35000,size = (500, 500))
  B = np.random.randint(1,56000,size = (500, 500))
  C = multiply_matrix(A,B)
  #C.sort()
  
  return(C[0][0])

if __name__ == '__main__':
    c = do_cpu_intensive_work()
    print(c)
