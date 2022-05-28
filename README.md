# cpp_csv_struct

Automatic CSV serialization from C++ structures.

## Usage

### WORKSPACE

To incorporate `cpp_csv_struct` into your project copy the following into your `WORKSPACE` file.

```Starlark
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "cpp_csv_struct",
    # See release page for latest version url and sha.
)

load("@cpp_csv_struct//:cpp_csv_struct_first_level_deps.bzl", "cpp_csv_struct_first_level_deps")
cpp_csv_struct_first_level_deps()

load("@cpp_csv_struct//:cpp_csv_struct_second_level_deps.bzl", "cpp_csv_struct_second_level_deps")
cpp_csv_struct_second_level_deps()
```
