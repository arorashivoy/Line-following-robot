# Line-following robot

A Raspberry Pi robot with two driven wheels and a five-sensor line array, built as
IIIT-Delhi robotics coursework in late 2024. It runs in two modes: driven by hand
from a joystick in a browser, or following a line on its own under closed-loop
control.

> A GIF of the robot following the line, and a screenshot of the joystick page,
> belong here.

## Hardware

Driven with [gpiozero](https://gpiozero.readthedocs.io). All pins are **BCM**
numbering.

| | Pin |
|---|---|
| Left motor — forward / backward / enable | 7, 8, 25 |
| Right motor — forward / backward / enable | 10, 9, 11 |
| Line sensors `S1`–`S5`, left to right | 17, 18, 27, 22, 23 |

Both motors are `Motor(..., pwm=True)` and paired into a gpiozero `Robot`, so
steering is done by scaling one wheel rather than by a servo.

## Autonomous mode — `main_pid.py`

The five sensors read **0 when they see the line** and 1 when they do not. The error
term weights them by how far off-centre they sit:

```python
error = ((not s1) * -1 + (not s2) * -1 + (not s3) * 0 + (not s4) * 1 + (not s5) * 1)
```

So the error runs from −2 (line hard left) through 0 (centred under `S3`) to +2
(line hard right). It is a coarse, discrete signal — five bits in, five possible
positions — which is the real constraint on how smoothly this can be driven.

That error feeds a `simple-pid` controller, whose output is clamped to [−1, 1] and
applied as `curve_left` / `curve_right` on `robot.forward()`. When all five sensors
read 1 — no line anywhere — the robot stops.

**The gains are `Kp = 0.5`, `Ki = 1`, `Kd = 0`.** Two things worth saying plainly
rather than letting the filename imply otherwise:

- **With `Kd = 0` this is a PI controller, not PID.** There is no derivative term.
- `Ki` is twice `Kp`. Integral action that strong on a discrete error signal will
  wind up through any gap in the line, which is the first thing to look at if the
  robot oscillates.

```sh
python3 main_pid.py
```

`main.py` is the earlier version of the same loop without the controller — it
reacts to the sensor pattern directly.

## Joystick mode — `api.py`

A FastAPI server that serves `index.html` and exposes two endpoints the page calls
as you drag the on-screen stick:

| Route | Does |
|---|---|
| `GET /move/{x}/{y}/{angle}` | translate a joystick vector into per-wheel speeds |
| `GET /rotate/{clockwise}` | turn in place |

```sh
pip install fastapi uvicorn gpiozero simple-pid
uvicorn api:app --host 0.0.0.0 --port 8000
```

Then open the Pi's address on port 8000 from a phone on the same network. Binding
to `0.0.0.0` is what makes that work — and also means anything on the network can
drive the robot, so keep it off untrusted networks.

`gpiozero` only imports on the Pi; none of this runs on a laptop.
