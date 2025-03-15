// Global variables
let socket;
let currentTool = 'draw';
let pianoRollZoom = 1;
let currentPattern = 'Demo Pattern';
let noteLength = 480; // Default to quarter note (480 ticks)
let velocity = 0.8;
let audioContext;
let audioAnalyser;
let audioDataArray;
let visualizerCanvas;
let visualizerCtx;
let isPlaying = false;
let synth;

// Note to frequency mapping
const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const NOTE_FREQUENCIES = {};

// DOM elements
let pianoRollGrid;
let pianoKeys;
let timelineHeader;
let userList;
let activityLog;
let velocitySlider;
let velocityValue;
let noteLengthSelect;

// Piano roll dimensions
const PIXELS_PER_TICK = 0.25;
const KEY_HEIGHT = 20;
const MIN_KEY = 21; // A0
const MAX_KEY = 108; // C8
const TOTAL_KEYS = MAX_KEY - MIN_KEY + 1;
const TICKS_PER_BEAT = 480;
const BEATS_PER_MEASURE = 4;
const MEASURES_TO_SHOW = 16;
const GRID_WIDTH = TICKS_PER_BEAT * BEATS_PER_MEASURE * MEASURES_TO_SHOW * PIXELS_PER_TICK;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    pianoRollGrid = document.getElementById('piano-roll-grid');
    pianoKeys = document.querySelector('.piano-keys');
    timelineHeader = document.querySelector('.timeline-header');
    userList = document.getElementById('user-list');
    activityLog = document.getElementById('activity-log');
    velocitySlider = document.getElementById('velocity-slider');
    velocityValue = document.querySelector('.velocity-value');
    noteLengthSelect = document.getElementById('note-length');

    // Set up velocity slider
    velocitySlider.addEventListener('input', () => {
        velocity = parseFloat(velocitySlider.value);
        velocityValue.textContent = `${Math.round(velocity * 100)}%`;
    });

    // Set up note length selector
    noteLengthSelect.addEventListener('change', () => {
        noteLength = parseInt(noteLengthSelect.value);
    });

    // Set up tool buttons
    document.getElementById('draw-tool-btn').addEventListener('click', (e) => {
        currentTool = 'draw';
        document.querySelectorAll('[data-tool]').forEach(btn => btn.classList.remove('active'));
        e.target.closest('button').classList.add('active');
    });

    document.getElementById('erase-tool-btn').addEventListener('click', (e) => {
        currentTool = 'erase';
        document.querySelectorAll('[data-tool]').forEach(btn => btn.classList.remove('active'));
        e.target.closest('button').classList.add('active');
    });

    // Set up zoom buttons
    document.getElementById('zoom-in-btn').addEventListener('click', () => {
        if (pianoRollZoom < 2) {
            pianoRollZoom += 0.25;
            updatePianoRollZoom();
        }
    });

    document.getElementById('zoom-out-btn').addEventListener('click', () => {
        if (pianoRollZoom > 0.5) {
            pianoRollZoom -= 0.25;
            updatePianoRollZoom();
        }
    });

    // Set up pattern selection
    document.getElementById('pattern-list').addEventListener('click', (e) => {
        const patternItem = e.target.closest('.pattern-item');
        if (patternItem) {
            document.querySelectorAll('.pattern-item').forEach(item => item.classList.remove('active'));
            patternItem.classList.add('active');
            currentPattern = patternItem.dataset.pattern;
            clearPianoRoll();
            loadPianoRollData();
        }
    });

    // Set up username update
    document.getElementById('update-name-btn').addEventListener('click', () => {
        const name = document.getElementById('username-input').value.trim();
        if (name && socket) {
            socket.emit('update_name', { name });
            addActivityItem(`You changed your name to ${name}`);
        }
    });

    document.getElementById('clear-notes-btn').addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all notes from this pattern?')) {
            clearPianoRoll();
            addActivityItem(`You cleared all notes from ${currentPattern}`);
        }
    });

    // Initialize audio context for visualizer
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        audioAnalyser = audioContext.createAnalyser();
        audioAnalyser.fftSize = 256;
        audioDataArray = new Uint8Array(audioAnalyser.frequencyBinCount);
        
        visualizerCanvas = document.getElementById('audio-visualizer');
        visualizerCtx = visualizerCanvas.getContext('2d');
        
        // Size the canvas correctly
        resizeVisualizer();
        window.addEventListener('resize', resizeVisualizer);
        
        // Set up Tone.js
        synth = new Tone.PolySynth(Tone.Synth).toDestination();
    } catch (e) {
        console.error('Web Audio API is not supported in this browser', e);
    }

    // Initialize piano roll
    initPianoRoll();
    
    // Connect to WebSocket server
    connectWebSocket();
});

