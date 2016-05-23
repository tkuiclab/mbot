
#define VACCUM_PIN 11
const char ON = 'O';    //get command
const char OFF = 'X';    //get value


void setup() {
  pinMode(VACCUM_PIN, OUTPUT);
  Serial.begin(9600);       
}





void loop() {
    
    //Serial.println("HI");
    if (Serial.available() > 0) {
    unsigned char cmd = Serial.read();
    //Serial.println(cmd);
    
      switch (cmd)
      {
        case 'O':
        case 'o':
            digitalWrite(VACCUM_PIN, HIGH);   // turns the LED on, output 5V
            //Serial.println("IN ON");
    
            break;
        case 'X':
        case 'x':
            digitalWrite(VACCUM_PIN, LOW);   // turns the LED on, output 5V
            //Serial.println("IN OFF");
    
            
            break;
        default:
            Serial.println("FAIL CMD");
            break;
      }
    }
}

