### README.md

# Real-Time Audio Streaming with QoS Analysis

This project implements a real-time audio streaming system with network quality of service (QoS) monitoring. Using Python, the system records audio data on a client, compresses it with AAC codec, and transmits it to a server over UDP. The system monitors and displays network metrics such as latency, packet loss, and bandwidth usage through a graphical interface.

## Features

- **Real-Time Audio Streaming**: Captures audio input from a microphone, compresses it, and streams it over a network.
- **QoS Monitoring**: Tracks network latency, packet loss rate, and bandwidth usage.
- **AAC Audio Compression**: Uses `FFmpeg` to compress audio data, reducing the required bandwidth.
- **UDP Protocol**: Streams audio using the UDP protocol for low-latency transmission.
- **Graphical Interface**: Provides a simple GUI for both the client and server to monitor audio streaming status and network metrics.

## Requirements

To run this project, you will need:

- **Python 3.x** (preferably Python 3.12 or later)
- **sounddevice** for real-time audio recording
- **numpy** for data handling
- **FFmpeg** for audio compression
- **tkinter** for GUI
- **wave** for audio processing

### Installing Dependencies

Install required Python packages:

```bash
pip install sounddevice numpy tkinter
```

Download and install **FFmpeg** from the [official website](https://ffmpeg.org/download.html), and ensure it's added to your system's PATH.

## Project Structure

```
RealTime-Audio-Streaming/
├── client.py            # Client-side script for audio recording and streaming
├── server.py            # Server-side script to receive and display streamed data
├── README.md            # Project documentation
└── requirements.txt     # Dependencies file
```

## Usage

### 1. Running the Server

On the server machine (or terminal), run:

```bash
python server.py
```

This will start the UDP server, which will display incoming audio packet information and network metrics.

### 2. Running the Client

On the client machine, update `ffmpeg_path` in `client.py` to your local FFmpeg path. Then, run:

```bash
python client.py
```

A GUI will appear, where you can start and stop audio recording and streaming. The client captures audio from your device, compresses it to AAC, and streams it to the server.

## How It Works

### Client-Side
- **Audio Recording**: Captures real-time audio using `sounddevice`.
- **Audio Compression**: Compresses the captured audio into AAC format using FFmpeg.
- **Packet Transmission**: Sends compressed audio packets to the server over UDP.
- **QoS Metrics**: Tracks latency, packet loss, and bandwidth usage during transmission.

### Server-Side
- **Packet Reception**: Listens for incoming audio packets from the client.
- **GUI Display**: Shows received packet information, including the packet size and sender address.

## QoS Monitoring

### Metrics Calculated:
- **Latency**: Measures the round-trip time of audio packets.
- **Packet Loss**: Estimates the percentage of lost packets.
- **Bandwidth Usage**: Calculates the amount of data transmitted over the network.

These metrics are displayed on the client GUI to help analyze the audio streaming quality.

## Example Workflow

1. Start the server by running `server.py`.
2. Run `client.py` and click the "Start" button to begin streaming.
3. Monitor the network metrics in the client GUI to assess the performance.

## Future Improvements

- **Dynamic Bitrate Adjustment**: Adapt audio quality based on real-time network conditions.
- **Error Correction**: Implement mechanisms to handle packet loss and improve audio quality.
- **Multi-Client Support**: Allow multiple clients to stream to a single server.
- **Enhanced UI**: Add visual charts for real-time tracking of network metrics.

## Contributing

If you wish to contribute, feel free to fork the repository and create a pull request.

![image](https://github.com/user-attachments/assets/2910f6d3-2a1f-48fd-80a1-ef1a1a0c2433)


