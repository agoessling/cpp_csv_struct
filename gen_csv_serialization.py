import argparse

import CppHeaderParser


def get_header_function(struct):
  namespace = f'{struct["namespace"]}::' if struct['namespace'] else ''
  type_name = f'{namespace}{struct["name"]}'

  s = f'''\
template <>
void CsvHeader(
    std::ostream& stream, const std::string& name, const {type_name}& data, bool trailing_comma) {{
'''

  num_prop = len(struct['properties']['public'])
  for i, member in enumerate(struct['properties']['public']):
    comma = 'true' if i < num_prop - 1 else 'trailing_comma'
    s += f'  CsvHeader('
    s += f'stream, name + "/{member["name"]}", data.{member["name"]}, {comma});\n'

  s += '}'

  return s


def get_serialization_function(struct):
  namespace = f'{struct["namespace"]}::' if struct['namespace'] else ''
  type_name = f'{namespace}{struct["name"]}'

  s = f'''\
template <>
void CsvSerialize(
    std::ostream& stream, const {type_name}& data, bool trailing_comma) {{
'''

  num_prop = len(struct['properties']['public'])
  for i, member in enumerate(struct['properties']['public']):
    comma = 'true' if i < num_prop - 1 else 'trailing_comma'
    s += f'  CsvSerialize(stream, data.{member["name"]}, {comma});\n'

  s += '}'

  return s


def get_header_header(inputs, primitives):
  s = ''
  s += '#pragma once\n\n'

  for f in inputs + primitives:
    s += f'#include "{f}"\n'

  return s[:-1]


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

  s = get_header_header(args.input, args.primitives)

  for input_file in args.input:
    header = CppHeaderParser.CppHeader(input_file)

    if args.debug:
      print(header.toJSON())

    structs = []
    for struct in header.classes.values():
      for base in struct['inherits']:
        if base['class'] == 'CsvSerializable':
          structs.append(struct)

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
