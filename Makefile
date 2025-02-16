# Video Tools Project

This project provides tools for merging video files using FFmpeg and managing the process via a `Makefile`. It requires Python 3.10.16, FFmpeg, and a working `make` environment.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Makefile Hierarchy](#makefile-hierarchy)
6. [Troubleshooting](#troubleshooting)


---

## Prerequisites

Before using this project, ensure your system meets the following requirements:

1. **Python 3.10.16**:
   - Install `pyenv` to manage Python versions:
     ```bash
     brew install pyenv
     ```
   - Install Python 3.10.16:
     ```bash
     pyenv install 3.10.16
     ```
   - Set the local Python version to 3.10.16:
     ```bash
     pyenv local 3.10.16
     ```

2. **FFmpeg**:
   - Install FFmpeg using Homebrew:
     ```bash
     brew install ffmpeg
     ```

3. **Make**:
   - Ensure `make` is installed (usually pre-installed on macOS and Linux).

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/video-tools.git
   cd video-tools
   ```
2. Verify the Python version:
   ```bash
   python --version
   ```
   This should output Python 3.10.16.

3. Verify FFmpeg is installed:
   ```bash
   ffmpeg -version
   ```

---

## Installation

Create a virtual environment and install dependencies:
```bash
make install
```
This will:
- Create a virtual environment in the `myenv` directory.
- Upgrade pip to the latest version.
- Install dependencies listed in `requirements.txt`.

---

## Usage

1. **Merge Video Files**  
   To merge video files, use the `merge_video_files` function in your Python script or interactive session. Ensure the input files are in the correct format and have consistent properties (e.g., frame rate, codec).

2. **Run Flask Development Server**  
   To run the Flask development server:
   ```bash
   make run
   ```

3. **Initialize the Database**  
   To initialize the SQLite database:
   ```bash
   make db_init
   ```

4. **Run Tests**  
   To run tests with coverage:
   ```bash
   make test
   ```

5. **Clean Up**  
   To remove temporary files, caches, and the virtual environment:
   ```bash
   make clean
   ```

---

## Makefile Hierarchy

The Makefile provides the following targets:

### Variables

```makefile
VENV_DIR := myenv
PYTHON := $(shell pyenv which python)
PIP := $(VENV_DIR)/bin/pip3
FLASK := $(VENV_DIR)/bin/flask
PYTEST := $(VENV_DIR)/bin/pytest
```

### Commands

- **install**  
  Creates a virtual environment using Python 3.10.16, upgrades pip, and installs dependencies from `requirements.txt`.
  ```bash
  make install
  ```

- **db_init**  
  Initializes the SQLite database and runs Flask migrations to set up the database schema.
  ```bash
  make db_init
  ```

- **run**  
  Starts the Flask development server.
  ```bash
  make run
  ```

- **test**  
  Runs tests with coverage using pytest.
  ```bash
  make test
  ```

- **clean**  
  Removes the virtual environment (`myenv`), deletes Python cache files (`*.pyc`, `__pycache__`), removes the database (`app.db`) and migrations folder, and cleans up the `file_object_storage` directory.
  ```bash
  make clean
  ```

---

## Troubleshooting

1. **make install Fails**  
   Ensure pyenv is installed and Python 3.10.16 is set as the local version:
   ```bash
   pyenv versions
   pyenv local 3.10.16
   ```

2. **FFmpeg Command Not Found**  
   Install FFmpeg using Homebrew:
   ```bash
   brew install ffmpeg
   ```

3. **Virtual Environment Not Using Correct Python Version**  
   Ensure the `PYTHON` variable in the Makefile points to the correct Python binary:
   ```bash
   $(shell pyenv which python)
   ```

4. **Database Initialization Fails**  
   Ensure Flask is installed and the `FLASK_APP` environment variable is set correctly in the Makefile.

---
