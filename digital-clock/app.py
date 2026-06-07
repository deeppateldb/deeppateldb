"""Flask backend for multi-timezone digital clock"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pytz
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG_FILE = 'config.json'

def load_config():
    """Load configuration from file"""
    if Path(CONFIG_FILE).exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        'timezones': ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'],
        'format_24h': False,
        'theme': 'light'
    }

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

config = load_config()

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/time')
def get_all_times():
    """Get current time in all configured timezones"""
    times = {}
    for tz_name in config['timezones']:
        try:
            tz = pytz.timezone(tz_name)
            current_time = datetime.now(tz)
            times[tz_name] = {
                'time': current_time.strftime('%H:%M:%S'),
                'time_12h': current_time.strftime('%I:%M:%S %p'),
                'date': current_time.strftime('%A, %B %d, %Y'),
                'offset': current_time.strftime('%z')
            }
        except Exception as e:
            times[tz_name] = {'error': str(e)}
    return jsonify(times)

@app.route('/api/time/<timezone>')
def get_time_by_timezone(timezone):
    """Get time in specific timezone"""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return jsonify({
            'timezone': timezone,
            'time': current_time.strftime('%H:%M:%S'),
            'time_12h': current_time.strftime('%I:%M:%S %p'),
            'date': current_time.strftime('%A, %B %d, %Y'),
            'offset': current_time.strftime('%z'),
            'timestamp': current_time.timestamp()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/timezones', methods=['GET'])
def get_timezones():
    """Get all available timezones"""
    return jsonify({
        'available': pytz.all_timezones,
        'current': config['timezones']
    })

@app.route('/api/timezones', methods=['POST'])
def set_timezones():
    """Set active timezones"""
    data = request.get_json()
    if 'timezones' in data:
        config['timezones'] = data['timezones']
        save_config(config)
        return jsonify({'success': True, 'timezones': config['timezones']})
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    data = request.get_json()
    config.update(data)
    save_config(config)
    return jsonify({'success': True, 'config': config})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
