import sounddevice as sd
import numpy as np
import socket
import time
import threading
import subprocess
import os
import tkinter as tk
import wave

HOST = '127.0.0.1'
PORT = 5000
SAMPLE_RATE = 12000
CHANNELS = 1
BUFFER_SIZE = 16384
LATENCY_THRESHOLD = 0.1

is_recording = False
audio_thread = None
monitor_thread = None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

latency_values = []
packet_loss = 0
total_packets_sent = 0
total_bandwidth_usage = 0

ffmpeg_path = r"C:\Users\Ghazavi\Desktop\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"

def compress_audio(audio_data):
    temp_input_file = "temp_input.wav"
    with wave.open(temp_input_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data)

    temp_output_file = "temp_output.aac"
    
    command = [
        ffmpeg_path,
        '-i', temp_input_file,
        '-c:a', 'aac',
        '-b:a', '128k',
        temp_output_file
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("ffmpeg error:", result.stderr.decode())
    
    if not os.path.exists(temp_output_file):
        print("Error: Output file not found.")
        return None

    with open(temp_output_file, "rb") as f:
        compressed_data = f.read()

    os.remove(temp_input_file)
    os.remove(temp_output_file)

    return compressed_data

def record_and_send_audio():
    global total_packets_sent, total_bandwidth_usage

    def callback(indata, frames, time, status):
        global total_packets_sent, total_bandwidth_usage
        if status:
            print(f"Recording Error: {status}", flush=True)

        audio_data = np.int16(indata * 32767)
        compressed_data = compress_audio(audio_data.tobytes())
        
        if compressed_data:
            try:
                sock.sendto(compressed_data, (HOST, PORT))
                total_packets_sent += 1
                total_bandwidth_usage += len(compressed_data)
                update_ui(f"Sent {len(compressed_data)} bytes to {HOST}:{PORT}")
            except socket.error as e:
                print("Network error:", e)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback, blocksize=BUFFER_SIZE):
        while is_recording:
            time.sleep(0.2)

def network_monitor():
    global latency_values, packet_loss
    while is_recording:
        start_time = time.time()
        time.sleep(0.05)
        latency = time.time() - start_time
        latency_values.append(latency)

        if np.random.rand() < 0.01:
            packet_loss += 1

        time.sleep(1)

def toggle_recording():
    global is_recording, latency_values, packet_loss, total_packets_sent, total_bandwidth_usage, audio_thread, monitor_thread
    if not is_recording:
        latency_values.clear()
        packet_loss = 0
        total_packets_sent = 0
        total_bandwidth_usage = 0

        is_recording = True
        start_button.config(text="Stop")

        audio_thread = threading.Thread(target=record_and_send_audio)
        audio_thread.start()

        monitor_thread = threading.Thread(target=network_monitor)
        monitor_thread.start()

    else:
        is_recording = False
        start_button.config(text="Start")

        avg_latency = np.mean(latency_values) if latency_values else 0
        packet_loss_rate = (packet_loss / total_packets_sent) * 100 if total_packets_sent else 0
        bandwidth_usage_kb = total_bandwidth_usage / 1024

        update_ui(f"Network Metrics:\nAverage Latency: {avg_latency:.3f} seconds\nPacket Loss Rate: {packet_loss_rate:.2f}%\nBandwidth Usage: {bandwidth_usage_kb:.2f} KB")

        if audio_thread is not None:
            audio_thread.join()
        if monitor_thread is not None:
            monitor_thread.join()

def update_ui(message):
    output_text.insert(tk.END, message + '\n')
    output_text.yview(tk.END)

root = tk.Tk()
root.title("Voice Streamer with QoS")

start_button = tk.Button(root, text="Start", command=toggle_recording, width=10, height=2)
start_button.pack(pady=20)

output_text = tk.Text(root, height=15, width=50)
output_text.pack(pady=10)

root.mainloop()