// Connect to WebSocket server
function connectWebSocket() {
    // Get the current hostname and use it to connect to the server
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const port = '5000';
    
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
        addActivityItem('Connected to FL Studio Live server');
    });
    
    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        addActivityItem('Disconnected from FL Studio Live server', 'error');
    });
    
    socket.on('client_list', (clients) => {
        updateUserList(clients);
    });
    
    socket.on('client_connected', (client) => {
        addActivityItem(`${client.name} connected`);
    });
    
    socket.on('client_disconnected', (client) => {
        addActivityItem(`${client.name} disconnected`);
    });
    
    socket.on('note_added', (data) => {
        if (data.pattern_name === currentPattern) {
            const note = data.note;
            addNoteToGrid(data.note_id, note.position, note.key, note.length, note.velocity, note.client_color);
            playNote(note.key, note.velocity, note.length);
            addActivityItem(`${data.client.name} added a note`);
        }
    });
    
    socket.on('note_updated', (data) => {
        if (data.pattern_name === currentPattern) {
            const note = data.note;
            updateNoteInGrid(data.note_id, note.position, note.key, note.length, note.velocity, note.client_color);
            addActivityItem(`${data.client.name} updated a note`);
        }
    });
    
    socket.on('note_deleted', (data) => {
        if (data.pattern_name === currentPattern) {
            const noteElement = document.getElementById(`note-${data.note_id}`);
            if (noteElement) {
                noteElement.remove();
                addActivityItem(`${data.client.name} deleted a note`);
            }
        }
    });
}

// Initialize the piano roll
function initPianoRoll() {
    // Create piano keys
    for (let i = MAX_KEY; i >= MIN_KEY; i--) {
        const keyIndex = i % 12;
        const octave = Math.floor(i / 12) - 1;
        const noteName = `${NOTE_NAMES[keyIndex]}${octave}`;
        const frequency = 440 * Math.pow(2, (i - 69) / 12);
        NOTE_FREQUENCIES[i] = frequency;
        
        const isBlack = [1, 3, 6, 8, 10].includes(keyIndex);
        const keyClass = isBlack ? 'black-key' : 'white-key';
        
        const keyElement = document.createElement('div');
        keyElement.className = `piano-key ${keyClass}`;
        keyElement.dataset.key = i;
        keyElement.textContent = noteName;
        
        pianoKeys.appendChild(keyElement);
    }
    
    // Create timeline markers
    for (let measure = 0; measure < MEASURES_TO_SHOW; measure++) {
        for (let beat = 0; beat < BEATS_PER_MEASURE; beat++) {
            const tick = (measure * BEATS_PER_MEASURE + beat) * TICKS_PER_BEAT;
            const x = tick * PIXELS_PER_TICK;
            
            if (beat === 0) {
                // Add measure marker
                const markerElement = document.createElement('div');
                markerElement.className = 'timeline-marker';
                markerElement.style.left = `${x}px`;
                markerElement.textContent = measure + 1;
                timelineHeader.appendChild(markerElement);
                
                // Add measure line
                const lineElement = document.createElement('div');
                lineElement.className = 'grid-measure-line';
                lineElement.style.left = `${x}px`;
                pianoRollGrid.appendChild(lineElement);
            } else {
                // Add beat line
                const lineElement = document.createElement('div');
                lineElement.className = 'grid-beat-line';
                lineElement.style.left = `${x}px`;
                pianoRollGrid.appendChild(lineElement);
            }
        }
    }
    
    // Add key lines
    for (let i = MAX_KEY; i >= MIN_KEY; i--) {
        const y = (MAX_KEY - i) * KEY_HEIGHT;
        const lineElement = document.createElement('div');
        lineElement.className = 'grid-key-line';
        lineElement.style.top = `${y}px`;
        pianoRollGrid.appendChild(lineElement);
    }
    
    // Add click handlers for drawing notes
    pianoRollGrid.addEventListener('click', (e) => {
        if (currentTool === 'draw') {
            const rect = pianoRollGrid.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Snap to grid
            const ticksPerPixel = 1 / (PIXELS_PER_TICK * pianoRollZoom);
            const position = Math.floor(x * ticksPerPixel / 120) * 120; // Snap to 16th notes
            const key = MAX_KEY - Math.floor(y / KEY_HEIGHT);
            
            if (key >= MIN_KEY && key <= MAX_KEY) {
                addNote(position, key, noteLength, velocity);
            }
        }
    });
    
    // Load initial data
    loadPianoRollData();
    
    // Start animation
    animateVisualizer();
}

