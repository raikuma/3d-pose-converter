import argparse

from core import parse, dump

def convert(input, output, input_format=None, output_format=None):
    data = parse(input, input_format)
    dump(data, output, output_format)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output file')
    parser.add_argument('--input-format', help='Input file format')
    parser.add_argument('--output-format', help='Output file format')
    args = parser.parse_args()
    convert(args.input, args.output, args.input_format, args.output_format)