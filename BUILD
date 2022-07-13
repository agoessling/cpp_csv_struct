load("@cpp_csv_struct//:csv_serialization_rule.bzl", "csv_serialization")
load("@cpp_csv_struct_py_deps//:requirements.bzl", "requirement")

exports_files(["csv_base_primitives.h"])

cc_library(
    name = "csv_base_primitives",
    hdrs = ["csv_base_primitives.h"],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "struct_to_serialize",
    hdrs = ["struct_to_serialize.h"],
    deps = [
        ":csv_base_primitives",
    ],
)

cc_library(
    name = "another_struct",
    hdrs = ["another_struct.h"],
    deps = [
        ":another_header",
        ":csv_base_primitives",
    ],
)

cc_library(
    name = "another_header",
    hdrs = ["another_header.h"],
)

csv_serialization(
    name = "csv_serialization",
    inputs = [
        ":struct_to_serialize",
        ":another_struct",
    ],
)

cc_binary(
    name = "test_serialization",
    srcs = ["test_serialization.cc"],
    deps = [
        ":csv_serialization",
        ":struct_to_serialize",
    ],
)

py_binary(
    name = "gen_csv_serialization",
    srcs = ["gen_csv_serialization.py"],
    deps = [
        requirement("robotpy-cppheaderparser"),
    ],
    visibility = ["//visibility:public"],
)
