import wgpu
import wgpu.backends.rs
import numpy as np
import queue

#write a wgsl shader and python code to take in 2 matricies and multiplies them, assume the matricies are compatable

#wgsl code
wgsl_code = """
struct Matrix {
  x_col: vec4<f32>,
  y_col: vec4<f32>,
  z_col: vec4<f32>,
  w_col: vec4<f32>
};

@group(0) @binding(0)
var<uniform> matrixA: Matrix;

@group(0) @binding(1)
var<uniform> matrixB: Matrix;

@group(0) @binding(2)
var<storage, read_write> matrixC: Matrix;

@compute 
@workgroup_size(8, 8, 1)
fn main(@builtin(global_invocation_id) GlobalInvocationID : vec3<i32>) {
  var row: i32 = GlobalInvocationID.x;
  var col: i32 = GlobalInvocationID.y;
  var index: i32 = row * 4 + col;
  matrixC[index] = matrixA[index] * matrixB[index];
}

        """

# wgsl_code = """
# struct Matrix4x4 {
#   row0: vec4<f32>;
#   row1: vec4<f32>;
#   row2: vec4<f32>;
#   row3: vec4<f32>;
# };

# [[block]]
# struct MatrixBlock {
#   matrixA: Matrix4x4;
#   matrixB: Matrix4x4;
#   matrixC: Matrix4x4;
# };

# [[binding(0), group(0)]] var<uniform> matrixBlock: MatrixBlock;

# [[stage(compute), workgroup_size(1)]]
# fn main() {
#   let index: u32 = gl_GlobalInvocationID.x;
#   let row: u32 = index / 4u;
#   let col: u32 = index % 4u;

#   let a_row: vec4<f32> = match row {
#     0u => matrixBlock.matrixA.row0,
#     1u => matrixBlock.matrixA.row1,
#     2u => matrixBlock.matrixA.row2,
#     3u => matrixBlock.matrixA.row3,
#     _ => vec4<f32>(0.0, 0.0, 0.0, 0.0),
#   };

#   let b_col: vec4<f32> = match col {
#     0u => matrixBlock.matrixB.row0,
#     1u => matrixBlock.matrixB.row1,
#     2u => matrixBlock.matrixB.row2,
#     3u => matrixBlock.matrixB.row3,
#     _ => vec4<f32>(0.0, 0.0, 0.0, 0.0),
#   };

#   let dot_product: f32 = dot(a_row, b_col);

#   let c_row: vec4<f32> = match row {
#     0u => &matrixBlock.matrixC.row0,
#     1u => &matrixBlock.matrixC.row1,
#     2u => &matrixBlock.matrixC.row2,
#     3u => &matrixBlock.matrixC.row3,
#     _ => &vec4<f32>(0.0, 0.0, 0.0, 0.0),
#   };

#   let c_new_value: f32 = match col {
#     0u => dot_product,
#     1u => dot_product,
#     2u => dot_product,
#     3u => dot_product,
#     _ => 0.0,
#   };

#   store(c_new_value, c_row[col]);
# }
# """
#python code

matrixA = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])

matrixB = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])

matrixC = np.zeros((4, 4))
#create a wgpu device

adapter:wgpu.GPUAdapter = wgpu.request_adapter(canvas=None, power_preference="high-performance")
device = adapter.request_device(required_limits=None)

#create a shader module

shader_module = device.create_shader_module(code = wgsl_code)

#create a bind group

bind_group = device.create_bind_group(
    layout=shader_module.get_bind_group_layout(0),
    entries=[
        wgpu.BindGroupEntry(binding=0, resource=wgpu.BindingResource.from_buffer(matrixA.astype(np.float32))),
        wgpu.BindGroupEntry(binding=1, resource=wgpu.BindingResource.from_buffer(matrixB.astype(np.float32))),
        wgpu.BindGroupEntry(binding=2, resource=wgpu.BindingResource.from_buffer(matrixC.astype(np.float32)))
        ]
        )

#create a compute pipeline 

compute_pipeline = device.create_compute_pipeline(
    layout=device.create_pipeline_layout(
        bind_group_layouts=[shader_module.get_bind_group_layout(0)]
        ),
        compute_stage={
            'module': shader_module,
            'entry_point': 'main'
            }
            )

#create a command encoder

command_encoder = device.create_command_encoder()

#create a compute pass

compute_pass = command_encoder.begin_compute_pass()

compute_pass.set_pipeline(compute_pipeline)

compute_pass.set_bind_group(0, bind_group)

compute_pass.dispatch(4, 4, 1)

#create a render pass

render_pass = command_encoder.begin_render_pass()

render_pass.set_pipeline(compute_pipeline)

render_pass.set_bind_group(0, bind_group)

render_pass.draw(4, 4, 1)

#create a command buffer

command_buffer = command_encoder.finish()

#submit the command buffer

queue.submit([command_buffer])

#print the result

print(np.array(matrixC))