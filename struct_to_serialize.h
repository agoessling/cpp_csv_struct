#pragma once

#include <string>

#include "csv_base_primitives.h"

namespace test {

struct TestStruct : CsvSerializable {
  double d;
  bool b;
  int i;
  std::string s;
};

};  // namespace test
