Simple Voice Recorder
=====================

A simple desktop application for recording audio from your computer's microphone and saving it as an MP3 file. The application features a clean graphical user interface built with Python and PyQt5.

Features
--------

-   **Easy to Use:** One-click recording and stopping.

-   **Real-time Feedback:** A timer displays the duration of the current recording.

-   **MP3 Format:** Saves audio directly to the universally compatible MP3 format.

-   **Cross-Platform:** Runs on Windows, macOS, and Linux.

Requirements
------------

Before you begin, ensure you have the following installed on your system:

1.  **Python:** Version 3.6 or newer.

2.  **FFmpeg:** A crucial backend tool for processing and saving the audio as an MP3.

3.  **Python Libraries:**

    -   `PyQt5`

    -   `sounddevice`

    -   `numpy`

    -   `scipy`

Installation Guide
------------------

Follow these steps to get the application running on your machine.

### Step 1: Install Python

If you don't already have Python, download it from the official website.

-   **Website:**  [python.org](https://www.python.org/downloads/ "null")

-   **Important (for Windows users):** During installation, make sure to check the box that says **"Add Python to PATH"**.

### Step 2: Install Required Libraries

Open your computer's command line interface (`cmd` on Windows, `Terminal` on macOS/Linux) and run the following command to install the necessary Python packages:

```
pip install PyQt5 sounddevice numpy scipy

```

### Step 3: Install FFmpeg

This application cannot save MP3 files without FFmpeg.

-   **On Windows:**

    1.  Go to the [FFmpeg downloads page](https://www.gyan.dev/ffmpeg/builds/ "null") and download the "essentials" build.

    2.  Unzip the downloaded file into a permanent folder, for example, `C:\ffmpeg`.

    3.  Add the `bin` sub-folder to your system's PATH environment variable (e.g., `C:\ffmpeg\bin`).

-   **On macOS (using Homebrew):**

    ```
    brew install ffmpeg

    ```

-   **On Linux (using apt for Debian/Ubuntu):**

    ```
    sudo apt-get install ffmpeg

    ```

### Step 4: Download and Run the Application

1.  Save the Python code as a file named `voice_recorder.py`.

2.  Navigate to the file's location in your terminal.

3.  Run the application with the following command:

```
python voice_recorder.py

```

How to Use
----------

1.  Launch the application by running the `voice_recorder.py` script.

2.  Click the **Record** button to begin recording audio from your default microphone.

3.  The timer will show the elapsed recording time.

4.  Click the **Stop & Save** button to end the recording.

5.  A file dialog will open, allowing you to name your file and choose where to save the MP3.