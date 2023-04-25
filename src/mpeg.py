import json

import numpy as np

from .structure import Intrinsic, Extrinsic

def parse(input):
    data = json.load(open(input, 'r'))

    cameras = []
    for name in data['sourceCameraNames']:
        camera = [c for c in data['cameras'] if c['Name'] == name][0]
        cameras.append(camera)

    resolution = cameras[0]['Resolution']
    width, height = resolution
    focal = cameras[0]['Focal']
    cx, cy = cameras[0]['Principle_point'] # it's typo on dataset

    intrinsic = Intrinsic(width, height, focal, (cx, cy))

    extrinsics = []
    for camera in cameras:
        eular_angles = camera['Rotation']
        R = eular2rotmat(eular_angles)
        t = np.array(camera['Position'])
        extrinsics.append(Extrinsic(t, R))

    return intrinsic, extrinsics, {}

def eular2rotmat_(rotation):
    yaw, pitch, roll = rotation
    yaw = np.deg2rad(yaw)
    pitch = np.deg2rad(pitch)
    roll = np.deg2rad(roll)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    Ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    R = Rz @ Ry @ Rx
    return R

def eular2rotmat(rotation):
    yaw, pitch, roll = rotation
    yaw = np.deg2rad(yaw)
    pitch = np.deg2rad(pitch)
    roll = np.deg2rad(roll)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)]
    ])

    Ry = np.array([
        [np.cos(-yaw), 0, np.sin(-yaw)],
        [0, 1, 0],
        [-np.sin(-yaw), 0, np.cos(-yaw)]
    ])

    Rz = np.array([
        [np.cos(-roll), -np.sin(-roll), 0],
        [np.sin(-roll), np.cos(-roll), 0],
        [0, 0, 1]
    ])

    R = Rz @ Ry @ Rx
    return R