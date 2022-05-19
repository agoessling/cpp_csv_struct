#include <iostream>

#include "csv_serialization.h"
#include "struct_to_serialize.h"

int main() {
  CsvHeader<test::TestStruct>(std::cout, "test_struct", false);

  test::TestStruct test = {
    .d = 5.34,
    .b = true,
    .i = 442,
    .s = "Hello, World!"
  };

  std::cout << std::endl;

  CsvSerialize(std::cout, test, false);

  std::cout << std::endl;

  return 0;
}
