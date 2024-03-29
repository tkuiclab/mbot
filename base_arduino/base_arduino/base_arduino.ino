// demo: CAN-BUS Shield, send data
#include "CAN_BUS_Shield/mcp_can.h"
#include <SPI.h>
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;

unsigned char flagRecv = 0;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

// receive interrupt
//void MCP2515_ISR()
//{
//    flagRecv = 1;
//}

int id_1 = 0x601;
int id_2 = 0x602;
int id_3 = 0x603;
int id_4 = 0x604;
int ptemp = 2;
double pi = 3.14159265359;
double sita = 0;
double alfa = 0.25 * pi;
double l = 38.891;
double beta1 = 0.25 * pi;
double beta2 = 0.75 * pi;
double beta3 = 1.25 * pi;
double beta4 = 1.75 * pi;
double r = 25.4;
float v1, v2, v3, v4;
float t1, t2, t3, t4;
float dtemp1 = 0, dtemp2 = 0, dtemp3 = 0, dtemp4 = 0;
int max_speed =500;

 
unsigned char buf[8] = {0, 1, 2, 3, 4, 5, 6, 7};
unsigned char len = 0;
long encodertemp = 0;
long encoder_1 = 0;
long encoder_2 = 0;
long encoder_3 = 0;
long encoder_4 = 0;
long last_encoder_1 = 0;
long last_encoder_2 = 0;
long last_encoder_3 = 0;
long last_encoder_4 = 0;
// 1. shutdown
unsigned char down[8] = {0x2b, 0x40, 0x60, 0, 0x60, 0, 0, 0};

// 2. switch on
unsigned char on0[8] = {0x2b, 0x40, 0x60, 0, 0x0E, 0, 0, 0};
unsigned char on[8] = {0x2b, 0x40, 0x60, 0, 7, 0, 0, 0};

// 3. enable
unsigned char enable[8] = {0x2b, 0x40, 0x60, 0, 15, 0, 0, 0};


// 4. 1OPMOD3
unsigned char opmod3[8] = {0x2F, 0x60, 0x60, 0, 0x03, 0, 0, 0};

// 5. speed=500
unsigned char speed500[8] = {0x23, 0xff, 0x60, 0, 0xf4, 1, 0, 0};

// 6. speed=0
unsigned char speed0[8] = {0x23, 0xff, 0x60, 0, 0, 0, 0, 0};
// 7. tpos
unsigned char tpos[8] = {0x40, 0x62, 0x60, 0, 0, 0, 0, 0};


//about VACCUM
#define VACCUM_PIN 7
const char ON = 'O';    //get command
const char OFF = 'X';    //get value


//init motor for motor(id)
void init_motor(int id) {
  int delay_time = 100;

  CAN.sendMsgBuf(id, 0, 8, on0);
  delay(delay_time);   // delay 10 second

  CAN.sendMsgBuf(id, 0, 8, on);
  delay(delay_time);   // delay 10 second

  CAN.sendMsgBuf(id, 0, 8, enable);
  delay(delay_time);   // delay 1 second

  CAN.sendMsgBuf(id, 0, 8, opmod3);
  delay(delay_time);    // delay 1 second
  
  //char *show_str = new char[20];
  //sprintf(show_str,"Motor %d -- init FINISH",id);
  //Serial.println(show_str);

}

void get_encoder(){
  CAN.sendMsgBuf(id_1, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_2, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_3, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_4, 0, 8, tpos);
  get_receive();
      if((encoder_1 == 0)||(encoder_2 == 0)||(encoder_3 == 0)||(encoder_4 == 0)){
        get_encoder();
//            Serial.print("re_getencoder");
//            Serial.print("\t");
//            Serial.print(encodertemp,DEC);
//            Serial.print("\n");
    }     
  }
