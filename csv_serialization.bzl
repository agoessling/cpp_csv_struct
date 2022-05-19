def csv_serialization(name, srcs, primitives = None, **kwargs):
    if not primitives:
      primitives = []

    primitives.append("@cpp_csv_struct//:csv_base_primitives.h")

    header_locations = " ".join(["$(location {})".format(h) for h in srcs])
    primitive_locations = " ".join(["$(location {})".format(p) for p in primitives])

    cmd = "$(location @cpp_csv_struct//:gen_csv_serialization) -i {} -o $@ -p {}".format(
        header_locations, primitive_locations);

    native.genrule(
        name = name + "_gen",
        srcs = srcs + primitives,
        outs = [name + ".h"],
        tools = ["@cpp_csv_struct//:gen_csv_serialization"],
        cmd = cmd,
    )

    native.cc_library(
        name = name,
        srcs = primitives,
        hdrs = [name + ".h"],
        **kwargs
    )
