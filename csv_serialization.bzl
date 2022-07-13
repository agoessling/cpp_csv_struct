def _csv_serialization_impl(ctx):
    dep_cc_infos = []
    headers = []
    primitives = []

    primitives += ctx.attr._base_primitives[CcInfo].compilation_context.direct_public_headers

    for src in ctx.attr.inputs:
        dep_cc_infos.append(src[CcInfo])
        headers += src[CcInfo].compilation_context.direct_public_headers

    for primitive in ctx.attr.primitives:
        dep_cc_infos.append(primitive[CcInfo])
        primitives += primitive[CcInfo].compilation_context.direct_public_headers

    output = ctx.actions.declare_file("{}.h".format(ctx.label.name))

    args = ctx.actions.args()
    args.add_all("-i", headers)
    args.add("-o", output)
    args.add_all("-p", primitives)

    ctx.actions.run(
        outputs = [output],
        inputs = headers,
        executable = ctx.attr._gen_csv_serialization.files_to_run,
        arguments = [args],
        mnemonic = "GenCsvSerialization",
        progress_message = "Generating CSV serialization",
    )

    output_depset = depset([output])

    cc_info = CcInfo(
        compilation_context = cc_common.create_compilation_context(headers = output_depset)
    )

    return [
        DefaultInfo(files = output_depset),
        cc_common.merge_cc_infos(
            direct_cc_infos = [cc_info],
            cc_infos = dep_cc_infos,
        ),
    ]


csv_serialization = rule(
    implementation = _csv_serialization_impl,
    doc = "Generate struct CSV serialization library.",
    attrs = {
        "inputs": attr.label_list(
            doc = "Libraries with structs to serialize.",
            providers = [CcInfo],
            mandatory = True,
        ),
        "primitives": attr.label_list(
            doc = "Primitive serialization template headers.",
            providers = [CcInfo],
        ),
        "_gen_csv_serialization": attr.label(
            doc = "CSV serialization generation script.",
            default = Label("@cpp_csv_struct//:gen_csv_serialization"),
            executable = True,
            cfg = "exec",
        ),
        "_base_primitives": attr.label(
            doc = "Base CSV serialization primitives.",
            default = Label("@cpp_csv_struct//:csv_base_primitives"),
        ),
    },
)
