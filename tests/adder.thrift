package easyrpc.tests.adder

service Service {
  i32 addTwo(1: i32 a, 2: i32 b);
  i32 addThree(1: i32 a, 2: i32 b, 3: i32 c);
}
