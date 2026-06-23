# Physics Sandbox

A 2D physics sandbox built in Python and pygame. Balls fall under gravity, bounce off the walls, slide to a stop with friction, and can be grabbed and flung with the mouse. A quadtree spatial structure keeps collision detection fast as the number of balls grows.

<img width="1006" height="828" alt="demo2" src="https://github.com/user-attachments/assets/9b60d438-39cd-4d05-a27f-4e8743f8e952" />




## Features

- Gravity with wall bounces and adjustable energy retention
- Friction that brings sliding balls to a smooth stop
- Grab-and-throw. Click a ball and fling it, throw speed depends on mouse motion

## How it works

Each ball is an object that tracks its position, velocity, mass, and radius. Every frame the simulation steps forward with Euler integration: gravity updates each ball's velocity, and velocity updates its position. Wall and ball collisions reflect those velocities.

Checking every pair of balls each frame grows as O(n²), which falls apart with a lot of balls. To avoid that, the collision step uses a quadtree, recursively subdivides space, packing detail where balls actually cluster, so each ball is only compared against the handful of others nearby.

## Usage
```
pip install pygame
python Engine.py
```

## Built with
- Python
- pygame

## Roadmap
- [x] finish the quadtree based collision
- [x] varied ball sizes
- [x] momentum conserving collision response

## LICENSE 
Released under MIT license
