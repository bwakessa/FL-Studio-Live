# FL-Studio-Live
This project attempts to support real-time collaboration on FL Studio. The FL Studio software only reads file data on startup, so this project attempts to get around that by mimicking real-time updates by automatically reloading the program on the user's side whenever a change is merged. This bypass isn't a very smooth experience for the user, so this project is simply for Proof-of-Concept.

Credit to the creators of the [PyFLP](https://github.com/demberto/PyFLP) library which I used to parse and update .flp files.

## Functionality
So far, this project only updates piano roll patterns in real-time. Support for the playlist and arrangement are yet to come. 

## Getting Started

### Prerequisites
- Python 3.8 or higher
- FL Studio installed (for full functionality)
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/jaffarkeikei/fl-studio-live.git
   cd fl-studio-live
   ```

2. Set up the web visualization component:
   ```
   cd web_visualization
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install simple-websocket  # For improved WebSocket performance
   ```

### Running the Application

1. Start the web visualization server:
   ```
   cd web_visualization
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5001
   ```

### Features
- Real-time collaborative piano roll editing
- Web-based visualization of FL Studio patterns
- Multi-user support with unique usernames
- Drawing and erasing tools
- Adjustable note velocity and length

### Troubleshooting

**Port Already in Use**
If you see "Address already in use" or "Port 5001 is in use by another program":
```
lsof -i :5001  # Find the process using port 5001
kill -9 [PID]  # Kill the process (replace [PID] with the actual process ID)
```

**WebSocket Issues**
If you see "WebSocket transport not available":
```
pip install simple-websocket
```

## TODO:

Current Fixes:
- Implement UI (CustomTkinter?)
- `Client.java`
    - Let user specify directory of changelogs through UI
    - Figure out ip of user to connect client socket
- `Server.java`
    - Let user specify directory of changelogs through UI
    - Fix subprocess directories for the general user
    - Detect when a client disconnects instead of simply throwing an erorr
- `ChangeLogEngine.py`
    - Loop through Note attributes in _is_equal() instead of hard-checking each one individually.
- `merge_logs.py`
    - Let user decide merged log directory through UI
- `save_clients.py`
    - Fix java compile directories for the general user
    - Let user select directories of fl studio file and changelogs
    - Fix loop to me triggered by UI

Future Expansions:
- Support for playlists
- Support for arrangements

## License
This project is open source and available under the [MIT License](LICENSE).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
