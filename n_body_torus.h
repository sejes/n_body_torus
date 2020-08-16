#pragma once

__declspec(dllexport) void nbody_torus(
  int n_bodies,
  float dt,
  float g,
  float* m,
  float* px,
  float* py,
  float* vx,
  float* vy,
  float w,
  float h);
__declspec(dllexport) float wrap(float x, float m);
float signed_modulo_distance(float x, float y, float m);
