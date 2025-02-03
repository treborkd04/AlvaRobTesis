/*#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 14
#define DHTTYPE DHT22
DHT dht(DHTPIN,DHTTYPE);
Adafruit_BMP085 bmp;

int pin =25;
float h;
float t;
float temp;
float presion;
float altitud;
bool digitalSensorRain;
int outputRain; 

const int arraySize = 5;
float valores[arraySize];  

void setup() {
  Serial.begin(115200);
  //Definir como entrada en la ESP32
  pinMode(pin,INPUT);
  //Temperatura y Humedad
  Serial.println(F("DHTxx text!"));
  
  if (isnan(h) || isnan(t))
  {
    Serial.println(F("Falla de Lectura del sensor!"));
  }
  dht.begin();
  bmp.begin();
  
}

void loop() {
  delay(1000);
  

  
  valores = medirValores();
  println(valores)

  /*
  Serial.print("Humedad: ");
  Serial.print(h);
  Serial.print(", Temperatura: ");
  Serial.print(t);
  
  Serial.print(", Temp_Bmp: ");
  Serial.print(temp);
  Serial.print(", Presión_Bmp: ");
  Serial.print(presion);
  Serial.print(", Altitud_Bmp: ");
  Serial.print(altitud);
  Serial.print(", Rain: ");
  Serial.print(outputRain);
  Serial.println("");

  */
  
/*
}


float medirValores(){

  float valores[5];
  digitalSensorRain = digitalRead(25);
  if (digitalSensorRain == HIGH)
  {
    outputRain = 0;
  }
  else{
    outputRain = 1;
  }
  h = dht.readHumidity();
  t = dht.readTemperature();
  temp = bmp.readTemperature();
  presion = bmp.readPressure();
  altitud = bmp.readAltitude();

  //AGREGAR VALORES AL ARRAY PRINCIPAL

  valores[0] = h;
  valores[1] = t;
  valores[2] = temp;
  valores[3] = presion;
  valores[4] = altitud;
  valores[5] = outputRain;

  return valores
}

*/

/*
#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 14
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;

int pin = 25;
float h;
float t;
float temp;
float presion;
float altitud;
bool digitalSensorRain;
int outputRain;

const int arraySize = 6;
float valores[arraySize];

unsigned long previousMillis = 0;
const unsigned long interval = 10000; // Intervalo de muestreo en milisegundos (1 minuto)

void setup() {
  Serial.begin(115200);
  pinMode(pin, INPUT);
  Serial.println(F("DHTxx text!"));

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Falla de Lectura del sensor!"));
  }
  dht.begin();
  bmp.begin();
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    medirValores();
    
    Serial.print("Humedad: ");
    Serial.print(valores[0]);
    Serial.print(", Temperatura DHT: ");
    Serial.print(valores[1]);
    Serial.print(", Temperatura BMP: ");
    Serial.print(valores[2]);
    Serial.print(", Presión BMP: ");
    Serial.print(valores[3]);
    Serial.print(", Altitud BMP: ");
    Serial.print(valores[4]);
    Serial.print(", Rain: ");
    Serial.println(valores[5]);
  }
}

void medirValores() {
  digitalSensorRain = digitalRead(25);
  outputRain = (digitalSensorRain == HIGH) ? 0 : 1;
  h = dht.readHumidity();
  t = dht.readTemperature();
  temp = bmp.readTemperature();
  presion = bmp.readPressure();
  altitud = bmp.readAltitude();

  // AGREGAR VALORES AL ARRAY PRINCIPAL
  valores[0] = h;
  valores[1] = t;
  valores[2] = temp;
  valores[3] = presion;
  valores[4] = altitud;
  valores[5] = outputRain;
}
*/

//POSIBLE CÓDIGO FINAL


#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 14
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;

int pin = 25;
float h;
float t;
float temp;
float presion;
float altitud;
bool digitalSensorRain;
int outputRain;

const int arraySize = 6;
float valores[arraySize];

unsigned long previousMillis = 0;
const unsigned long interval = 1000; // Intervalo de muestreo en milisegundos (1 minuto)

void setup() {
  Serial.begin(115200);
  pinMode(pin, INPUT);
  Serial.println(F("DHTxx text!"));
  dht.begin();
  bmp.begin();
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    medirValores();
    
    //Serial.print("Humedad: ");
    Serial.print(valores[0]);
    Serial.print(",");
    //Serial.print(",Temp");
    Serial.print(valores[1]);
    Serial.print(",");
    //Serial.print(",TemperaturaBMP: ");
    //Serial.print(valores[2]);
    //Serial.print(",PresionBMP: ");
    Serial.print(valores[3]);
    Serial.print(",");
    //Serial.print(",AltitudBMP: ");
    //Serial.print(valores[4]);
    //Serial.print(",Rain: ");
    Serial.println(valores[5]);
  }
}

void medirValores() {
  digitalSensorRain = digitalRead(pin);
  outputRain = (digitalSensorRain == HIGH) ? 0 : 1; // Invertido para la lógica común de sensores de lluvia
  h = dht.readHumidity();
  t = dht.readTemperature();
  //temp = bmp.readTemperature();
  presion = bmp.readPressure();
  //altitud = bmp.readAltitude();

  // Verificar si las lecturas son válidas antes de asignarlas al array de valores
  if (isnan(h) || isnan(t) || isnan(temp) || isnan(presion) || isnan(altitud)) {
    Serial.println(F("Falla de Lectura del sensor!"));
    // Manejar el error aquí según sea necesario
  } else {
    // AGREGAR VALORES AL ARRAY PRINCIPAL
    valores[0] = h;
    valores[1] = t;
    //valores[2] = temp;
    valores[3] = presion;
    //valores[4] = altitud;
    valores[5] = outputRain;
  }
}
