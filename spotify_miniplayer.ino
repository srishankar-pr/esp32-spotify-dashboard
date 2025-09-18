#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

String inputString = "";      // incoming data buffer
bool stringComplete = false;  // flag for completed line

void setup() {
  Serial.begin(115200);
  delay(1000);

  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println("SSD1306 allocation failed");
    while(true); // Halt
  }
  display.clearDisplay();
  display.display();

  inputString.reserve(200);
}

void loop() {
  // Read serial input
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
      break;
    } else {
      inputString += inChar;
    }
  }

  if (stringComplete) {
    parseAndDisplay(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void parseAndDisplay(String data) {
  int firstSep = data.indexOf('|');
  int secondSep = data.indexOf('|', firstSep + 1);
  int thirdSep = data.indexOf('|', secondSep + 1);

  if (firstSep < 0 || secondSep < 0 || thirdSep < 0) {
    Serial.println("Invalid data format");
    return;
  }

  String title = data.substring(0, firstSep);
  String artist = data.substring(firstSep + 1, secondSep);
  long progress = data.substring(secondSep + 1, thirdSep).toInt();
  long duration = data.substring(thirdSep + 1).toInt();

  displayTrack(title, artist, progress, duration);
}

void displayTrack(String title, String artist, long progress_ms, long duration_ms) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Now Playing:");

  // Limit string lengths for display
  if (title.length() > 21) {
    title = title.substring(0, 18) + "...";
  }
  if (artist.length() > 21) {
    artist = artist.substring(0, 18) + "...";
  }

  display.setCursor(0, 16);
  display.println(title);
  display.setCursor(0, 28);
  display.println(artist);

  // Progress bar
  float ratio = (duration_ms > 0) ? (float)progress_ms / duration_ms : 0;
  int barWidth = 108;
  int filledWidth = (int)(barWidth * ratio);

  display.drawRect(10, 50, barWidth, 10, SSD1306_WHITE);
  display.fillRect(10, 50, filledWidth, 10, SSD1306_WHITE);

  // Time text
  int progressSec = progress_ms / 1000;
  int durationSec = duration_ms / 1000;

  display.setCursor(0, 40);
  display.print(progressSec);
  display.print("s / ");
  display.print(durationSec);
  display.print("s");

  display.display();
}
