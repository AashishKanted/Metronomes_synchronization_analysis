from moviepy.editor import VideoFileClip
import numpy as np
from scipy.signal import find_peaks
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt

# Load the video file
video = VideoFileClip('data\\M2.mp4')

# Extract the audio from the video
audio = video.audio

# Convert audio to a numpy array
audio_data = audio.to_soundarray(fps=44100)

# Compute the time axis
time_axis = np.linspace(0, len(audio_data) / 44100, num=len(audio_data))

# Calculate the volume (RMS of the sound's waveform)
volume = np.sqrt(((audio_data**2).mean(axis=1)))

# Create a figure and subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 6))

# Plotting the original volume waveform
axs[0].plot(time_axis, volume)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Volume')
axs[0].set_title('Sound Volume over Time with Peaks')

# Plotting the time differences between peaks
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Time Period Between Ticks (s)')

# Initialize height and distance parameters
initial_height = np.mean(volume) * 14
initial_distance = 1

# Create sliders for height and distance
ax_height = plt.axes([0.15, 0.05, 0.65, 0.03])
ax_distance = plt.axes([0.15, 0.01, 0.65, 0.03])
slider_height = Slider(ax_height, 'Height', 0, np.max(volume), valinit=initial_height)
slider_distance = Slider(ax_distance, 'Distance', 0, len(time_axis)/50, valinit=initial_distance)

# Function to update the plot based on slider values
def update(val):
    # Get the current slider values
    height = slider_height.val
    distance = slider_distance.val
    
    # Find peaks (ticks) in the volume
    peaks, _ = find_peaks(volume, height=height, distance=distance)
    
    # Calculate time differences between consecutive peaks
    peak_times = time_axis[peaks]
    time_differences = np.diff(peak_times)
    
    # Clear the subplots
    axs[0].cla()
    axs[1].cla()
    
    # Plotting the original volume waveform
    axs[0].plot(time_axis, volume)
    axs[0].plot(peak_times, volume[peaks], 'x')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Volume')
    axs[0].set_title('Sound Volume over Time with Peaks')
    
    # Plotting the time differences between peaks
    axs[1].plot(peak_times[1:], time_differences, '-o')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Time Period Between Ticks (s)')
    
    # Update the plot
    fig.canvas.draw()

# Register the update function with the sliders
slider_height.on_changed(update)
slider_distance.on_changed(update)

# Show the plot
plt.show()

# Find peaks (ticks) in the volume
peaks, _ = find_peaks(volume, height=np.mean(volume) * 14,distance=1) # Adjust the threshold as needed


# Calculate time differences between consecutive peaks
peak_times = time_axis[peaks]
time_differences = np.diff(peak_times)

# Plot volume over time
plt.figure(figsize=(12, 6))

# Plotting the original volume waveform
plt.subplot(2, 1, 1)
plt.plot(time_axis, volume)
plt.plot(peak_times, volume[peaks], 'x')
plt.xlabel('Time (s)')
plt.ylabel('Volume')
plt.title('Sound Volume over Time with Peaks')

# Plotting the time differences between peaks
plt.subplot(2, 1, 2)
plt.plot(peak_times[1:], time_differences, '-o')
plt.xlabel('Time (s)')
plt.ylabel('Time Period Between Ticks (s)')
plt.title('Time Period Between Subsequent Ticks')

plt.tight_layout()
plt.show()
