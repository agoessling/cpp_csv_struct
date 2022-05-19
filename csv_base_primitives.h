#pragma once

#include <ostream>
#include <string>

struct CsvSerializable {};

template <class T>
void CsvHeader(std::ostream& stream, const std::string& name, bool trailing_comma) {
  stream << name;
  if (trailing_comma) stream << ",";
}

template <class T>
void CsvSerialize(std::ostream& stream, const T& data, bool trailing_comma) {
  stream << data;
  if (trailing_comma) stream << ",";
}

template <>
void CsvSerialize<std::string>(std::ostream& stream, const std::string& data, bool trailing_comma) {
  stream << "\"" << data << "\"";
  if (trailing_comma) stream << ",";
}
