#include <math.h>
#include <stdio.h>
#include "nbody.h"

void nbody_torus(
  int n_bodies,
  float dt,
  float g,
  float* m,
  float* px,
  float* py,
  float* vx,
  float* vy,
  float w,
  float h)
{
  for (int i = 0; i < n_bodies; i++) {
    float px_i = px[i];
    float py_i = py[i];
    float f_x = 0;
    float f_y = 0;
    for (int j = 0; j < n_bodies; j++) {
      float r_x = signed_modulo_distance(px_i, px[j], w);
      float r_y = signed_modulo_distance(py_i, py[j], h);
      float d2 = r_x * r_x + r_y * r_y;
      if (d2 > 1e-2) {
        float d = sqrtf(d2);
        float prop = g / (d * d2);
        f_x += r_x * prop;
        f_y += r_y * prop;
      }
    }
    float m_i = m[i];
    float a_x = f_x / m_i;
    float a_y = f_y / m_i;
    vx[i] += a_x * dt;
    vy[i] += a_y * dt;
  }
  for (int i = 0; i < n_bodies; i++) {
    px[i] = wrap(px[i] + vx[i] * dt, w);
    py[i] = wrap(py[i] + vy[i] * dt, h);
  }
}

static inline float signed_modulo_distance(float x, float y, float m)
{
  float s = y - x;
  float d = fabsf(s);
  if (d > m / 2) {
    s -= copysignf(m, s);
  }
  return s;
}

// https://stackoverflow.com/a/11980362
inline float wrap(float x, float m)
{
  return x - m * floorf(x / m);
}
