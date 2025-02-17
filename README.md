# Video Tools Project

This project provides tools for merging video files using FFmpeg and managing the process . It requires Python 3.10.16, FFmpeg, and a working `make` environment.

---

# Note
Temporary DB ( app.db ) is committed to the code if you want to have a look , make sure you delete it `rm -rf app/app.db` before starting the setup.

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
4. Make local storage folder: 
   ```bash
   mkdir file_object_storage
   ```
5. Create the .env file and tweak the variables if needed
   ```bash
   cp .env.dist .env
   ```

---

## Installation

Create a virtual environment and install dependencies:
Enter you virtual environment name in the make file. 
```bash
make install
```
This will:
- Create a virtual environment in the `your_env` directory.
- Upgrade pip to the latest version.
- Install dependencies listed in `requirements.txt`.

---

## Usage


1. **Initialize the Database**  
   To initialize the SQLite database:
   ```bash
   make db_init
   ```
1. **Switch to virtual env**  
   To initialize the SQLite database:
   ```bash
   source <venv-name>/bin/activate
   ```

2. **Run Flask Development Server**  
   To run the Flask development server:
   ```bash
   make run
   ```

3. **Run Tests**  
   To run tests with coverage:
   ```bash
   make test
   ```

4. **Clean Up**  
   To remove temporary files, caches, and the virtual environment:
   ```bash
   make clean
   ```

---

## Makefile Hierarchy

The Makefile provides the following targets:

- **install**  
  Creates a virtual environment using Python 3.10.16. Upgrades pip and installs dependencies from `requirements.txt`.

- **db_init**  
  Initializes the SQLite database and runs Flask migrations to set up the database schema.

- **run**  
  Starts the Flask development server.

- **test**  
  Runs tests with coverage using pytest.

- **clean**  
  Removes the virtual environment (`myenv`), deletes Python cache files (`*.pyc`, `__pycache__`), removes the database (`app.db`) and migrations folder, and cleans up the `file_object_storage` directory.

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