void get_receive (){
      if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf
        
        unsigned long canId = CAN.getCanId();       
                
        if((canId == 0x581) || (canId == 0x582) || (canId == 0x583) || (canId == 0x584))
        {        
//          Serial.println("-----------------------------");
//          Serial.print("get data from ID: ");
//          Serial.println(canId,HEX);
          
          for(int i = 7; i>=4; i--){
            encodertemp = (encodertemp << 8);
//                        Serial.print(encodertemp,HEX);
//                                      Serial.print("\t");            
            encodertemp = encodertemp + buf[i];
//                        Serial.print(encodertemp,HEX);
//                                      Serial.print("\t");
            }
          switch(canId)
          {
            case 0x581:
            encoder_1 = encodertemp;
//            Serial.print(encoder_1,DEC);       
            break;
            case 0x582:
            encoder_2 = encodertemp;
//            Serial.print(encoder_2,DEC);       
            break;
            case 0x583:
            encoder_3 = encodertemp;
//            Serial.print(encoder_3,DEC);       
            break;
            case 0x584:
            encoder_4 = encodertemp;
//            Serial.print(encoder_4,DEC);       
            break;            
           }
            encodertemp = 0;

//          for(int i = 0; i<len; i++)    // print the data
//          {                
//              Serial.print(buf[i],HEX);
//              Serial.print("\t");
//              
//          }        
//          Serial.println();
        }
    }  
  }
//init all motors
void init_all() {
  init_motor(id_1);
  init_motor(id_2);
  init_motor(id_3);
  init_motor(id_4);


  Serial.println("(Arduino) init all motor finish");
}

//stop all motors at speed 0
void stop_all() {
  CAN.sendMsgBuf(id_1, 0, 8, speed0);
  CAN.sendMsgBuf(id_2, 0, 8, speed0);
  CAN.sendMsgBuf(id_3, 0, 8, speed0);
  CAN.sendMsgBuf(id_4, 0, 8, speed0);
  dtemp1=0;
  dtemp2=0;
  dtemp3=0;
  dtemp4=0;

}


void set_motor_rpm(int id, int rpm) {
  //    Serial.println(rpm, HEX);
  unsigned char rpm_low1  = 0xff & rpm;          //get 0x00ff of rpm
  unsigned char rpm_high2 = (rpm >> 8)  & 0xff;   //get 0xff00 of rpm
  unsigned char rpm_low3  = (rpm >> 8 >> 8 ) & 0xff;    //get 0xff0000 of rpm
  unsigned char rpm_high4 = (rpm >> 8 >> 8 >> 8) & 0xff;   //get 0xff000000 of rpm

  //      Serial.println(rpm_low1, HEX);
  //      Serial.println(rpm_high2, HEX);
  //      Serial.println(rpm_low3, HEX);
  //      Serial.println(rpm_high4, HEX);
  //speed for buffer
  unsigned char buf_speed[8] = {0x23, 0xff, 0x60, 0, rpm_low1, rpm_high2, rpm_low3, rpm_high4};

  CAN.sendMsgBuf(id, 0, 8, buf_speed);
  //        Serial.println(v3);

  //char *show_str = new char[64];
  //  sprintf(show_str,"set Motor %d to rpm=%d(0x%04x),rpm_low=0x%02x,rpm_high=0x%02x",id,rpm,rpm,rpm_low,rpm_high);
  //Serial.println(show_str);

}


void set_base_speed(int x, int y, int yaw) {
//  if (x == 0 && y == 0 && yaw == 0) {
//    stop_all();
//  }
  Serial.print("run speed");
  v1 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta2) / sin(-alfa)) * yaw;
  v2 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta1) / sin(alfa)) * yaw;
  v3 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta3) / sin(alfa)) * yaw;
  v4 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta4) / sin(-alfa)) * yaw;

  v1 *= 1 / r;
  v2 *= -1 / r;
  v3 *= 1 / r;
  v4 *= -1 / r;
    if( v1*max_speed/2>=max_speed || v1*max_speed/2<=-max_speed){
      v1=(v1/abs(v1))*max_speed;
    }else{
      v1*=max_speed/2;
    }
      
    if( v2*max_speed/2>=max_speed || v2*max_speed/2<=-max_speed){
      v2=(v2/abs(v2))*max_speed;
    }else{
      v2*=max_speed/2;
    }
      
    if( v3*max_speed/2>=max_speed || v3*max_speed/2<=-max_speed){
      v3=(v3/abs(v3))*max_speed;
    }else{
      v3*=max_speed/2;
    }
      
    if( v4*max_speed/2>=max_speed || v4*max_speed/2<=-max_speed){
      v4=(v4/abs(v4))*max_speed;  
    }else{
      v4*=max_speed/2;
    } 
          
  Serial.print("v1=");
  Serial.println(v1);
  Serial.print("v2=");
  Serial.println(v2);
  Serial.print("v3=");
  Serial.println(v3);
  Serial.print("v4=");
  Serial.println(v4);//*/ 
  //-------------------------------------A---------------------
