import argparse

import open3d as o3d
import open3d.visualization as vis

from core import parse

def visualize(input, input_format=None):
    data = parse(input, input_format)
    intrinsic, extrinsics = data[:2]

    print(intrinsic)

    # (X, -Y, -Z) -> (X, Y, Z)
    for extrinsic in extrinsics:
        extrinsic.t = -extrinsic.t

    geometries = []

    for i, extrinsic in enumerate(extrinsics):
        cube = o3d.geometry.TriangleMesh.create_box(0.1, 0.1, 0.1)
        cube.translate(extrinsic.t)
        geometries.append(cube)

    vis.draw(geometries)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('--input-format', help='Input file format')
    args = parser.parse_args()
    visualize(args.input, args.input_format)