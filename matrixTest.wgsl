// Define the size of the matrices
let int kMatrixSize = 4;

// Define the matrices as input and output bindings
[[block]]
struct Matrix {
  values: array<vec4<f32>, kMatrixSize>;
};
[[binding(0), group(0)]] var<uniform> A: Matrix;
[[binding(1), group(0)]] var<uniform> B: Matrix;
[[binding(2), group(0)]] var<out> C: Matrix;

// Main function
[[stage(vertex)]]
fn main() -> void {
  // Multiply matrices A and B and store the result in C
  for (var i : u32 = 0u; i < kMatrixSize; i = i + 1u) {
    for (var j : u32 = 0u; j < kMatrixSize; j = j + 1u) {
      var sum: f32 = 0.0;
      for (var k : u32 = 0u; k < kMatrixSize; k = k + 1u) {
        sum = sum + A.values[i][k] * B.values[k][j];
      }
      C.values[i][j] = vec4<f32>(sum, sum, sum, sum);
    }
  }
}