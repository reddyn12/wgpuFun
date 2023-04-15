import wgpu
import wgpu.backends.rs
import numpy as np

from wgpu.utils import compute_with_buffers
adapter:wgpu.GPUAdapter = wgpu.request_adapter(canvas=None, power_preference="high-performance")
device = adapter.request_device(required_limits=None)


# print(adapter, device, adapter.request_adapter_info(), adapter.limits)

with open('matrixTest.wgsl', 'r') as f:
    shader_code = f.read()

# shader_module = device.create_shader_module(code=shader_code)


A = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0], [9.0, 10.0, 11.0, 12.0], [13.0, 14.0, 15.0, 16.0]]
B = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
C = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]

# Create buffers for the input and output matrices
a_buffer = device.create_buffer_with_data(data=np.array(A), usage =1)
b_buffer = device.create_buffer_with_data(data=np.array(B), usage = 1)
c_buffer = device.create_buffer_with_data(data=np.array(C), usage = 2)


t = compute_with_buffers({0:a_buffer,1:b_buffer}, C, shader_code)
# Bind the input and output buffers to the shader module using bind groups
# bind_group_layout = device.create_bind_group_layout(entries=[
#   wgpu.Binding(layout=0, buffer=a_buffer),
#   wgpu.Binding(layout=1, buffer=b_buffer),
#   wgpu.Binding(layout=2, buffer=c_buffer, writable=True)
# ])
# bind_group = device.create_bind_group(layout=bind_group_layout, entries=[
#   wgpu.Binding(layout=0, buffer=a_buffer),
#   wgpu.Binding(layout=1, buffer=b_buffer),
#   wgpu.Binding(layout=2, buffer=c_buffer, writable=True)
# ])