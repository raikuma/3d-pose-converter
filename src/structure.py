import numpy as np

class Intrinsic:
    def __init__(self, width, height, focal, principal_point=None, skew=0):
        self.width = width
        self.height = height
        self.focal = focal
        try:
            self.fx, self.fy = focal
        except:
            self.fx, self.fy = focal, focal
        if principal_point is None:
            self.principal_point = (width / 2, height / 2)
        else:
            self.principal_point = principal_point
        self.skew = skew

    @property
    def cx(self):
        return self.principal_point[0]
    
    @property
    def cy(self):
        return self.principal_point[1]

    @property
    def K(self):
        return np.array([
            [self.fx, self.skew, self.cx],
            [0, self.fy, self.cy],
            [0, 0, 1]], dtype=np.float32)
    
    def __str__(self):
        return 'Intrinsic(width={}, height={}, focal={}, principal_point={}, skew={})'.format(
            self.width, self.height, self.focal, self.principal_point, self.skew)

class Extrinsic:
    # Camera-to-World
    # Camera space: +X, -Y, -Z
    # World space: +X, -Y, -Z

    def __init__(self, t, R):
        self.t = np.array(t, dtype=np.float32).reshape(3, 1)
        self.R = np.array(R, dtype=np.float32)

    @property
    def c2w(self):
        bottom = np.array([[0, 0, 0, 1]], dtype=np.float32)
        c2w = np.concatenate([self.R, self.t], axis=1)
        c2w = np.concatenate([c2w, bottom], axis=0)
        return c2w
    
    @property
    def w2c(self):
        return np.linalg.inv(self.c2w)
    
    def __str__(self):
        return 'Extrinsic(t={}, R={})'.format(self.t, self.R)
    
class Bound:
    def __init__(self, near, far):
        self.near = far
        self.near = far

    def __str__(self):
        return 'Bound(near={}, far={})'.format(self.near, self.far)
