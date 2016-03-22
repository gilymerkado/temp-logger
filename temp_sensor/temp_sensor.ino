#include <OneWire.h>

const int temperaturePin1 = 2;
const int temperaturePin2 = 3;
const int temperaturePin3 = 4;
const int temperaturePin4 = 5;
const int temperaturePin5 = 6;

//Temperature chip i/o
OneWire ds1(temperaturePin1); // on digital pin 2
OneWire ds2(temperaturePin2); // on digital pin 3
OneWire ds3(temperaturePin3); // on digital pin 4
OneWire ds4(temperaturePin4); // on digital pin 5
OneWire ds5(temperaturePin5); // on digital pin 6

void setup()
{
  Serial.begin(9600);
}


void loop()
{
  float temperature1 = getTemp(ds1);
//  Serial.print("1 ");
  Serial.println(temperature1);
  
//  float temperature2 = getTemp(ds2);
//  Serial.print("2 ");
//  Serial.println(temperature2);
//  
//  float temperature3 = getTemp(ds3);
//  Serial.print("3 ");
//  Serial.println(temperature3);
//  
//  float temperature4 = getTemp(ds4);
//  Serial.print("4 ");
//  Serial.println(temperature4);
//  
//  float temperature5 = getTemp(ds5);
//  
//  Serial.print("5 ");
//  Serial.println(temperature5);
  delay(1000); // repeat once per second
}

float getTemp(OneWire pin) {
  //returns the temperature from one DS18S20 in DEG Celsius
  
  byte data[12];
  byte addr[8];
  
  if(!pin.search(addr)) {
    //no more sensors on chain, reset search
    pin.reset_search();
    return -1000;
  }
  if (OneWire::crc8(addr, 7) != addr[7]) {
    Serial.print("Device is not recognized");
    return -1000;
  }
  
  pin.reset();
  pin.select(addr);
  pin.write(0x44, 1);//Start conversion, with parasite power on at the end
  byte present = pin.reset();
  pin.select(addr);
  pin.write(0xBE);// Read Scratchpad
  
  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = pin.read();
  }
  
  pin.reset_search();
  
  byte MSB = data[1];
  byte LSB = data[0];
  
  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;
  
  return TemperatureSum;
}
