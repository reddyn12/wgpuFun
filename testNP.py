import numpy as np
import time


data = np.array([[1,2,3,4,5,6,67,7,8,8,8,9],[1,2,3,4,5,6,67,7,8,8,8,9]])
data1 = np.array([[1,2,3,4,5,6,67,7,8,8,8,9],[1,2,3,4,5,6,67,7,8,8,8,9]])


numpy_data = np.frombuffer(data, np.int32)
# print(data.nbytes, numpy_data.nbytes)
times = []
s = time.time()
for i in range(100):
    s = time.time()
    ans = data+data1    
    times.append(time.time()-s)

print(np.average(times))
print(ans)