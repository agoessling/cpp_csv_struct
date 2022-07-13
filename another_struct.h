#pragma once

#include "another_header.h"
#include "csv_base_primitives.h"

namespace test {

struct SubStruct : CsvSerializable {
  int i;
};

};  // namespace test
