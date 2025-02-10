# FL-Studio-Live
This project attempts to support real-time collaboration on FL Studio. The FL Studio software only reads file data on startup, so this project attempts to get around that my mimicking real-time updates by automatically reloading the program on the user's side whenever a change is merged. This bypass isn't a very smooth experience for the user, so this project is simply for Proof-of-Concept.

## Functionality
So far, this project only updates piano roll patterns in real-time. Support for the playlist and arrangement are yet to come. 

## TODO:

Current Fixes:
* Implement UI (CustomTkinter?)
* `Client.java`
- Let user specify directory of changelogs through UI
- Figure out ip of user to connect client socket
* `Server.java`
- Let user specify directory of changelogs through UI
- Fix subprocess directories for the general user
- Detect when a client disconnects instead of simply throwing an erorr
* `ChangeLogEngine.py`
- Loop through Note attributes in _is_equal() instead of hard-checking each one individually.
* `merge_logs.py`
- Let user decide merged log directory through UI

