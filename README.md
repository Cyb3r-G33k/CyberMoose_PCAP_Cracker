
# CyberMooseHandShakeCracker  
*Created by Alex Losev*

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Supported GPUs](#supported-gpus)
7. [Logs and Results](#logs-and-results)
8. [Development Roadmap](#development-roadmap)
9. [Contributing](#contributing)
10. [License](#license)

---

## Introduction

**CyberMooseHandShakeCracker** is a Python-based tool designed to crack Wi-Fi handshakes from `.pcap` or `.cap` files using GPU acceleration (both NVIDIA and AMD). It provides an easy-to-use graphical user interface (GUI) to manage cracking operations and monitor progress. This tool is ideal for cybersecurity enthusiasts or penetration testers who want to test Wi-Fi network security effectively.

---

## Features

- **File Format Support:** Handles `.pcap` and `.cap` files.
- **GPU Acceleration:** Supports both NVIDIA and AMD GPUs for fast cracking.
- **Interactive GUI:** Provides an interface to select handshake files and view cracking progress.
- **Real-Time Progress Display:** Shows the current hash rate and estimated cracking time.
- **Random Brute Force Mode:** Option to perform random brute force attacks without generating a wordlist.
- **Logging:** Saves cracking results and operations to log files.
- **Save Results:** Cracked passwords are saved in a text file.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Cyb3r-G33k/CyberMoose_PCAP_Cracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure GPU drivers are installed:**  
   - For **NVIDIA**: Install [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit).
   - For **AMD**: Install [ROCm](https://rocm.docs.amd.com/en/latest/).

4. **Run the application**
   ```bash
   python main.py
   ```

---

## Usage

1. **Launch the application:**  
   Run `main.py` to open the GUI.

2. **Select a handshake file:**  
   Use the file picker in the GUI to choose a `.pcap` or `.cap` file.

3. **Start the cracking process:**  
   Click the **Start** button to begin the cracking operation.

4. **View progress:**  
   The progress bar and hash rate will update in real-time. If successful, the result will appear in a message box and be saved to a text file.

5. **Enable random brute force mode:**  
   Check the **Random Brute Force** option to use this mode without a predefined wordlist.

---

## Configuration

1. **Settings File:**  
   The `config.ini` file is auto-generated upon the first run. Use it to:
   - Set GPU preferences (NVIDIA/AMD).
   - Adjust the hashing algorithm if needed.
   - Specify output directories for logs and results.

2. **Brute Force Settings:**  
   Enable brute force mode through the settings panel or directly in the `config.ini` file.

---

## Supported GPUs

- **NVIDIA:** Requires CUDA support.
- **AMD:** Requires ROCm support.

Make sure your GPU drivers and libraries are installed and up to date to ensure proper functionality.

---

## Logs and Results

- **Logs:**  
  Logs are stored in the `/logs` directory with timestamps for each cracking session.

- **Results:**  
  Cracked passwords are saved in the `/results` directory as `.txt` files.

---

## Development Roadmap

- [x] Basic GUI functionality  
- [x] Support for `.pcap` and `.cap` files  
- [ ] Add multi-GPU support  
- [ ] Implement wordlist management  
- [ ] Add feature to import custom wordlists via GUI  
- [ ] Integrate with cloud services for distributed cracking  

---

## Contributing

We welcome contributions from the community! Follow these steps to contribute:

1. Fork the repository.  
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Added new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Create a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
