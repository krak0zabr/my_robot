#include <ros.h>
#include "std_msgs/Int16.h"
#include "std_msgs/Float32.h"
#include "FastLED.h"

#define NUM_LEDS 24
#define PIN 30
CRGB leds[NUM_LEDS];

int info = 0;

class NewHardware : public ArduinoHardware
{
  public:
  NewHardware():ArduinoHardware(&Serial1, 115200){};
};
ros::NodeHandle_<NewHardware>  nh;

std_msgs::Int16 button;
ros::Publisher button_start("start", &button);

void edge_determine(const std_msgs::Float32 msg){
  float inf = msg.data;
  if (inf > 0.5){
    for (int i = 0; i < NUM_LEDS; i++){
      leds[i] = CHSV(0, 255, 255);
    }
    FastLED.show();
  }
  else if (inf < 0.3) {
    for (int i = 0; i < NUM_LEDS; i++){
      leds[i] = CHSV(90, 255, 255);
    }
    FastLED.show();
  }
  else {
    for (int i = 0; i < NUM_LEDS; i++){
      leds[i] = CHSV(0, 0, 0);
    }
    FastLED.show();
  }
}

ros::Subscriber<std_msgs::Float32> edge("edge", &edge_determine);

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, PIN, RGB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(60);
  pinMode(24, INPUT);
  
  nh.initNode();
  nh.advertise(button_start);
  nh.subscribe(edge);
}

void loop() {
  nh.spinOnce();
  int present = digitalRead(24);
    
  button.data = present;
  if (info != present) {
    if (present == 1) {
      button_start.publish(&button);   
      delay(200);
    }
    info = present;
  }
}