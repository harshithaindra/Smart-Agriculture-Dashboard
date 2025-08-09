#include <DHT.h>

#define DHTPIN 2          // DHT sensor data pin is connected to digital pin 2
#define DHTTYPE DHT11     // Using DHT11

DHT dht(DHTPIN, DHTTYPE); // Create DHT object
const int soilPin = A0;   // Soil sensor is connected to analog pin A0

void setup() {
  Serial.begin(9600);     // Start serial communication with PC
  dht.begin();            // Start the DHT sensor
}

void loop() {
  float temperature = dht.readTemperature(); // in °C
  float humidity = dht.readHumidity();       // in %
  int soilValue = analogRead(soilPin);       // 0 = wet, 1023 = dry

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Error reading DHT!");
    return;
  }

  // Print in format: temp,humidity,soil
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(soilValue);

  delay(2000); // Wait 2 seconds before next reading
}
