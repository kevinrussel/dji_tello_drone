# Tello Drone UDP Command Receiver

This is the **drone-side companion service** to the hand-gesture controller project. It runs on a machine connected to a DJI Tello drone, listens for binary UDP command packets on the network, and translates them into real flight commands using the [`djitellopy`](https://github.com/damiafuentes/DJITelloPy) library.


<img src="README_docs/takeoff.gif" alt="Demo"  height="300">

Together with the gesture-tracking client, the full pipeline looks like:

```
Webcam + Hand Gestures  --(UDP packets)-->  This Service  --(djitellopy API)-->  DJI Tello Drone
```
<img src="README_docs/landing.gif" alt="Demo"  height="300">

<img src="README_docs/moving.gif" alt="Demo"  height="300">


---

## Project Structure

```
.
├── main.py   # Production receiver: listens for UDP commands and drives the Tello
└── test.py   # Standalone test scripts that simulate a client sending flight commands
```

---

## `main.py` — Command Receiver

Defines the `tello_class`, which runs two concurrent responsibilities:



1. **UDP listener** (`worker`) — binds a UDP socket to port `8080` with a 4 MB receive buffer, and continuously listens for incoming packets. Each packet is unpacked and, if its timestamp is newer than the last processed command, pushed onto a thread-safe `queue.Queue`.
2. **Command executor** (`drone_commands`) — runs on the main thread, pulling commands off the queue one at a time and issuing the corresponding Tello SDK call:

   | Command Type | Action |
   |---|---|
   | `t` | Takeoff (only triggered once, guarded by `takeoff_initiated`) |
   | `l` | Land |
   | `m` | Send RC control command — applies `command_speed` to the vertical (up/down) axis via `send_rc_control(0, 0, command_speed, 0)` |

   Movement commands are only processed **after** takeoff has been initiated.

### Key methods

- **`__init__`** — connects to the Tello, opens and binds the UDP socket on port `8080`, and initializes state (`last_known_time`, `takeoff_initiated`).
- **`worker()`** — runs in a background daemon thread; receives raw UDP packets, decodes them, and enqueues valid (newer) commands.
- **`deal_with_packet(message)`** — unpacks the binary payload using `struct.unpack("!Qch", message)` into `(timestamp, command_type, command_speed)`, decoding the command type byte into a string.
- **`drone_commands()`** — the main consumer loop that pulls from the queue and drives the drone via `djitellopy`.
- **`start_drone()`** — establishes/re-establishes the Tello connection.
- **`main()`** — entry point: starts the UDP listener thread, connects to the drone, and enters the command execution loop.

---

## `test.py` — Manual Test Client

A standalone script (independent of `main.py`) for manually exercising the UDP protocol without needing the full hand-gesture pipeline. It builds and sends the same binary packet format directly to the drone's listening address (`192.168.10.2:8080`).

### `create_header(flag)`

Builds a UDP packet for a given command flag (`"takeoff"`, `"land"`, `"up"`, or default `"down"`), packing a timestamp, command-type byte, and a hardcoded speed value (`60` for takeoff/up, `-60` for down) using `struct.pack('!Qch', ...)`.

### Test routines

- **`test1_takeoff()`** — sends a takeoff command, waits 5 seconds, then sends a land command.
- **`test2_altitude()`** — sends takeoff, waits 10 seconds, then sends a sequence of up/down movement commands with delays between each, finishing with land.
- **`test3_up_and_down()`** — sends takeoff, then loops 29 times sending alternating up/down commands every 3 iterations with a 0.5 second delay between each, finishing with land. This simulates a sustained back-and-forth altitude oscillation.

At the bottom of the file, `test3_up_and_down()` is the active call (the other two are commented out), so running the script executes that test by default.

---

## UDP Packet Format

Both `main.py` and `test.py` use the same binary protocol as the hand-gesture client:

```
struct.pack('!Qch', timestamp, command_type, movement_speed)
```

| Field | Type | Description |
|---|---|---|
| `timestamp` | `Q` (unsigned long long, 8 bytes) | Nanosecond timestamp (`time.time_ns()`) |
| `command_type` | `c` (char, 1 byte) | `b't'` = takeoff, `b'l'` = land, `b'm'` = move |
| `movement_speed` | `h` (short, 2 bytes) | Signed vertical speed, e.g. `-80` to `80` |

All fields are packed in network byte order (`!`).

---

## Requirements

- Python 3.x
- [`djitellopy`](https://pypi.org/project/djitellopy/)
- A DJI Tello drone, connected to the same Wi-Fi network as the host machine

Install dependencies:

```bash
pip install djitellopy
```

---

## Usage

### Running the receiver

```bash
python main.py
```

This connects to the Tello, opens a UDP listener on port `8080`, and waits for incoming command packets (e.g. from the hand-gesture controller).

### Running a manual test

Edit `test.py` to uncomment the desired test function at the bottom of the file, then run:

```bash
python test.py
```

Make sure `server_address` in `test.py` matches the IP address of the machine running `main.py`, and that `main.py` is already running and listening before the test script sends commands.

---

## Notes

- Takeoff is only ever triggered **once** per session (`takeoff_initiated`), preventing duplicate takeoff commands from repeated packets.
- Movement (`m`) commands are ignored until takeoff has completed.
- The UDP listener uses an enlarged 4 MB socket receive buffer to reduce the chance of dropped packets under load.
- `main.py` and `test.py` are independent entry points — `test.py` is meant for manually validating the UDP protocol and drone response, not for production use alongside the real gesture client.

## Disclaimer

This project issues live flight commands to a physical drone. Always test in a large, open, obstacle-free area, keep the drone within line of sight, and be ready to take manual control at any time.