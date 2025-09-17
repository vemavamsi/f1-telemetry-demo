
from flask import Flask
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import os, random, time, threading

app = Flask(__name__)

# Env controls
DRIVERS = int(os.getenv('DRIVERS', '5'))
UPDATE_INTERVAL = float(os.getenv('UPDATE_INTERVAL', '0.5'))
JITTER = float(os.getenv('JITTER', '0.2'))

# Metrics
speed = Gauge('driver_speed_kph', 'Instant speed of driver', ['driver'])
engine = Gauge('driver_engine_temp_celsius', 'Engine temperature', ['driver'])
laptime = Gauge('driver_last_lap_ms', 'Last lap time (ms)', ['driver'])
position = Gauge('driver_track_position', 'Track position (1=lead)', ['driver'])

# Sim state
state = {
    f"D{n:02d}": {
        'speed': random.uniform(120, 320),
        'engine': random.uniform(80, 105),
        'laptime': random.uniform(80_000, 100_000),
        'position': n
    }
    for n in range(1, DRIVERS + 1)
}

def step_driver(d):
    # speed fluctuates; occasional spikes
    d['speed'] = max(0, min(360, d['speed'] + random.uniform(-8, 8) + random.uniform(-1,1) * 20 * JITTER))
    # engine temp tracks speed plus random heat
    d['engine'] = max(60, min(140, d['engine'] + (d['speed'] - 200) * 0.01 + random.uniform(-0.5, 0.8)))
    # lap time drifts inversely to speed
    d['laptime'] = max(70_000, min(120_000, d['laptime'] + (210 - d['speed']) * 2 + random.uniform(-200, 200)))

def update_loop():
    while True:
        # Simple re‑ranking by lap time (lower is better)
        ranking = sorted(state.items(), key=lambda kv: kv[1]['laptime'])
        for idx, (name, d) in enumerate(ranking, start=1):
            step_driver(d)
            speed.labels(name).set(d['speed'])
            engine.labels(name).set(d['engine'])
            laptime.labels(name).set(d['laptime'])
            position.labels(name).set(idx)
        time.sleep(UPDATE_INTERVAL)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    threading.Thread(target=update_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
