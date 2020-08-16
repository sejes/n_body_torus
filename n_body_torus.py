import ctypes
import numpy as np
import matplotlib.animation
import matplotlib.pyplot as plt


class NBody:
    _lib = ctypes.cdll.LoadLibrary('n_body.dll')
    _lib.nbody_torus.restype = None
    _lib.nbody_torus.argtypes = [
        ctypes.c_int,
        ctypes.c_float,
        ctypes.c_float,
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        np.ctypeslib.ndpointer(dtype=np.float32),
        ctypes.c_float,
        ctypes.c_float,
    ]
    _lib.wrap.restype = ctypes.c_float
    _lib.wrap.argtypes = [
        ctypes.c_float,
        ctypes.c_float,
    ]

    def __init__(self, g, m, p, v, w, h):
        self._g = g
        self._m = np.array(m, dtype=np.float32, order='C')
        self._px, self._py = np.array(np.transpose(p), dtype=np.float32, order='C')
        self._vx, self._vy = np.array(np.transpose(v), dtype=np.float32, order='C')
        self._w = w
        self._h = h
        self._n = len(m)
        for arr in self._px, self._py, self._vx, self._vy:
            if arr.shape != (self._n,):
                raise ValueError
        for i in range(self._n):
            self._px[i] = self._lib.wrap(self._px[i], w)
            self._py[i] = self._lib.wrap(self._py[i], h)

    def step(self, dt):
        self._lib.nbody_torus(
            self._n,
            dt,
            self._g,
            self._m,
            self._px, self._py,
            self._vx, self._vy,
            self._w,
            self._h
        )

    def animate(self, dt, steps_per_frame, fps):
        fig, ax = plt.subplots()
        ln, = plt.plot([], [], 'ko', markersize=0.5)

        def fn(_):
            for _ in range(steps_per_frame):
                self.step(dt)
            ln.set_data(self._px, self._py)
            return ln,

        plt.axis('scaled')
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_xlim(0, self._w)
        ax.set_ylim(0, self._h)

        # Must assign to variable otherwise destroyed by garbage collector
        _ = matplotlib.animation.FuncAnimation(fig, fn, interval=1e3 / fps)
        plt.show()