float a1 = (v1-dtemp1)/10;
float a2 = (v2-dtemp2)/10;
float a3 = (v3-dtemp3)/10;
float a4 = (v4-dtemp4)/10;
  if((a1!=0)&&(a2!=0)&&(a3!=0)&&(a4!=0)){
    for(int i=1 ; i <=10 ; i++){
      dtemp1 = dtemp1+a1;
      dtemp2 = dtemp2+a2;
      dtemp3 = dtemp3+a3;
      dtemp4 = dtemp4+a4;
    
      set_motor_rpm(id_1, dtemp1);
      set_motor_rpm(id_2, dtemp2);
      set_motor_rpm(id_3, dtemp3);
      set_motor_rpm(id_4, dtemp4);
      delay (30);
      
    /*Serial.print("dtemp1=");
      Serial.println(dtemp1);
      Serial.print("dtemp2=");
      Serial.println(dtemp2);
      Serial.print("dtemp3=");
      Serial.println(dtemp3);
      Serial.print("dtemp4=");
      Serial.println(dtemp4);//*/
    }
  }
}
void set_base_move(int x, int y, int yaw) {
  int sw = 1;
  v1 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta2) / sin(-alfa)) * yaw;
  v2 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta1) / sin(alfa)) * yaw;
  v3 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta3) / sin(alfa)) * yaw;
  v4 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta4) / sin(-alfa)) * yaw;

  v1 *= 1 / (r*pi);
  v2 *= -1 / (r*pi);
  v3 *= 1 / (r*pi);
  v4 *= -1 / (r*pi);
  t1 = v1;
  t2 = v2;
  t3 = v3;
  t4 = v4;
  last_encoder_1 = encoder_1;
  last_encoder_2 = encoder_2;
  last_encoder_3 = encoder_3;
  last_encoder_4 = encoder_4;  
          Serial.print("last_encoder_1 = ");
          Serial.print(last_encoder_1,DEC);
          Serial.print("\n");
          Serial.print("last_encoder_2 = ");
          Serial.print(last_encoder_2,DEC);
          Serial.print("\n");
          Serial.print("last_encoder_3 = ");
          Serial.print(last_encoder_3,DEC);
          Serial.print("\n");
          Serial.print("last_encoder_4 = ");
          Serial.print(last_encoder_4,DEC);
          Serial.print("\n");
  while(sw){

    get_encoder();
      if(labs(last_encoder_1-encoder_1) >= labs(t1*400000)){ 
          sw = 0;
          set_motor_rpm(id_1, v1*0);     
        }else{
          sw = 1;
        }
      if(labs(last_encoder_2-encoder_2) >= labs(t2*400000)){ 
          sw = 0;
          set_motor_rpm(id_2, v2*0);      
        }else{
          sw = 1;
        }
      if(labs(last_encoder_3-encoder_3) >= labs(t3*400000)){ 
          sw = 0;
          set_motor_rpm(id_1, v1*0);    
        }else{
          sw = 1;
        }
      if(labs(last_encoder_4-encoder_4) >= labs(t4*400000)){ 
          sw = 0;
          set_motor_rpm(id_4, v1*0);    
        }else{
          sw = 1;
        } 
        //SPEED 
    if( v1*max_speed/2>=max_speed || v1*max_speed/2<=-max_speed){
      v1=(v1/abs(v1))*max_speed;
    }else{
      v1*=max_speed/2;
    }
      
    if( v2*max_speed/2>=max_speed || v2*max_speed/2<=-max_speed){
      v2=(v2/abs(v2))*max_speed;
    }else{
      v2*=max_speed/2;
    }
      
    if( v3*max_speed/2>=max_speed || v3*max_speed/2<=-max_speed){
      v3=(v3/abs(v3))*max_speed;
    }else{
      v3*=max_speed/2;
    }
      
    if( v4*max_speed/2>=max_speed || v4*max_speed/2<=-max_speed){
      v4=(v4/abs(v4))*max_speed;  
    }else{
      v4*=max_speed/2;
    }
        
       set_motor_rpm(id_1, v1);
       set_motor_rpm(id_2, v2);
       set_motor_rpm(id_3, v3);
       set_motor_rpm(id_4, v4);       
                        
    }
       set_motor_rpm(id_1, 0);
       set_motor_rpm(id_2, 0);
       set_motor_rpm(id_3, 0);
       set_motor_rpm(id_4, 0);   

