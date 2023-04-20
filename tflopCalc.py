import time
from wgpu.utils import compute_with_buffers
import numpy as np
import wgpu
import wgpu.backends.rs

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
# data = data.astype(np.float16)
# data1 = data1.astype(np.float16)

print(data)
numpy_data = np.frombuffer(data, np.float16)

s = time.time()
cnt = 0
while time.time()<=s+4:
    out = compute_with_buffers({0: data, 1: data1}, {2: numpy_data.nbytes}, code)
    # ans = data+data1
    cnt = cnt + 24

print(cnt)
print(cnt/4)