from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import statsmodels.api as sm

# Load the video file
video = VideoFileClip('Metronomes1.mp4')

# Extract the audio from the video
audio = video.audio

# Convert audio to a numpy array
audio_data = audio.to_soundarray(fps=44100)

# Compute the time axis
time_axis = np.linspace(0, len(audio_data) / 44100, num=len(audio_data))

# Calculate the volume (RMS of the sound's waveform)
volume = np.sqrt(((audio_data**2).mean(axis=1)))

print("applying LOESS smoothening")
# Applying LOESS smoothening
lowess = sm.nonparametric.lowess
volume_smoothed = lowess(volume, time_axis, frac=0.2)[:, 1] # The frac parameter may need adjustment
print("applying LOESS smoothening done")

# Find peaks (ticks) in the smoothed volume
peaks, _ = find_peaks(volume_smoothed, height=np.mean(volume_smoothed) * 1.5)

# Calculate time differences between consecutive peaks
peak_times = time_axis[peaks]
time_differences = np.diff(peak_times)

# Plot volume over time
plt.figure(figsize=(12, 6))

# Plotting the original and smoothed volume waveform
plt.subplot(2, 1, 1)
plt.plot(time_axis, volume, label='Original')
plt.plot(time_axis, volume_smoothed, label='Smoothed', color='red')
plt.plot(peak_times, volume_smoothed[peaks], 'x')
plt.xlabel('Time (s)')
plt.ylabel('Volume')
plt.title('Sound Volume over Time with Peaks')
plt.legend()

# Plotting the time differences between peaks
plt.subplot(2, 1, 2)
plt.plot(peak_times[1:], time_differences, '-o')
plt.xlabel('Time (s)')
plt.ylabel('Time Period Between Ticks (s)')
plt.title('Time Period Between Subsequent Ticks')

plt.tight_layout()
plt.show()
