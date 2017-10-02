#include <dht11.h>
#include <Servo.h>

Servo myservo;
dht11 DHT;
#define LED 2
#define pin_dht 3
#define acqua_bassa 4
#define acqua_alta 5
#define Pompa 6
#define servo 8
#define VERDE 10
#define ROSSO 11
#define BLU 12
//#define fotoresistenza A
#define motorpin A0
#define etanolo A1
#define metano A2
#define butano A3
#define idrogeno A4
int livello = 0; //livello acqua

void setup() {
  myservo.attach(servo);
  myservo.write(0);
  pinMode(ROSSO, OUTPUT);
  pinMode(VERDE, OUTPUT);
  pinMode(BLU, OUTPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(LED,HIGH);
  //pinMode(fotoresistenza, INPUT);
  pinMode(motorpin, OUTPUT);
  pinMode(Pompa, OUTPUT);
  digitalWrite(Pompa, HIGH);
  pinMode(acqua_bassa, INPUT);
  pinMode(acqua_alta, INPUT);
  Serial.begin(9600);
}
void colore (unsigned char rosso, unsigned char verde, unsigned char blu)
{
  analogWrite(ROSSO, rosso); //attiva il led rosso con l’intensita’ definita nella variabile rosso
  analogWrite(BLU, blu); //attiva il led blu con l’intensita’ definita nella variabile blu
  analogWrite(VERDE, verde); //attiva il led verde con l’intensita’ definita nella variabile verde
}
void loop() {
  int chk;
  chk = DHT.read(pin_dht);
  switch (chk){
    case DHTLIB_OK:
      break;
    case DHTLIB_ERROR_CHECKSUM:
      break;
    case DHTLIB_ERROR_TIMEOUT:
      break;
    default:
      break;
  }
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'H') {
      digitalWrite(LED, LOW);
    }
    else if (c == 'L') {
      digitalWrite(LED, HIGH);
    }
    else if (c == 'T'){
      Serial.println(DHT.temperature,1);
      colore(0, 0, 255);
    }
    else if (c == 'U'){
      Serial.println(DHT.humidity,1);
      colore(0, 255, 0);
    }
    else if (c == 'A'){
      myservo.write(90);
      colore(255, 0, 0);
    }
    else if (c == 'C'){
      colore(255, 0, 0);
      myservo.write(-90);
    }
    else if (c == 'V'){
      colore(0, 0, 255);
      analogWrite(motorpin , 170);
    }else if (c == 'S'){
      colore(0, 0, 0);
      analogWrite(motorpin , 0);
    }
    else if(c == 'I'){
      livello=digitalRead(acqua_bassa);
      if (livello == 1){
      colore(0, 255, 0);
      digitalWrite(Pompa, LOW);
      delay(2000);
      digitalWrite(Pompa, HIGH);
      colore(0, 0, 0);}
      else {
          Serial.print("E");
      }
    }
    else if(c == 'G'){
      Serial.println(analogRead(etanolo)/1024.0*5.0);
      
      Serial.println(analogRead(metano)/1024.0*5.0);
      Serial.println(analogRead(butano)/1024.0*5.0);
      Serial.println(analogRead(idrogeno)/1024.0*5.0);
    }
    else if (c == 'R'){
      colore(255, 0, 0); // lancia la routine colore, con il parametro rosso a 255, il verde a 0
      // ed il blu a 0 (accende il rosso)
      delay(600); // aspetta 2 secondi prima di accendere il successivo colore
      colore(0,255, 0); // lancia la routine colore ed accende il verde
      delay(600); // aspetta 2 secondi
      colore(0, 0, 255); // accende il blu
      delay(600);
      colore(237,109,0); // accende l’arancione (237 di rosso e 109 di verde)
      delay(600);;
      colore(255,215,0); // accende il giallo (255 di rosso e 215 di verde)
      delay(600);
      colore(0,46,90); // accende l’indaco (46 di verde e 90 di blu)
      delay(600);
      colore(128,0,128); // accende il viola (128 di rosso e 128 di blu)
      delay(600);
      colore(0,0,0); // spegne tutto e ricomincia
      delay(600);
    }
  }
}

