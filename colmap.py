import os

import numpy as np

from structure import Intrinsic, Extrinsic

def parse(input):
    camerasfile = os.path.join(input, 'cameras.txt')
    imagesfile = os.path.join(input, 'images.txt')
    pointsfile = os.path.join(input, 'points3D.txt')

    # cameras
    with open(camerasfile, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            camera_id, model, width, height, *params = line.split()
            width, height = map(float, (width, height))

            assert model in ['SIMPLE_PINHOLE',
                             'PINHOLE',
                             'SIMPLE_RADIAL']
            
            # https://github.com/colmap/colmap/blob/dev/src/base/camera_models.h
            if model == 'SIMPLE_PINHOLE':
                f, cx, cy = map(float, params)
                focal = f
            elif model == 'PINHOLE':
                fx, fy, cx, cy = map(float, params)
                focal = (fx, fy)
            elif model == 'SIMPLE_RADIAL':
                f, cx, cy, k1, k2 = map(float, params)
                focal = f

            break # only one camera

    intrinsic = Intrinsic(width, height, focal, (cx, cy))

    # images
    extrinsics = []
    lines = open(imagesfile, 'r').readlines()
    lines = [line for line in lines if line and not line.startswith('#')]
    for i in range(0, len(lines), 2):
        image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, name = lines[i].split()
        qw, qx, qy, qz, tx, ty, tz = map(float, (qw, qx, qy, qz, tx, ty, tz))
        potins2D = lines[i + 1].split()

        R = qvec2rotmat([qw, qx, qy, qz])
        t = np.array([[tx], [ty], [tz]], dtype=np.float32)
        bottom = np.array([[0, 0, 0, 1]], dtype=np.float32)
        w2c = np.concatenate([R, t], axis=1)
        w2c = np.concatenate([w2c, bottom], axis=0)

        c2w = np.linalg.inv(w2c)
        R = c2w[:3, :3]
        t = c2w[:3, 3]
        extrinsics.append(Extrinsic(t, R))

    return intrinsic, extrinsics, {}

def dump(data, output):
    intrinsic, extrinsics, extra = data

    os.makedirs(output, exist_ok=True)

    camerasfile = os.path.join(output, 'cameras.txt')
    imagesfile = os.path.join(output, 'images.txt')
    pointsfile = os.path.join(output, 'points3D.txt')

    # cameras
    with open(camerasfile, 'w') as f:
        f.write('# Camera list with one line of data per camera:\n')
        f.write('#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n')
        f.write('# Number of cameras: 1\n')

        f.write('1 PINHOLE {} {} {} {} {} {}\n'.format(
            intrinsic.width, intrinsic.height, intrinsic.fx, intrinsic.fy, intrinsic.cx, intrinsic.cy))

    # images
    with open(imagesfile, 'w') as f:
        f.write('# Image list with two lines of data per image:\n')
        f.write('#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n')
        f.write('#   POINTS2D[] as (X, Y, POINT3D_ID)\n')
        f.write('# Number of images: {0}, mean observations per image: {0}\n'.format(len(extrinsics)))

        for i, extrinsic in enumerate(extrinsics):
            w2c = extrinsic.w2c
            R = w2c[:3, :3]
            t = w2c[:3, 3].reshape(-1)
            qvec = rotmat2qvec(R)
            f.write('{} {} {} {} {} {} {} {} 1 {}\n'.format(
                i + 1, *qvec, *t, '{:03d}.jpg'.format(i)))
            f.write('\n')

    # points
    with open(pointsfile, 'w') as f:
        f.write('# 3D point list with one line of data per point:\n')
        f.write('#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n')
        f.write('# Number of points: 0, mean track length: 0\n')

def qvec2rotmat(qvec):
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

def rotmat2qvec(R):
    Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz, Rzz = R.flat
    K = np.array([
        [Rxx - Ryy - Rzz, 0, 0, 0],
        [Ryx + Rxy, Ryy - Rxx - Rzz, 0, 0],
        [Rzx + Rxz, Rzy + Ryz, Rzz - Rxx - Ryy, 0],
        [Ryz - Rzy, Rzx - Rxz, Rxy - Ryx, Rxx + Ryy + Rzz]]) / 3.0
    eigvals, eigvecs = np.linalg.eigh(K)
    qvec = eigvecs[[3, 0, 1, 2], np.argmax(eigvals)]
    if qvec[0] < 0:
        qvec *= -1
    return qvec
