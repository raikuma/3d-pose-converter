# 3D Pose Converter

## Usage

Convert

```
python convert.py INPUT OUTPUT [--input-format INPUT_FORMAT] [--output-format OUTPUT_FORMAT]
```

Visualize

For visualize, it require open3d package.

```
pip install open3d
```

```
python visualize.py INPUT [--input-format INPUT_FORMAT]
```

It supports (not bounds yet)

- COLMAP (sparse)
- LLFF, NeRF (poses_bounds.npy)

TODO

- bounds support
- Instant-NGP, NerfStudio (transforms.json)
- Kubric (metadata.json)
- custom

## World-to-Camera, Camera-to-World

X-to-Y: Move some position represented in X space to Y space

- Camera position in world space: $p$
- Translation vector: $t$
- Rotation matrix: $R$

### World-to-Camera (w2c)

$$Rp+t=\vec{\mathbf{0}}$$
$$p=-R^{-1}t$$

when R is orthogonal,

$$R^{-1}=R^T$$
$$\therefore p=-R^{T}t$$

### Camera-to-World (c2w)

$$R\vec{\mathbf{0}}+t=p$$
$$\therefore p=t$$

## Specification

All poses should be considered with **camera space** and **world space**.
Basically right-hand coordinate system (right-up-forward) is used in this repo.

![coordinate_system.png](https://www.scratchapixel.com/images//geometry/geo-lh-vs-rh-coordsys.png)

Focal lengths are represented by pixel unit.

For inner implementation, it uses

- Camera space: +X, -Y, -Z 
- World space: +X, -Y, -Z 

### COLMAP (sparse) [Reference](https://colmap.github.io/format.html)

- Camera space: +X, -Y, -Z
- World space: +X, -Y, -Z

It consists of 3 txt files.

**cameras.txt**

Intrinsic of cameras. In monocular camera setting, only one camera exists.

```
# Camera list with one line of data per camera:
#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
# Number of cameras: 3
1 SIMPLE_PINHOLE 3072 2304 2559.81 1536 1152
2 PINHOLE 3072 2304 2560.56 2560.56 1536 1152
3 SIMPLE_RADIAL 3072 2304 2559.69 1536 1152 -0.0218531
```

**images.txt**

Extrinsic of cameras. World-to-Camera.

```
Image list with two lines of data per image:
#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
#   POINTS2D[] as (X, Y, POINT3D_ID)
# Number of images: 2, mean observations per image: 2
1 0.851773 0.0165051 0.503764 -0.142941 -0.737434 1.02973 3.74354 1 P1180141.JPG
2362.39 248.498 58396 1784.7 268.254 59027 1784.7 268.254 -1
2 0.851773 0.0165051 0.503764 -0.142941 -0.737434 1.02973 3.74354 1 P1180142.JPG
1190.83 663.957 23056 1258.77 640.354 59070
```

**points3D.txt** (optional)

```
# 3D point list with one line of data per point:
#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)
# Number of points: 3, mean track length: 3.3334
63390 1.67241 0.292931 0.609726 115 121 122 1.33927 16 6542 15 7345 6 6714 14 7227
63376 2.01848 0.108877 -0.0260841 102 209 250 1.73449 16 6519 15 7322 14 7212 8 3991
63371 1.71102 0.28566 0.53475 245 251 249 0.612829 118 4140 117 4473
```

### LLFF, NeRF (poses_bounds.npy) [Reference](https://github.com/Fyusion/LLFF#using-your-own-poses-without-running-colmap)

- Camera space: -Y, +X, -Z
- World space: +X, -Y, -Z

**poses_bounds.npy**

Camera parameters and bounds. Camera-to-World.

It has n x 17 matrices. (n=number of images)
