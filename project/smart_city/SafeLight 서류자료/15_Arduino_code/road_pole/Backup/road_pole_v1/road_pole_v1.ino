#include <SoftwareSerial.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <Wire.h>

// DHT 센서 핀과 타입 설정 (DHT11 센서 사용, 핀 7)
#define DHTPIN 2      // DHT 센서의 데이터 핀 (D2)
#define DHTTYPE DHT11

// 메인 조도센서, LED1, LED2 핀 설정 
int ldrPin = A0;      // LDR 센서가 연결된 아날로그 핀
int ldrPin2 = A2;      // LDR 센서가 연결된 아날로그 핀
int ldrPin3 = A3;      // LDR 센서가 연결된 아날로그 핀
int ledPin1 = 9;      // LED1이 연결된 디지털 핀
int ledPin2 = 10;     // LED2가 연결된 디지털 핀
int ldrValue = 0;     // LDR의 아날로그 값
int ldrValue2 = 0;     // LDR의 아날로그 값
int ldrValue3 = 0;     // LDR의 아날로그 값
int brightness = 0;   // LED 밝기 (0~255)
bool autoMode = false;  // 자동 모드 활성화 여부 (웹 또는 앱에서 AUTO_MODE가 켜졌을 때)


// RGB핀 설정
int switchPin = 8;      // 스위치가 연결된 디지털 핀
int redPin = 7;         // 빨간색 LED가 연결된 핀
int bluePin = 6;        // 파란색 LED가 연결된 핀
int buzzerPin = 4;      // 부저가 연결된 핀

// 기울기 센서 핀 설정
int sensorPin = 11;  // 기울기 센서가 연결된 아날로그 핀
int sensorValue = 0; // 센서 갑 저장 변수

// LED 상태를 저장하는 변수 추가 (앱에서 명령을 보내면 조도센서 무시)
bool ledControlByApp = false;  // 앱에서 LED 제어 중인지 확인하는 변수
bool ledState = false;         // 현재 LED 상태 저장 변수

// 객체 선언
DHT dht(DHTPIN, DHTTYPE);  // DHT 센서 객체
LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C LCD 주소 0x27, 16x2 LCD

// 체감온도 계산 함수
float computeHeatIndex(float temperature, float humidity) {
    float HI;

    // 체감온도 계산을 위한 상수들
    float c1 = -8.78471, c2 = 1.61139, c3 = 2.33854, c4 = -0.14624;
    float c5 = -0.012308, c6 = -0.016424, c7 = 0.002211;
    float c8 = 0.000725, c9 = -0.00000358;

    HI = c1 + c2 * temperature + c3 * humidity + c4 * temperature * humidity + c5 * temperature * temperature +
         c6 * humidity * humidity + c7 * temperature * temperature * humidity + c8 * temperature * humidity * humidity +
         c9 * temperature * temperature * humidity * humidity;

    return HI;
}


void setup() {
  Serial.begin(9600);        // 시리얼 통신 시작
  pinMode(ledPin1, OUTPUT);  // LED1 핀을 출력으로 설정
  pinMode(ledPin2, OUTPUT);  // LED2 핀을 출력으로 설정
  pinMode(switchPin, INPUT_PULLUP);  // 스위치 핀, 내부 풀업 저항 사용
  pinMode(redPin, OUTPUT);           // 빨간색 LED 핀
  pinMode(bluePin, OUTPUT);          // 파란색 LED 핀
  pinMode(buzzerPin, OUTPUT);        // 부저 핀
  
  dht.begin();         // DHT 센서 초기화
  lcd.begin();    // LCD 초기화 (16x2 크기)
  lcd.backlight();     // LCD 백라이트 켜기  lcd.setCursor(0, 0);
  lcd.print("Humidity Sensor");
  delay(2000);         // 2초 대기
  lcd.clear();
}

