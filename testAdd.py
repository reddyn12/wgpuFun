import numpy as np
import time

times = []
a = 5
b = 15
c =0
for i in range(100):
    s = time.time()
    c = a + b
    
    times.append(time.time()-s)

print(np.average(times))
