load("@rules_python//python:pip.bzl", "pip_install")

def cpp_csv_struct_second_level_deps():
    pip_install(
       name = "cpp_csv_struct_py_deps",
       requirements = "@cpp_csv_struct//:requirements.txt",
    )
