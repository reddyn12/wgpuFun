import wgpu
import numpy as np
from wgpu.utils import compute_with_buffers
import wgpu.backends.rs
import time
code = '''
@group(0) @binding(0)
var<storage,read> data1: array<i32>;
@group(0) @binding(1)
var<storage,read> data2: array<i32>;
@group(0) @binding(2)
var<storage,read_write> out: array<i32>;

@compute
@workgroup_size(1)
fn main(@builtin(global_invocation_id) index: vec3<u32>) {
    let i: u32 = index.x;
    out[i] = data1[i] + data2[i];
}

'''

data = np.array([[1,2,3,4,5,6,67,7,8,8,8,9],[1,2,3,4,5,6,67,7,8,8,8,9]])
data1 = np.array([[1,2,3,4,5,6,67,7,8,8,8,9],[1,2,3,4,5,6,67,7,8,8,8,9]])


numpy_data = np.frombuffer(data, np.int32)
# print(data.nbytes, numpy_data.nbytes)
times = []
s = time.time()
for i in range(100):
    s = time.time()
    
    out = compute_with_buffers({0: data, 1: data1}, {2: numpy_data.nbytes}, code)
    times.append(time.time()-s)

print(np.average(times))
# result = np.frombuffer(out[2], dtype=np.int32)
# print(result)
# print(data)
# result.shape = (2,12)
# print(result)
# print(out[2].tolist())
