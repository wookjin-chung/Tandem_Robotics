# Tandem_Robotics

Tandem_Robotics is an educational robotics project utilizing Micro:bit and Arduino Uno. This repository provides libraries, example code, and comprehensive educational materials for controlling robots on both platforms.

## Table of Contents
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
  - [Micro:bit](#microbit)
    - [Using the Pre‑built HEX Files](#using-the-pre-built-hex-files)
  - [Arduino Uno](#arduino-uno)
- [Educational Materials](#educational-materials)
- [Usage Examples](#usage-examples)
- [License](#license)
- [Contact](#contact)

## Features
- **Micro:bit Library**: Provides various descendant libraries including `microbit_abot.py`.
- **Arduino Library**: Offers `MicroAbot.zip` file and example sketch (`microbit_abot.ino`).
- **Diverse Practice Examples**: Includes numerous Python examples that are easy for beginners to follow.
- **Comprehensive Educational Materials**: Provides `Python for Tandem Robotics: An Integrated Approach` PDF.
- **Open Source**: An open‑source project that anyone can freely use and contribute to.

## Directory Structure
```text
Tandem_Robotics/
├── README.md
├── LICENSE
├── .gitignore
├── microbit/
│   ├── libraries/
│   │   ├── microbit_abot.py
│   │   ├── abot_straight_calibrate.py
│   │   ├── abot_rotation_calibrate.py
│   │   ├── abot_calibrated.py
│   │   └── ultrasonic.py
│   └── examples/
│       ├── ch01_hello_microbit.py
│       ├── ch2_01_variables_display.py
│       ├── … …
│       └── ch7_19_distributed_dance_sequence.py
├── arduino/
│   ├── MicroAbot.zip
│   └── MicroAbot/
│       ├── library.properties
│       ├── src/
│       │   ├── MicroAbot.cpp
│       │   └── MicroAbot.h
│       └── examples/
│           ├── microbit_abot/
│           │   └── microbit_abot.ino
│           ├── ch3_01_i2c_text_communication/
│           │   └── ch3_01_i2c_text_communication.ino
│           ├── ch3_02_i2c_numeric_communication/
│           │   └── ch3_02_i2c_numeric_communication.ino
│           └── ch3_03_i2c_acceleration_data_transfer/
│               └── ch3_03_i2c_acceleration_data_transfer.ino
├── docs/
│   └── educational_materials/
│       └── Python_for_Tandem_Robotics.pdf
└── assets/
    ├── images/
    │   ├── Logo_tandem_robotics.png
    │   ├── Logo_tandem_robotics_inv.png
    │   ├── Tandem_robot.png
    │   ├── microbit_abot_board.png
    │   └── … …
    └── ZIP/
        └── python_examples_hex.zip
```

## Installation

### Micro:bit
1. **Library‑based approach (all board versions)**
   1. Upload every `.py` file from `microbit/libraries/` to your Micro:bit.
   2. Copy the example you want to run from `microbit/examples/` to the board and execute it.
   3. For detailed instructions, refer to the [Educational Materials](docs/educational_materials/Python_for_Tandem_Robotics.pdf).

2. ### Using the Pre‑built HEX Files
   If you are **only flashing a program** and do **not** need to edit the source, you can use the ready‑made HEX images.

   | Requirement | Details |
   |-------------|---------|
   | Compatible hardware | **Micro:bit V2.0 or later** *(V1 boards are **not** supported because the images contain MicroPython V2‑specific firmware blobs).* |
   | File bundle | `assets/ZIP/python_examples_hex.zip` |

   **Steps**
   1. Download `python_examples_hex.zip` from the `assets/ZIP/` folder (or from the latest Release assets).
   2. Extract the archive on your computer. It contains a HEX file for every example in `microbit/examples/`.
   3. Connect your Micro:bit (V2+) via USB. It appears as a drive named `MICROBIT`.
   4. Drag‑and‑drop the desired `.hex` file onto the drive. The board will flash itself and reboot directly into the example.

   *Tip: The HEX archive compresses all examples into a ~ 20 MB download, keeping the repository lightweight while still giving you plug‑and‑play images.*

### Arduino Uno
1. Download `arduino/MicroAbot.zip`.
2. Open the Arduino IDE and navigate to **Sketch ▸ Include Library ▸ Add .ZIP Library…** to install the package.
3. Open `arduino/MicroAbot/examples/microbit_abot/microbit_abot.ino` and upload it to your Arduino Uno.
4. See the [Educational Materials](docs/educational_materials/Python_for_Tandem_Robotics.pdf) for full instructions.

## Educational Materials
- **[Python for Tandem Robotics: An Integrated Approach](docs/educational_materials/Python_for_Tandem_Robotics.pdf)** – a comprehensive guide for learners and instructors.

## Usage Examples
- Browse the examples in `microbit/examples/` and `arduino/MicroAbot/examples/`.
- Each example is annotated to help you understand the concepts being demonstrated.

## License
This project is licensed under the **[MIT License](LICENSE)**.

## Contact
Have questions or suggestions? Please open an issue via the **[Issue Tracker](https://github.com/wookjin-chung/Tandem_Robotics/issues)**.
