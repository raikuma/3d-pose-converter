import numpy as np

from structure import Intrinsic, Extrinsic

def parse(input):
    poses_bounds = np.load(input)
    poses = poses_bounds[:, :-2].reshape(-1, 3, 5)
    bounds = poses_bounds[:, -2:]
    R = poses[:, :, :3]
    t = poses[:, :, 3:4]
    hwf = poses[:, :, 4:5]

    # Rotation colnums (-Y, X, Z) -> (X, -Y, -Z)
    R = np.concatenate([R[:, :, 1:2], R[:, :, 0:1], -R[:, :, 2:3]], axis=2)

    height, width, focal = hwf[0].reshape(3)

    intrinsic = Intrinsic(width, height, focal)
    extrinsics = [
        Extrinsic(pos, rot)
        for pos, rot in zip(t, R)
    ]

    return intrinsic, extrinsics, {}

def dump(data, output):
    intrinsic, extrinsics, extra = data
    try:
        bounds = extra['bounds']
    except:
        bounds = np.zeros((len(extrinsics), 2))

    R = np.concatenate([extrinsic.R.reshape(1, 3, 3) for extrinsic in extrinsics], axis=0)
    t = np.concatenate([extrinsic.t.reshape(1, 3, 1) for extrinsic in extrinsics], axis=0)
    hwf = np.array([intrinsic.height, intrinsic.width, intrinsic.fx]).reshape(1, 3, 1).repeat(len(extrinsics), axis=0)

    # Rotation colnums (X, -Y, -Z) -> (-Y, X, Z)
    R = np.concatenate([R[:, :, 1:2], R[:, :, 0:1], -R[:, :, 2:3]], axis=2)

    poses = np.concatenate([R, t, hwf], axis=2).reshape(-1, 15)
    poses_bounds = np.concatenate([poses, bounds], axis=1)
    np.save(output, poses_bounds)