//Tutorial 2 Arduino Program 
//EP4US2 Fall 2020
//Last Modified: October 4, 2020
//Program Purpose: To obtain and display sensor data on GUI
//Adapted from example program posted on github and from Tutorial 1

#include <OneWire.h>
#include <DallasTemperature.h>
#include <String> //generic library

// Data wire is conntec to the Arduino digital pin 16
#define ONE_WIRE_BUS 16

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

void setup() {
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  
  //Setup code runs once
  //The pinMode function sets a type associated to a specific GPIO (General Purpose Input Output) 
  
  Serial.begin(9600); //Baud rate of 115200Hz
  sensors.begin();
  
  //The pinMode function sets a type associated to a specific GPIO (General Purpose Input Output) 
  pinMode(0,OUTPUT); //IO 0 Output
}

void loop() {

  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  
  //Convert output into voltage: divide max voltage by range of microcontroller. 
  float photo = float(3.3*(float(analogRead(0))/4095.0));

  //Display Sensor data on the Serial Monitor
  Serial.println("Temperature C: " + String(sensors.getTempCByIndex(0)));
  Serial.println("Temperature F: " + String(sensors.getTempFByIndex(0)));
  Serial.println("Light Sensor: " + String(photo));
  delay(1000);
}
   
