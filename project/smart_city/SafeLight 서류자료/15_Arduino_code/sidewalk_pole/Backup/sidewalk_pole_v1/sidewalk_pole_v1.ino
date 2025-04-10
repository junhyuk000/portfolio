#include <SoftwareSerial.h>
#include <Wire.h>



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
int status = 0;  // 앱에서 LED 제어 중인지 확인하는 변수

bool ledState = false;         // 현재 LED 상태 저장 변수



void setup() {
  Serial.begin(9600);        // 시리얼 통신 시작
  pinMode(ledPin1, OUTPUT);  // LED1 핀을 출력으로 설정
  pinMode(ledPin2, OUTPUT);  // LED2 핀을 출력으로 설정
  pinMode(switchPin, INPUT_PULLUP);  // 스위치 핀, 내부 풀업 저항 사용
  pinMode(redPin, OUTPUT);           // 빨간색 LED 핀
  pinMode(bluePin, OUTPUT);          // 파란색 LED 핀
  pinMode(buzzerPin, OUTPUT);        // 부저 핀
  
  

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
          status = 1;
          digitalWrite(ledPin1, HIGH);
          digitalWrite(ledPin2, HIGH);
      } 
      else if (command == "LED_OFF_APP") {
          autoMode = false;
          status = 1;
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
      } 
      else if (command == "AUTO_MODE_APP") {
          autoMode = true;  // 조도 센서 기반 자동 제어 모드 활성화
          status = 0;
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


  delay(100);


  sensorValue = digitalRead(sensorPin);  // 센서 값 읽기
  // Serial.print("Sensor Value: ");       // 시리얼 모니터에 출력
  // Serial.println(sensorValue);
  
  delay(500);  // 0.5초마다 센서 값 갱신
  
  // LDR 값을 읽어온다 (0~1023 범위)
  ldrValue = analogRead(ldrPin);
  
  ldrValue2 = analogRead(ldrPin2);
  
  ldrValue3 = analogRead(ldrPin3);
  
  // 시리얼 모니터에 LDR 값 출력 (디버깅용)
  // Serial.print("LDR Value: ");
  // Serial.println(ldrValue);

  // // 조도 값에 따라 LED 제어
  // if (ldrValue < 200) {  // 어두운 환경
  //   analogWrite(ledPin1, 255);   // LED1 켬
  //   analogWrite(ledPin2, 255);   // LED2 켬
  // }
  // else if (ldrValue < 400) {  // 어느 정도 밝은 환경
  //   analogWrite(ledPin1, 60);   // LED1 켬c:\Users\sj606\olddata\Desktop\road_pole\road_pole.ino
  //   analogWrite(ledPin2, 60);   // LED2 켬
  // }
  // else {  // 밝은 환경
  //   analogWrite(ledPin1, 0);    // LED1 끔
  //   analogWrite(ledPin2, 0);    // LED2 끔
  // }



    // **변경된 시리얼 출력** (한 줄로 출력)   


    int switchState = digitalRead(switchPin); 

    
    Serial.print("ID: 2"); // side walk용
    Serial.print(" | TILT Value: "); // side walk용
    Serial.print(sensorValue);
    Serial.print(" | MAIN LDR Value: ");    
    Serial.print(ldrValue);
    Serial.print(" | SUB1 LDR Value: ");
    Serial.print(ldrValue2);
    Serial.print(" | SUB2 LDR Value: ");
    Serial.print(ldrValue3);
  
    Serial.print(" | Switch State: ");
    Serial.print(switchState);  // 스위치 상태 (HIGH 또는 LOW)를 출력
    if (status == 1){
      Serial.println(" | Check: 1");
    }
    else {
      Serial.println(" | Check: 0");
    }
    



    delay(3000); // 2초마다 갱신

  if (switchState == LOW) {  // 스위치가 눌리면
    // 10번 점멸 반복 (빨간색과 파란색 LED 번갈아 점멸)
    for (int i = 0; i < 4; i++) {
      // 빨간색 LED 켜고, 파란색 LED 끄기
      digitalWrite(redPin, HIGH);
      digitalWrite(bluePin, LOW);
      tone(buzzerPin, 880);  // 1000Hz 소리 (주파수 설정)
      delay(500);  // 100ms 대기 (소리 짧게 울리기)
      noTone(buzzerPin);  // 소리 끄기
      
      // 빨간색 LED 끄고, 파란색 LED 켜기
      digitalWrite(redPin, LOW);
      digitalWrite(bluePin, HIGH);
      tone(buzzerPin, 523);  // 1000Hz 소리 (주파수 설정)
      delay(500);  // 100ms 대기 (소리 짧게 울리기)
      noTone(buzzerPin);  // 소리 끄기
      // delay(500);                    // 500ms 대기

    }
    // 점멸이 끝난 후 부저 끄기
    digitalWrite(buzzerPin, LOW);
  } else {
    // 스위치가 눌리지 않으면 LED와 부저 끄기
    digitalWrite(redPin, LOW);
    digitalWrite(bluePin, LOW);
    digitalWrite(buzzerPin, LOW);   // 부저 끄기
  }

  delay(100);  // 작은 지연, 너무 빨리 반복되지 않도록 함


}