//          Serial.print("encoder_1 = ");
//          Serial.print(encoder_1,DEC);
//          Serial.print("\n");
//          Serial.print("encoder_2 = ");
//          Serial.print(encoder_2,DEC);
//          Serial.print("\n");
//          Serial.print("encoder_3 = ");
//          Serial.print(encoder_3,DEC);
//          Serial.print("\n");
//          Serial.print("encoder_4 = ");
//          Serial.print(encoder_4,DEC);   
//          Serial.print("\n");
      
  /*Serial.print("t1=");
  Serial.println(t1*400000);
  Serial.print("t2=");
  Serial.println(t2*400000);
  Serial.print("t3=");
  Serial.println(t3*400000);
  Serial.print("t4=");
  Serial.println(t4*400000);//*/
 
}
void run_point(int point) {
    //set_base_move(0, -30, 0);//south
    //set_base_move(0, 30, 0);//north
    //set_base_move(0, 10, 0);
    
    if((ptemp-point)<0){
        set_base_move(0, (point-ptemp)*31.5, 0);
        ptemp=point;
      }else if((ptemp-point)>0){
        set_base_move(0, (point-ptemp)*31.5, 0);
        ptemp=point;
      }else{
        set_base_speed(0, 0, 0);     
      }
}





//arduino setup function, run at begin
void setup()
{
  pinMode(VACCUM_PIN, OUTPUT);
  Serial.begin(9600);

START_INIT:

  if (CAN_OK == CAN.begin(CAN_1000KBPS))                  // init can bus : baudrate = 500k
  {
    Serial.println("CAN BUS Shield init ok!(send)");  //    set_motor_rpm(id_4,-500);
  }
  else
  {
    Serial.println("CAN BUS Shield init fail");
    Serial.println("Init CAN BUS Shield again");
    delay(100);
    goto START_INIT;
  }

  init_all();

}


int8_t x_speed;
int8_t y_speed;
int8_t yaw_speed;
int8_t point_index;
int8_t move_len;
int8_t *ref_val;


char *loop_show_str = new char[64];




const int CMD = 1;    //get command
const int VAL = 2;    //get value
int step = CMD;



//   x   -100   y


//arduino loop function
void loop()
{

  
  if (Serial.available() > 0) {
    unsigned char data = Serial.read();

//    Serial.print("get data=");
//    Serial.println(data);

 

    switch (step)
    {
      case CMD:
        /*------------------GET Command---------------------*/
        switch (data)
        {
          case 'i':
            init_all();        
            break;

          case 'x':
            ref_val = &x_speed;
            step = VAL;
            break;

          case 'y':
            ref_val = &y_speed;
            step = VAL;
            break;

          case 'w':
            ref_val = &yaw_speed;
            step = VAL;
            break;

          case 'r':
            //------------------------RUN----------------------------//
//            sprintf(loop_show_str, "x_speed=%d,y_speed=%d", x_speed, y_speed);
//            Serial.println(loop_show_str);
            set_base_speed(x_speed, y_speed, yaw_speed);

            break;
          case 'a':
            //------------------------read_point----------------------//
            ref_val = &point_index;
            step = VAL;
            break;
        
          case 'b':
            //--------------------run_point--------------------------//
            Serial.print("RUN_POINT=");
            Serial.println(point_index);
            get_encoder();           
            run_point(point_index); 
          case 'T':
            //------------------------Test Run----------------------//
            get_encoder();
//            set_base_move(0, 10, 0);
            Serial.println("(Arduino) Move 10cm North");
            break;
          case 'G':
            //------------------------move len----------------------//
            ref_val = &move_len;
            step = VAL;
            break;
          case 'F':
            get_encoder();           
            set_base_move(0, move_len, 0);
            Serial.println("(Arduino) Move Length");
            break;
          case 's':
          case 'S':
            stop_all();
            break;
          case 'O':
            digitalWrite(VACCUM_PIN, HIGH);   // turns the LED on, output 5V
            //Serial.println("IN ON");
    
            break;
          case 'X':
            digitalWrite(VACCUM_PIN, LOW);   // turns the LED on, output 5V
            //Serial.println("IN OFF");
    


          default:
            break;


        }

      case VAL:
        *ref_val = data;
        step = CMD;
        break;

      default:
        step = CMD;
        break;
    }




  }
  
//    get_encoder(); 

}


/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
