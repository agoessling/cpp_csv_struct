#pragma once

#include <array>
#include <ostream>
#include <sstream>
#include <string>
#include <type_traits>
#include <vector>

struct CsvSerializable {};

namespace {

template <typename T>
struct is_indexable_container : std::false_type {};

template <typename U, size_t N>
struct is_indexable_container<std::array<U, N>> : std::true_type {};

template <typename U>
struct is_indexable_container<std::vector<U>> : std::true_type {};

template <typename T>
using is_array_like = std::disjunction<is_indexable_container<T>,
                                       std::is_array<T>>;

template <typename T>
size_t GetSize(const T& array_like) {
  if constexpr(is_indexable_container<T>::value) {
    return array_like.size();
  }

  if constexpr(std::is_array<T>::value) {
    return std::extent<T>::value;
  }
}

};  // namespace

template <class T>
void CsvHeader(std::ostream& stream, const std::string& name, const T& data, bool trailing_comma) {
  // Array like.
  if constexpr(::is_array_like<T>::value) {
    const size_t len = ::GetSize(data);
    for (size_t i = 0; i < len; ++i) {
      std::stringstream full_name;
      full_name << name << "[" << i << "]";
      bool comma = i < len - 1 ? true : trailing_comma;
      CsvHeader(stream, full_name.str(), data[i], comma);
    }
    return;
  }

  // Everything else.
  if constexpr(!::is_array_like<T>::value) {
    (void)data;
    stream << name;
    if (trailing_comma) stream << ",";
    return;
  }
}

template <class T>
void CsvSerialize(std::ostream& stream, const T& data, bool data_present, bool trailing_comma) {
  // Array like.
  if constexpr(::is_array_like<T>::value) {
    const size_t len = ::GetSize(data);
    for (size_t i = 0; i < len; ++i) {
      bool comma = i < len - 1 ? true : trailing_comma;
      CsvSerialize(stream, data[i], data_present, comma);
    }
    return;
  }

  // Everything else.
  if constexpr(!::is_array_like<T>::value) {
    if (data_present) stream << data;
    if (trailing_comma) stream << ",";
    return;
  }
}

template <>
inline void CsvSerialize(std::ostream& stream, const std::string& data, bool data_present, bool trailing_comma) {
  if (data_present) stream << "\"" << data << "\"";
  if (trailing_comma) stream << ",";
}
