import argparse

import open3d as o3d
import open3d.visualization as vis

from src.core import parse

def visualize(input, input_format=None, scale=1.0):
    data = parse(input, input_format)
    intrinsic, extrinsics = data[:2]

    print(intrinsic)

    # (X, -Y, -Z) -> (X, Y, Z)
    for extrinsic in extrinsics:
        # extrinsic.R[:, 1:3] *= -1
        # extrinsic.t[:, 1:3] = -extrinsic.t
        extrinsic.t *= scale

    print(len(extrinsics))

    geometries = []

    for i, extrinsic in enumerate(extrinsics):
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1)
        c2w = extrinsic.c2w
        axis.transform(c2w)
        geometries.append(axis)

    vis.draw(geometries)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('--input-format', help='Input file format')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale')
    args = parser.parse_args()
    visualize(args.input, args.input_format, args.scale)