from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import sys
import os
import json
import random
from datetime import datetime

# Add the parent directory to the path so we can import from flp_parser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flp_parser.ChangeLogEngine import ChangeLogEntry, ChangeLog, ChangeType
except ImportError:
    # Mock classes for testing without the actual FL Studio parser
    class ChangeType:
        INSERT = 1
        DELETE = 2
        UPDATE = 3
    
    class Note:
        def __init__(self, position=0, length=0, key=60, velocity=0.8):
            self.position = position  # Position in ticks
            self.length = length      # Length in ticks
            self.key = key            # MIDI note number (60 = middle C)
            self.velocity = velocity  # Note velocity (volume)
    
    class ChangeLogEntry:
        def __init__(self, change_type, pattern_name, note, updates=None):
            self.change_type = change_type
            self.pattern_name = pattern_name
            self.note = note
            self.updates = updates
            self.timestamp = datetime.now()
    
    class ChangeLog:
        def __init__(self):
            self._entries = []
        
        def add_entry(self, entry):
            self._entries.append(entry)
        
        def get_entries(self):
            return self._entries

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fl-studio-live-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected clients
clients = {}
# Store current piano roll state
piano_roll_state = {}
# Mock changelog for demo purposes
changelog = ChangeLog()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/piano-roll', methods=['GET'])
def get_piano_roll():
    return jsonify(piano_roll_state)

@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify(clients)

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    client_color = f"#{random.randint(0, 0xFFFFFF):06x}"
    clients[client_id] = {
        'id': client_id,
        'name': f"User-{len(clients) + 1}",
        'color': client_color,
        'connected_at': datetime.now().isoformat()
    }
    emit('client_connected', clients[client_id], broadcast=True)
    emit('client_list', list(clients.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in clients:
        client = clients.pop(client_id)
        emit('client_disconnected', client, broadcast=True)
        emit('client_list', list(clients.values()), broadcast=True)

@socketio.on('update_name')
def handle_name_update(data):
    client_id = request.sid
    if client_id in clients and 'name' in data:
        clients[client_id]['name'] = data['name']
        emit('client_updated', clients[client_id], broadcast=True)
        emit('client_list', list(clients.values()), broadcast=True)

@socketio.on('add_note')
def handle_add_note(data):
    client_id = request.sid
    if client_id not in clients:
        return
    
    note_data = data.get('note', {})
    pattern_name = data.get('pattern_name', 'Default Pattern')
    
    # Create a Note object
    note = Note(
        position=note_data.get('position', 0),
        length=note_data.get('length', 480),  # Default to one beat at 120 BPM
        key=note_data.get('key', 60),         # Middle C by default
        velocity=note_data.get('velocity', 0.8)
    )
    
    # Create a change log entry
    entry = ChangeLogEntry(ChangeType.INSERT, pattern_name, note)
    changelog.add_entry(entry)
    
    # Update piano roll state
    note_id = f"{note.position}_{note.key}_{datetime.now().timestamp()}"
    if pattern_name not in piano_roll_state:
        piano_roll_state[pattern_name] = {}
    
    piano_roll_state[pattern_name][note_id] = {
        'position': note.position,
        'length': note.length,
        'key': note.key,
        'velocity': note.velocity,
        'client_id': client_id,
        'client_color': clients[client_id]['color'],
        'timestamp': datetime.now().isoformat()
    }
    
    # Broadcast the change
    emit('note_added', {
        'pattern_name': pattern_name,
        'note_id': note_id,
        'note': piano_roll_state[pattern_name][note_id],
        'client': clients[client_id]
    }, broadcast=True)

@socketio.on('update_note')
def handle_update_note(data):
    client_id = request.sid
    if client_id not in clients:
        return
    
    note_id = data.get('note_id')
    pattern_name = data.get('pattern_name', 'Default Pattern')
    updates = data.get('updates', {})
    
    if pattern_name in piano_roll_state and note_id in piano_roll_state[pattern_name]:
        # Get the original note
        note_data = piano_roll_state[pattern_name][note_id]
        
        # Create a Note object from the original data
        note = Note(
            position=note_data['position'],
            length=note_data['length'],
            key=note_data['key'],
            velocity=note_data['velocity']
        )
        
        # Create a change log entry for the update
        entry = ChangeLogEntry(ChangeType.UPDATE, pattern_name, note, updates)
        changelog.add_entry(entry)
        
        # Update the piano roll state
        for key, value in updates.items():
            if key in ['position', 'length', 'key', 'velocity']:
                piano_roll_state[pattern_name][note_id][key] = value
        
        piano_roll_state[pattern_name][note_id]['client_id'] = client_id
        piano_roll_state[pattern_name][note_id]['client_color'] = clients[client_id]['color']
        piano_roll_state[pattern_name][note_id]['timestamp'] = datetime.now().isoformat()
        
        # Broadcast the change
        emit('note_updated', {
            'pattern_name': pattern_name,
            'note_id': note_id,
            'note': piano_roll_state[pattern_name][note_id],
            'client': clients[client_id],
            'updates': updates
        }, broadcast=True)

@socketio.on('delete_note')
def handle_delete_note(data):
    client_id = request.sid
    if client_id not in clients:
        return
    
    note_id = data.get('note_id')
    pattern_name = data.get('pattern_name', 'Default Pattern')
    
    if pattern_name in piano_roll_state and note_id in piano_roll_state[pattern_name]:
        # Get the note data before deleting
        note_data = piano_roll_state[pattern_name][note_id]
        
        # Create a Note object from the data
        note = Note(
            position=note_data['position'],
            length=note_data['length'],
            key=note_data['key'],
            velocity=note_data['velocity']
        )
        
        # Create a change log entry
        entry = ChangeLogEntry(ChangeType.DELETE, pattern_name, note)
        changelog.add_entry(entry)
        
        # Delete the note from the piano roll state
        del piano_roll_state[pattern_name][note_id]
        
        # Broadcast the change
        emit('note_deleted', {
            'pattern_name': pattern_name,
            'note_id': note_id,
            'client': clients[client_id]
        }, broadcast=True)

# Generate demo data for testing
def generate_demo_data():
    pattern_name = "Demo Pattern"
    piano_roll_state[pattern_name] = {}
    
    # C major scale
    scale_notes = [60, 62, 64, 65, 67, 69, 71, 72]
    
    # Generate a simple melody
    for i, key in enumerate(scale_notes):
        position = i * 480  # 480 ticks per beat
        note_id = f"{position}_{key}_demo"
        
        piano_roll_state[pattern_name][note_id] = {
            'position': position,
            'length': 480,
            'key': key,
            'velocity': 0.8,
            'client_id': 'demo',
            'client_color': '#3498db',
            'timestamp': datetime.now().isoformat()
        }

# Generate some demo data
generate_demo_data()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 