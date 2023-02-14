#include <iostream>
#include <vector>

#include "csv_serialization.h"
#include "struct_to_serialize.h"

int main() {
  test::TestStruct test = {
    .d = 5.34,
    .b = true,
    .i = 442,
    .s = "Hello, World!"
  };

  std::vector<double> inner{1, 2, 3};
  test.vec.push_back(inner);
  test.vec.push_back(inner);
  test.vec.push_back(inner);
  test.vec.push_back(inner);

  test.arr = {1,2,3,4,5};

  test.arr_vec[0] = inner;
  test.arr_vec[1] = inner;
  test.arr_vec[2] = inner;

  CsvHeader<test::TestStruct>(std::cout, "test_struct", test, false);

  std::cout << std::endl;

  CsvSerialize(std::cout, test, true, false);

  std::cout << std::endl;

  return 0;
}
