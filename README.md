# Hand Gesture Drone Controller

Kevin Russel

July/26/2026

A computer-vision system that lets you control a drone's altitude (takeoff, land, ascend, descend, hold) using a single hand gesture in front of a webcam. Hand tracking is powered by [MediaPipe](https://github.com/google-ai-edge/mediapipe) and [OpenCV](https://opencv.org/), and commands are streamed to the drone over UDP.

The core idea: the distance between your **thumb tip** and **index finger tip** is measured, converted into a 0–100% "throttle" value, and mapped to a drone command that's packed into a binary UDP packet and sent to the drone's onboard receiver.

---

## How It Works

1. **Hand detection** — `handtrackingmodule.py` wraps MediaPipe's Hands solution to detect up to two hands per frame and expose the (x, y) pixel coordinates of all 21 landmarks per hand.
2. **Gesture measurement** — `projecthand.py` reads landmark `4` (thumb tip) and landmark `8` (index tip) of the detected hand, and computes the Euclidean distance (hypotenuse) between them.
3. **Percentage mapping** — that distance is linearly interpolated from a `[30, 270]` pixel range into a `[0, 100]` percentage range, representing how "open" the pinch gesture is.
4. **Movement decision** — the percentage is translated into a drone command:

   | Percentage | Movement | Speed |
   |---|---|---|
   | `0` | `LAND` | `0` |
   | `1–40` | `DOWN` | interpolated `-80` to `-20` |
   | `40–60` | `HOLD` | `0` |
   | `60–99` | `UP` | interpolated `20` to `80` |
   | `100` | `TAKEOFF` | `60` (sent once) |

5. **Packet creation** — `create_header()` packs a binary UDP payload containing a nanosecond timestamp, a single-byte command type (`l` = land, `t` = takeoff, `m` = move), and the movement speed, using Python's `struct` module (`!Qch` format: unsigned long long, char, short).
6. **Transmission** — the packed header is sent via a UDP socket to the drone's configured IP address and port.
7. **Live visualization** — the current FPS, gesture percentage, movement state, a color-coded status label, and a vertical "throttle" bar are drawn onto the webcam feed in real time with OpenCV.

---

## Project Structure

```
.
├── handtrackingmodule.py   # Hand detection wrapper around MediaPipe Hands
└── projecthand.py          # Main application: gesture → command → UDP → drone
```

### `handtrackingmodule.py`

Defines the `handDetector` class, which encapsulates MediaPipe's hand-tracking pipeline:

- `findHands(image, draw)` — runs hand detection on a frame and optionally draws landmark connections on it.
- `findposition(image)` — returns pixel-coordinate landmark lists for up to two detected hands (`left_hand`, `right_hand`), each formatted as `[id, x, y]` per landmark.
- `draw_line(image, point1, point2)` — draws a line between two points (used to visualize the thumb-to-index gesture).
- Includes a standalone `main()` for testing the module on its own (prints landmark 4 and overlays an FPS counter).

### `projecthand.py`

Defines the `Hand_Drone` class, which is the main application entry point:

- **`__init__`** — configures the webcam capture (1000×1000), the `handDetector` instance, the drone's target UDP address/port, and the UDP socket.
- **`calculate_hypot`** — computes the pixel distance between two points.
- **`calculate_percentage`** — maps that distance to a 0–100 percentage.
- **`drone_move_down` / `drone_move_up`** — compute proportional descent/ascent speeds.
- **`drone_movement`** — decides the movement command and speed from the current percentage.
- **`create_header`** — builds the binary UDP packet sent to the drone.
- **`calculate_fps`** — tracks frames-per-second for on-screen display.
- **`image_on_screen`** — renders the live overlay (FPS, percentage, movement label, color-coded throttle bar).
- **`worker`** — the main loop: captures frames, runs detection, computes gestures, sends UDP commands, and renders the display.

---

## Requirements

- Python 3.x
- [OpenCV](https://pypi.org/project/opencv-python/) (`opencv-python`)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [NumPy](https://pypi.org/project/numpy/)
- A webcam
- A drone (or receiver) listening for UDP packets on the configured IP/port

Install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## Usage

1. Update the drone's target IP and port in `Hand_Drone.__init__`:

   ```python
   self.server_address = "192.168.10.2"
   self.port = 8080
   ```

2. Run the controller:

   ```bash
   python projecthand.py
   ```

3. Hold up **one hand** (with the other hand out of frame) in front of the webcam:
   - Pinch your thumb and index finger together fully → **LAND**
   - Keep them at a moderate distance → **HOLD**
   - Slightly open → **DOWN** (proportional descent speed)
   - More open → **UP** (proportional ascent speed)
   - Fully spread apart → **TAKEOFF** (sent once per session)

4. Press the webcam window's close controls or interrupt the process (`Ctrl+C`) to stop.

> **Note:** Gesture tracking only activates when exactly one hand (mapped internally as the "left" hand slot) is visible and the other hand slot is empty — this is an intentional single-hand control scheme.

---

## UDP Packet Format

Each command sent to the drone is packed with:

```
struct.pack('!Qch', timestamp, command_type, movement_speed)
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | `Q` (unsigned long long, 8 bytes) | Nanosecond timestamp (`time.time_ns()`) |
| `command_type` | `c` (char, 1 byte) | `b'l'` = land, `b't'` = takeoff, `b'm'` = move |
| `movement_speed` | `h` (short, 2 bytes) | Signed speed value, `-80` to `80` |

All values are packed in network byte order (`!`).

---

## On-Screen Display

While running, the live camera feed shows:

- **FPS counter** (top-left)
- **Gesture percentage** (0–100)
- **Movement label** (`HOLD`, `UP`, `DOWN`, `TAKEOFF`, `LAND`), color-coded:
  - Green — `HOLD`
  - Red — `UP`
  - Blue — `DOWN`
  - Yellow — `TAKEOFF` / `LAND`
- A **vertical throttle bar** that fills based on the current gesture percentage
- A **connecting line** drawn between the thumb tip and index fingertip

---

## Disclaimer

This project sends real movement commands over the network. Test thoroughly in a safe, open environment before flying an actual drone, and ensure a manual override/failsafe is always available.