// Load piano roll data from the server
function loadPianoRollData() {
    fetch('/api/piano-roll')
        .then(response => response.json())
        .then(data => {
            // Clear existing notes
            clearPianoRoll();
            
            // Add notes from the current pattern
            if (data[currentPattern]) {
                Object.entries(data[currentPattern]).forEach(([noteId, note]) => {
                    addNoteToGrid(noteId, note.position, note.key, note.length, note.velocity, note.client_color);
                });
            }
        })
        .catch(error => {
            console.error('Error loading piano roll data:', error);
        });
}

// Clear all notes from the piano roll
function clearPianoRoll() {
    const notes = pianoRollGrid.querySelectorAll('.note-block');
    notes.forEach(note => note.remove());
}

// Add a new note and send to server
function addNote(position, key, length, velocity) {
    if (!socket) return;
    
    socket.emit('add_note', {
        pattern_name: currentPattern,
        note: {
            position,
            key,
            length,
            velocity
        }
    });
    
    // Play the note
    playNote(key, velocity, length);
}

// Add a note to the piano roll grid
function addNoteToGrid(noteId, position, key, length, velocity, color) {
    const noteElement = document.createElement('div');
    noteElement.id = `note-${noteId}`;
    noteElement.className = 'note-block fade-in';
    noteElement.style.left = `${position * PIXELS_PER_TICK * pianoRollZoom}px`;
    noteElement.style.top = `${(MAX_KEY - key) * KEY_HEIGHT}px`;
    noteElement.style.width = `${length * PIXELS_PER_TICK * pianoRollZoom}px`;
    noteElement.style.backgroundColor = color || '#8a2be2';
    noteElement.style.opacity = velocity;
    noteElement.dataset.noteId = noteId;
    noteElement.dataset.position = position;
    noteElement.dataset.key = key;
    noteElement.dataset.length = length;
    noteElement.dataset.velocity = velocity;
    
    // Add delete handler
    noteElement.addEventListener('click', (e) => {
        if (currentTool === 'erase') {
            e.stopPropagation();
            deleteNote(noteId);
        }
    });
    
    pianoRollGrid.appendChild(noteElement);
}

// Update a note in the grid
function updateNoteInGrid(noteId, position, key, length, velocity, color) {
    const noteElement = document.getElementById(`note-${noteId}`);
    if (noteElement) {
        noteElement.style.left = `${position * PIXELS_PER_TICK * pianoRollZoom}px`;
        noteElement.style.top = `${(MAX_KEY - key) * KEY_HEIGHT}px`;
        noteElement.style.width = `${length * PIXELS_PER_TICK * pianoRollZoom}px`;
        noteElement.style.opacity = velocity;
        noteElement.style.backgroundColor = color || '#8a2be2';
        noteElement.dataset.position = position;
        noteElement.dataset.key = key;
        noteElement.dataset.length = length;
        noteElement.dataset.velocity = velocity;
    }
}

// Delete a note and send to server
function deleteNote(noteId) {
    if (!socket) return;
    
    socket.emit('delete_note', {
        pattern_name: currentPattern,
        note_id: noteId
    });
}

