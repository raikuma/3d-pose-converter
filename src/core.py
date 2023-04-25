import os

from . import colmap
from . import llff
from . import mpeg

def parse(input, input_format=None):
    if input_format is None:
        if os.path.isdir(input):
            input_format = 'colmap'
        elif input.endswith('.npy'):
            input_format = 'llff'
        else:
            raise ValueError('Unknown input format')
    print('Parsing input file from', input, 'with format', input_format)

    # sparse
    if input_format == 'colmap':
        return colmap.parse(input)
    # poses_bounds.npy
    if input_format == 'llff':
        return llff.parse(input)
    # mpeg
    if input_format == 'mpeg':
        return mpeg.parse(input)
    
    raise ValueError('Unknown input format')

def dump(data, output, output_format=None):
    print('Dumping data to', output, 'with format', output_format)

    # sparse
    if output_format == 'colmap':
        colmap.dump(data, output)
        return
    # poses_bounds.npy
    if output_format == 'llff':
        llff.dump(data, output)
        return

    raise ValueError('Unknown output format')