void loop() {
  // ** 블루투스 또는 시리얼 명령 수신 **
  if (Serial.available()) {  
      String command = Serial.readStringUntil('\n'); // 한 줄씩 읽기
      command.trim();

      Serial.println("Received command: " + command);  // 수신한 명령 확인

      // ** 앱에서 제어 (APP 명령) **
      if (command == "LED_ON_APP") {
          autoMode = false; // 수동 모드로 변경
          digitalWrite(ledPin1, HIGH);
          digitalWrite(ledPin2, HIGH);
      } 
      else if (command == "LED_OFF_APP") {
          autoMode = false;
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
      } 
      else if (command == "AUTO_MODE_APP") {
          autoMode = true;  // 조도 센서 기반 자동 제어 모드 활성화
      }

      // ** 웹에서 제어 (WEB 명령) **
      else if (command == "LED_ON_WEB") {
          autoMode = false;
          digitalWrite(ledPin1, HIGH);
          digitalWrite(ledPin2, HIGH);
      } 
      else if (command == "LED_OFF_WEB") {
          autoMode = false;
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
      } 
      else if (command == "AUTO_MODE_WEB") {
          autoMode = true;  // 조도 센서 기반 자동 제어 모드 활성화
      }
  }

  // ** 조도 센서를 통한 자동 밝기 조절 (AUTO_MODE_APP & AUTO_MODE_WEB) **
  if (autoMode) {  
      ldrValue = analogRead(ldrPin);
      
      if (ldrValue < 200) {  
          analogWrite(ledPin1, 255);
          analogWrite(ledPin2, 255);
      } 
      else if (ldrValue < 400) {  
          analogWrite(ledPin1, 60);
          analogWrite(ledPin2, 60);
      } 
      else {  
          analogWrite(ledPin1, 0);
          analogWrite(ledPin2, 0);
      }
  }


  delay(100);  // 작은 지연

  sensorValue = digitalRead(sensorPin);  // 센서 값 읽기
  delay(500);  // 0.5초마다 센서 값 갱신

  // LDR 값 읽기
  ldrValue = analogRead(ldrPin);
  ldrValue2 = analogRead(ldrPin2);
  ldrValue3 = analogRead(ldrPin3);

  // 온습도 값 읽기
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // 오류 확인
  if (isnan(humidity) || isnan(temperature)) {
      Serial.println("DHT 센서 오류!");
      lcd.setCursor(0, 0);
      lcd.print("Sensor Error");
      return;
  }

  // 체감온도 계산
  float heatIndex = computeHeatIndex(temperature, humidity);
  int switchState = digitalRead(switchPin); 

  // 시리얼 출력
  Serial.print("ID: 1 | TILT Value: ");
  Serial.print(sensorValue);
  Serial.print(" | MAIN LDR Value: ");    
  Serial.print(ldrValue);
  Serial.print(" | SUB1 LDR Value: ");
  Serial.print(ldrValue2);
  Serial.print(" | SUB2 LDR Value: ");
  Serial.print(ldrValue3);
  Serial.print(" | Temperature: ");
  Serial.print(temperature);
  Serial.print(" | Humidity: ");
  Serial.print(humidity);
  Serial.print(" | Heat Index: ");
  Serial.print(heatIndex);
  Serial.print(" | Switch State: ");
  Serial.println(switchState); 

  // LCD 출력
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("HI: ");
  lcd.print(heatIndex);
  lcd.print(" C");

  delay(1000); // 1초마다 갱신

  // 스위치 동작 처리
  if (switchState == LOW) {  
    for (int i = 0; i < 4; i++) {
      digitalWrite(redPin, HIGH);
      digitalWrite(bluePin, LOW);
      tone(buzzerPin, 880);  // 880Hz 소리
      delay(500);
      noTone(buzzerPin);
      
      digitalWrite(redPin, LOW);
      digitalWrite(bluePin, HIGH);
      tone(buzzerPin, 523);  // 523Hz 소리
      delay(500);
      noTone(buzzerPin);
    }
    digitalWrite(buzzerPin, LOW);  // 부저 끄기
  } else {
    digitalWrite(redPin, LOW);
    digitalWrite(bluePin, LOW);
    digitalWrite(buzzerPin, LOW);   // 부저 끄기
  }

  delay(100);  // 작은 지연
}