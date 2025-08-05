import sys
import os
import subprocess
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, QTime, Qt

class VoiceRecorderApp(QWidget):
    def __init__(self):
        super().__init__()

        # --- App State ---
        self.is_recording = False
        self.recorded_frames = []
        self.samplerate = 44100  # Standard sample rate for audio
        self.channels = 1        # Mono recording
        self.timer = QTimer(self)
        self.time = QTime(0, 0, 0)

        # --- UI Initialization ---
        self.initUI()

    def initUI(self):
        """Sets up the graphical user interface."""
        self.setWindowTitle('Voice Recorder')
        self.setGeometry(300, 300, 400, 200) # x, y, width, height

        # --- Layout ---
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Status Label ---
        self.status_label = QLabel('Press "Record" to start recording.', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #333;")
        
        # --- Timer Label ---
        self.timer_label = QLabel('00:00:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #555;")
        self.timer_label.hide() # Hidden until recording starts

        # --- Buttons ---
        self.record_button = QPushButton('Record', self)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f; 
                color: white; 
                font-size: 18px; 
                font-weight: bold;
                padding: 12px; 
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        
        self.stop_button = QPushButton('Stop & Save', self)
        self.stop_button.setEnabled(False) # Disabled by default
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #5bc0de; 
                color: white; 
                font-size: 18px; 
                font-weight: bold;
                padding: 12px; 
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #46b8da;
            }
            QPushButton:disabled {
                background-color: #999;
            }
        """)

        # --- Event Connections ---
        self.record_button.clicked.connect(self.toggle_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.timer.timeout.connect(self.update_timer)

        # --- Assembling the Layout ---
        layout.addWidget(self.status_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.record_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def toggle_recording(self):
        """Starts the recording process."""
        if self.is_recording:
            return 
            
        self.is_recording = True
        self.recorded_frames = [] # Clear previous recording
        
        # Update UI
        self.status_label.setText('Recording...')
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.record_button.setStyleSheet("background-color: #999;") # Gray out record button
        
        # Start timer
        self.time.setHMS(0,0,0)
        self.timer_label.setText('00:00:00')
        self.timer_label.show()
        self.timer.start(1000) # Update every second

        # Start the audio stream
        try:
            self.stream = sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                callback=self.audio_callback,
                dtype='int16'
            )
            self.stream.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not start recording. Make sure a microphone is connected.\n\nDetails: {e}")
            self.reset_ui()


    def audio_callback(self, indata, frames, time, status):
        """This function is called for each audio block from the microphone."""
        if status:
            print(status, file=sys.stderr)
        self.recorded_frames.append(indata.copy())

    def stop_recording(self):
        """Stops the recording and handles file saving."""
        if not self.is_recording:
            return

        # Stop stream and timer
        self.stream.stop()
        self.stream.close()
        self.timer.stop()
        
        # Save the file
        self.save_file()
        
        # Reset UI to initial state
        self.reset_ui()

    def save_file(self):
        """Saves the recorded audio by converting a temporary WAV file to MP3 using FFmpeg."""
        if not self.recorded_frames:
            QMessageBox.warning(self, "Warning", "No audio was recorded.")
            return

        recording = np.concatenate(self.recorded_frames, axis=0)
        
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Recording', 'recording.mp3', 'MP3 Files (*.mp3)')

        if file_path:
            # Ensure the filename ends with .mp3
            if not file_path.lower().endswith('.mp3'):
                file_path += '.mp3'
                
            temp_wav_path = "temp_recording.wav"
            try:
                # 1. Save as a temporary WAV file
                wav.write(temp_wav_path, self.samplerate, recording)

                # 2. Construct and run the FFmpeg command to convert WAV to MP3
                command = [
                    'ffmpeg',
                    '-i', temp_wav_path,   # Input file
                    '-y',                  # Overwrite output file if it exists
                    '-vn',                 # No video
                    '-ar', str(self.samplerate), # Audio sample rate
                    '-ac', str(self.channels),   # Audio channels
                    '-b:a', '192k',        # Audio bitrate
                    file_path              # Output file
                ]
                
                # Execute the command, hiding the console window on Windows
                subprocess.run(command, check=True, capture_output=True, text=True)

                QMessageBox.information(self, "Success", f"Recording saved successfully to:\n{file_path}")

            except FileNotFoundError:
                 QMessageBox.critical(self, "Error", "FFmpeg not found. Please ensure FFmpeg is installed and in your system's PATH.")
            except subprocess.CalledProcessError as e:
                # This error occurs if ffmpeg returns a non-zero exit code
                QMessageBox.critical(self, "Error", f"Failed to convert the file using FFmpeg.\n\nFFmpeg error:\n{e.stderr}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An unexpected error occurred.\n\nDetails: {e}")
            finally:
                # 3. Clean up the temporary WAV file
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)

    def reset_ui(self):
        """Resets the UI to its initial state after stopping or an error."""
        self.is_recording = False
        self.status_label.setText('Press "Record" to start recording.')
        self.timer_label.hide()
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Restore original button styles
        self.record_button.setStyleSheet("""
            QPushButton { background-color: #d9534f; color: white; font-size: 18px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #c9302c; }
        """)

    def update_timer(self):
        """Updates the timer display every second."""
        self.time = self.time.addSecs(1)
        self.timer_label.setText(self.time.toString('hh:mm:ss'))
        
    def closeEvent(self, event):
        """Ensures the audio stream is closed when the app window is closed."""
        if self.is_recording:
            self.stream.stop()
            self.stream.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    ex = VoiceRecorderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
