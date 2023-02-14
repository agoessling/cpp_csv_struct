import argparse

import CppHeaderParser


def get_header_function_declaration(type_name):
  return f'''\
template <>
inline void CsvHeader(std::ostream& stream,
                      const std::string& name,
                      const {type_name}& data,
                      bool trailing_comma)'''


def get_serialization_function_declaration(type_name):
  return f'''\
template <>
inline void CsvSerialize(std::ostream& stream,
                         const {type_name}& data,
                         bool data_present,
                         bool trailing_comma)'''


def get_header_function(struct):
  s = f'{get_header_function_declaration(qualified_struct_type(struct))} {{\n'

  num_prop = len(struct['properties']['public'])
  for i, member in enumerate(struct['properties']['public']):
    comma = 'true' if i < num_prop - 1 else 'trailing_comma'
    s += f'  CsvHeader('
    s += f'stream, name + "/{member["name"]}", data.{member["name"]}, {comma});\n'

  s += '}'

  return s


def get_serialization_function(struct):
  s = f'{get_serialization_function_declaration(qualified_struct_type(struct))} {{\n'

  num_prop = len(struct['properties']['public'])
  for i, member in enumerate(struct['properties']['public']):
    comma = 'true' if i < num_prop - 1 else 'trailing_comma'
    s += f'  CsvSerialize(stream, data.{member["name"]}, data_present, {comma});\n'

  s += '}'

  return s


def get_header_header(inputs, primitives):
  s = ''
  s += '#pragma once\n'

  for f in inputs:
    s += f'\n#include "{f}"'

  s += '\n'

  for f in primitives:
    s += f'\n#include "{f}"'

  return s


def qualified_struct_type(struct):
  namespace = f'{struct["namespace"]}::' if struct['namespace'] else ''
  return f'{namespace}{struct["name"]}'


def qualified_member_type(member):
  namespace = f'{member["namespace"]}' if member['namespace'] else ''
  return f'{namespace}{member["type"]}'


def main():
  parser = argparse.ArgumentParser(
      description="Create serialization functions from struct definitions.")
  parser.add_argument('-i', '--input', required=True, nargs='+', help='Input header file(s).')
  parser.add_argument('-o', '--output', help='Output header file.')
  parser.add_argument('-p', '--primitives', nargs='+', default=[],
      help='CSV primitive serialization header file(s).')
  parser.add_argument('-d', '--debug', action='store_true',
      help='Print details from parsed header files.')

  args = parser.parse_args()

  structs = []
  for input_file in args.input:
    header = CppHeaderParser.CppHeader(input_file)

    if args.debug:
      print(header.toJSON())

    for struct in header.classes.values():
      for base in struct['inherits']:
        if base['class'] == 'CsvSerializable':
          structs.append(struct)

  s = get_header_header(args.input, args.primitives)

  for struct in structs:
    s += '\n\n'
    s += f'{get_header_function_declaration(qualified_struct_type(struct))};'
    s += '\n\n'
    s += f'{get_serialization_function_declaration(qualified_struct_type(struct))};'

  for struct in structs:
    s += '\n\n'
    s += get_header_function(struct)
    s += '\n\n'
    s += get_serialization_function(struct)

  if args.output:
    with open(args.output, 'w') as f:
      f.write(s)


if __name__ == '__main__':
  main()