// Update the piano roll zoom
function updatePianoRollZoom() {
    // Update all notes
    const notes = pianoRollGrid.querySelectorAll('.note-block');
    notes.forEach(note => {
        const position = parseInt(note.dataset.position);
        const length = parseInt(note.dataset.length);
        note.style.left = `${position * PIXELS_PER_TICK * pianoRollZoom}px`;
        note.style.width = `${length * PIXELS_PER_TICK * pianoRollZoom}px`;
    });
    
    // Update grid width
    pianoRollGrid.style.width = `${GRID_WIDTH * pianoRollZoom}px`;
}

// Update the user list
function updateUserList(clients) {
    userList.innerHTML = '';
    
    clients.forEach(client => {
        const userElement = document.createElement('div');
        userElement.className = 'user-item fade-in';
        userElement.dataset.clientId = client.id;
        
        const avatarElement = document.createElement('div');
        avatarElement.className = 'user-avatar';
        avatarElement.style.backgroundColor = client.color;
        avatarElement.textContent = client.name[0].toUpperCase();
        
        const nameElement = document.createElement('div');
        nameElement.className = 'user-name';
        nameElement.textContent = client.name;
        
        userElement.appendChild(avatarElement);
        userElement.appendChild(nameElement);
        userList.appendChild(userElement);
    });
}

// Add an item to the activity log
function addActivityItem(message, type = 'info') {
    const activityElement = document.createElement('div');
    activityElement.className = `activity-item ${type} fade-in`;
    
    const timeElement = document.createElement('div');
    timeElement.className = 'activity-time';
    const now = new Date();
    timeElement.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    
    const messageElement = document.createElement('div');
    messageElement.className = 'activity-message';
    messageElement.textContent = message;
    
    activityElement.appendChild(timeElement);
    activityElement.appendChild(messageElement);
    
    activityLog.prepend(activityElement);
    
    // Keep only the last 50 messages
    const items = activityLog.querySelectorAll('.activity-item');
    if (items.length > 50) {
        for (let i = 50; i < items.length; i++) {
            items[i].remove();
        }
    }
}

// Play a note using Tone.js
function playNote(key, velocity, length) {
    if (!synth) return;
    
    // Convert MIDI note to frequency
    const frequency = NOTE_FREQUENCIES[key] || 440 * Math.pow(2, (key - 69) / 12);
    
    // Convert ticks to seconds (assuming 120 BPM)
    const durationSeconds = length / TICKS_PER_BEAT * (60 / 120);
    
    // Play the note
    synth.triggerAttackRelease(frequency, durationSeconds, Tone.now(), velocity);
}

// Resize the visualizer canvas
function resizeVisualizer() {
    visualizerCanvas.width = visualizerCanvas.parentElement.offsetWidth;
    visualizerCanvas.height = visualizerCanvas.parentElement.offsetHeight;
}

// Animate the audio visualizer
function animateVisualizer() {
    requestAnimationFrame(animateVisualizer);
    
    if (!audioAnalyser || !visualizerCtx) return;
    
    // Get frequency data
    audioAnalyser.getByteFrequencyData(audioDataArray);
    
    // Clear canvas
    visualizerCtx.clearRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
    
    // Set up gradient
    const gradient = visualizerCtx.createLinearGradient(0, 0, 0, visualizerCanvas.height);
    gradient.addColorStop(0, '#8a2be2');
    gradient.addColorStop(0.5, '#00bfff');
    gradient.addColorStop(1, '#ff1493');
    
    // Draw bars
    const barWidth = visualizerCanvas.width / audioDataArray.length;
    let x = 0;
    
    for (let i = 0; i < audioDataArray.length; i++) {
        const barHeight = audioDataArray[i] / 255 * visualizerCanvas.height;
        
        visualizerCtx.fillStyle = gradient;
        visualizerCtx.fillRect(x, visualizerCanvas.height - barHeight, barWidth - 1, barHeight);
        
        x += barWidth;
    }
    
    // Draw a cosmic line across the top for effect
    visualizerCtx.beginPath();
    visualizerCtx.moveTo(0, 10);
    
    for (let i = 0; i < visualizerCanvas.width; i++) {
        visualizerCtx.lineTo(i, 5 + Math.sin(i * 0.01 + Date.now() * 0.001) * 5);
    }
    
    visualizerCtx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    visualizerCtx.lineWidth = 2;
    visualizerCtx.stroke();
} 