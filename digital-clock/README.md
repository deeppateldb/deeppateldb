# Digital Clock - Multi-Timezone Display

A sophisticated digital clock application that displays the current time across multiple time zones with an elegant web interface and real-time updates.

## Features

✨ **Key Features:**
- Real-time clock display with live updates every second
- Support for multiple time zones
- Beautiful, responsive UI
- 12-hour and 24-hour format toggle
- Add/remove custom time zones
- Digital and analog clock options
- Dark/Light theme support
- Timezone information display (UTC offset, region details)
- Local storage to save preferences

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python Flask
- **Libraries:** Moment.js, Pytz

## Installation

### Backend Setup
```bash
cd digital-clock
pip install -r requirements.txt
```

### Frontend
No additional setup needed - just open `index.html` in your browser or run the Flask server.

## Usage

### Web Version (Recommended)
```bash
python app.py
```
Then navigate to `http://localhost:5000`

### Command Line Version
```bash
python cli_clock.py
```

## Project Structure

```
digital-clock/
├── app.py                 # Flask backend
├── cli_clock.py          # Command-line version
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   ├── style.css     # Main styles
│   │   └── dark-theme.css # Dark theme
│   └── js/
│       └── clock.js      # Clock logic
├── templates/
│   └── index.html        # Main HTML
└── tests/
    └── test_clock.py     # Unit tests
```

## API Endpoints

- `GET /api/time` - Get current time in all configured zones
- `GET /api/time/<timezone>` - Get time in specific timezone
- `POST /api/timezones` - Set active timezones
- `GET /api/timezones` - List all available timezones

## Configuration

Edit the `config.json` file to customize:
- Default timezones
- Time format (12/24 hour)
- Theme preference
- Update interval

## Examples

### Python Usage
```python
from clock import MultiTimezoneClock

clock = MultiTimezoneClock()
clock.add_timezone('America/New_York')
clock.add_timezone('Europe/London')
clock.add_timezone('Asia/Tokyo')

for tz, time in clock.get_all_times():
    print(f"{tz}: {time}")
```

## License

MIT License
