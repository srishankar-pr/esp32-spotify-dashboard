# ESP32 Spotify Dashboard

A hardware dashboard built with ESP32 and SSD1306 OLED display that shows now playing Spotify track information in real time. The project uses Python and the Spotify API for gathering playback data and sends updates to the ESP32 via serial.

## Features

- Displays track name, artist, and playback status from Spotify
- Real-time updates using Python and serial communication
- Compact SSD1306 OLED display (128x64 px)
- Supports breadboard prototyping for beginners and hardware hobbyists

## Hardware Required

- ESP32 development board
- SSD1306 OLED display (I2C, 128x64)
- Breadboard and jumper wires
- USB cable (for ESP32-PC serial link)

## Software Required

- Python 3
- Spotipy or requests library for Spotify API access
- pyserial library for serial communication
- Arduino IDE (for ESP32 firmware and display code)
- Spotify Developer account for API credentials

## Wiring

| Device        | ESP32 Pin | Description   |
|---------------|-----------|--------------|
| SSD1306 SCL   | GPIO 22   | I2C clock    |
| SSD1306 SDA   | GPIO 21   | I2C data     |
| VCC/GND       | 3.3V/GND  | Power        |
| Serial        | USB       | To PC        |

## Setup

### 1. Get Spotify API Credentials

- Register your app on [Spotify Developer Dashboard]
- Get your `CLIENT_ID`, `CLIENT_SECRET`, and set up `REDIRECT_URI`
- Use `get_refresh_token.py` script to get your `REFRESH_TOKEN`
- Store credentials in a `.env` file (see `.env.example`)

### 2. Flash ESP32

- Connect SSD1306 display to ESP32 as described
- Open and upload the Arduino firmware  in Arduino IDE
- Install the Adafruit_SSD1306 and Adafruit_GFX libraries

### 3. Run Python Telemetry Script

- Edit serial port and .env settings in your Python script (`spotify_dashboard.py`)
- Start the script while Spotify is open; now playing info will appear on the dashboard

### 4. Enjoy Live Spotify Data

- Track info updates as songs change and playback progresses on Spotify
- Playback status (playing/paused) displayed in real time


## License

MIT License or your choice. See LICENSE file.

## Credits

Thanks to the Spotify developer community, Adafruit, and open source hardware enthusiasts.


