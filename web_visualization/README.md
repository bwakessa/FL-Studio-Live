# FL Studio Live - Web Visualization

An out-of-this-world web-based visualization for FL Studio Live collaborative music production.

![FL Studio Live Visualization](https://i.imgur.com/example.jpg)

## Overview

This web application provides a stunning, interactive visualization of the FL Studio Live collaborative workflow. It allows multiple users to collaborate on FL Studio piano roll patterns in real-time through a beautiful cosmic-themed interface.

## Features

- **Interactive Piano Roll**: Add, edit, and delete notes in a visually stunning interface
- **Real-time Collaboration**: See changes from other users as they happen
- **Audio Playback**: Hear notes as they're added using the Web Audio API
- **Audio Visualizer**: Beautiful visualization of the audio output
- **User Activity Tracking**: See who's online and what changes they're making
- **Responsive Design**: Works on desktop and tablet devices

## Installation

1. Make sure you have Python 3.7+ installed
2. Clone this repository
3. Install dependencies:

```bash
cd web_visualization
pip install -r requirements.txt
```

## Running the Application

From the web_visualization directory, run:

```bash
python app.py
```

Then open your browser and navigate to:

```
http://localhost:5000
```

## Usage

1. **Connecting**: The application automatically connects to the server when loaded
2. **Setting Your Name**: Enter your name in the input field and click the check button
3. **Adding Notes**: Select the "Draw" tool and click on the piano roll grid
4. **Removing Notes**: Select the "Erase" tool and click on a note
5. **Changing Note Length**: Use the dropdown to select different note lengths
6. **Changing Velocity**: Adjust the velocity slider to change how loud notes are
7. **Zooming**: Use the zoom buttons to adjust the piano roll view

## Technical Details

- **Backend**: Flask with Flask-SocketIO for real-time communication
- **Frontend**: HTML5, CSS3, and Vanilla JavaScript
- **Audio**: Web Audio API and Tone.js for sound synthesis
- **Visualization**: HTML5 Canvas for audio visualization

## Integration with FL Studio Live

This visualization serves as a demonstration of the capabilities of the FL Studio Live collaboration system. It can be integrated with the actual FL Studio parser by connecting the WebSocket events to the real FL Studio project file parser.

## License

This project is open source and available under the MIT License.

## Acknowledgements

- Based on the FL-Studio-Live project
- Inspired by FL Studio's piano roll interface
- Uses Tone.js for audio synthesis 