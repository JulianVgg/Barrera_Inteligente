CREATE TABLE IF NOT EXISTS authorized_plates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT NOT NULL UNIQUE,
    owner_name TEXT NOT NULL,
    vehicle_type TEXT DEFAULT 'Automovil',
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_detected TEXT,
    event_date TEXT NOT NULL,
    event_time TEXT NOT NULL,
    access_status TEXT NOT NULL,
    reason TEXT NOT NULL,
    vehicle_confidence REAL,
    distance_cm REAL,
    image_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);