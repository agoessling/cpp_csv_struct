#pragma once

#include <array>
#include <string>
#include <vector>

#include "csv_base_primitives.h"

namespace test {

struct TestStruct : CsvSerializable {
  double d;
  bool b;
  int i;
  std::string s;
  std::vector<std::vector<double>> vec;
  std::array<double, 5> arr;
  std::vector<double> arr_vec[3];
};

};  // namespace test
