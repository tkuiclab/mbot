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
double pi = 3.14159265359;
double sita = 0;
double alfa = 0.25 * pi;
double l = 388.91;
double beta1 = 0.25 * pi;
double beta2 = 0.75 * pi;
double beta3 = 1.25 * pi;
double beta4 = 1.75 * pi;
double r = 25.4;
float v1, v2, v3, v4;
float dtemp1 = 0, dtemp2 = 0, dtemp3 = 0, dtemp4 = 0;

unsigned char buf[8] = {0, 1, 2, 3, 4, 5, 6, 7};
unsigned char len = 0;
unsigned char encoder_1[8]= {0, 1, 2, 3, 4, 5, 6, 7};
unsigned char encoder_2[8]= {0, 1, 2, 3, 4, 5, 6, 7};
unsigned char encoder_3[8]= {0, 1, 2, 3, 4, 5, 6, 7};
unsigned char encoder_4[8]= {0, 1, 2, 3, 4, 5, 6, 7};
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

void get_encoder (){
  CAN.sendMsgBuf(id_1, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_2, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_3, 0, 8, tpos);
  get_receive();
  CAN.sendMsgBuf(id_4, 0, 8, tpos);
  get_receive();     
  }
void get_receive (){
      if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

        unsigned long canId = CAN.getCanId();
        

        
        if((canId == 0x581) || (canId == 0x582) || (canId == 0x583) || (canId == 0x584))
        {        
          Serial.println("-----------------------------");
          Serial.print("get data from ID: ");
          Serial.println(canId, HEX);        
          for(int i = 0; i<len; i++)    // print the data
          {
                
              Serial.print(buf[i],HEX);
              Serial.print("\t");
          }        
          Serial.println();
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
  CAN.sendMsgBuf(id_2, 0, 8, speed0);float v1, v2, v3, v4;
  CAN.sendMsgBuf(id_3, 0, 8, speed0);
  CAN.sendMsgBuf(id_4, 0, 8, speed0);


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
  if (x == 0 && y == 0 && yaw == 0) {
    stop_all();
  }

  v1 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta2) / sin(-alfa)) * yaw;
  v2 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta1) / sin(alfa)) * yaw;
  v3 = (cos(sita - alfa) / sin(alfa)) * x + (sin(sita - alfa) / sin(alfa)) * y + (l * sin(sita - alfa - beta3) / sin(alfa)) * yaw;
  v4 = (cos(sita + alfa) / sin(-alfa)) * x + (sin(sita + alfa) / sin(-alfa)) * y + (l * sin(sita + alfa - beta4) / sin(-alfa)) * yaw;

  v1 *= 1 / r;
  v2 *= -1 / r;
  v3 *= 1 / r;
  v4 *= -1 / r;

    if( v1*250>=500 || v1*250<=-500){
      v1=(v1/abs(v1))*500;
    }else{
      v1*=250;
    }
      
    if( v2*250>=500 || v2*250<=-500){
      v2=(v2/abs(v2))*500;
    }else{
      v2*=250;
    }
      
    if( v3*250>=500 || v3*250<=-500){
      v3=(v3/abs(v3))*500;
    }else{
      v3*=250;
    }
      
    if( v4*250>=500 || v4*250<=-500){
      v4=(v4/abs(v4))*500;
    }else{
      v4*=250;
    }  
      
  /*Serial.print("v1=");
  Serial.println(v1);
  Serial.print("v2=");
  Serial.println(v2);
  Serial.print("v3=");
  Serial.println(v3);
  Serial.print("v4=");
  Serial.println(v4);*/
  
float a1 =(v1-dtemp1)/10;
float a2 =(v2-dtemp2)/10;
float a3 =(v3-dtemp3)/10;
float a4 =(v4-dtemp4)/10;

  for(int i=1 ; i <=10 ; i++){
    dtemp1 = dtemp1+a1;
    dtemp2 = dtemp2+a2;
    dtemp3 = dtemp3+a3;
    dtemp4 = dtemp4+a4;
    
    set_motor_rpm(id_1, dtemp1);
    set_motor_rpm(id_2, dtemp2);
    set_motor_rpm(id_3, dtemp3);
    set_motor_rpm(id_4, dtemp4);
    delay (50);
          
  /*Serial.print("dtemp1=");
  Serial.println(dtemp1);
  Serial.print("dtemp2=");
  Serial.println(dtemp2);
  Serial.print("dtemp3=");
  Serial.println(dtemp3);
  Serial.print("dtemp4=");
  Serial.println(dtemp4);*/
  }
  
//  get_encoder();
 
   
//  set_motor_rpm(id_1, -500);
//  set_motor_rpm(id_2, -500);
//  set_motor_rpm(id_3, -500);
//  set_motor_rpm(id_4, -500);
  //  CAN.sendMsgBuf(id_1, 0, 8, speed500);
  //  CAN.sendMsgBuf(id_2, 0, 8, speed500);
  //  CAN.sendMsgBuf(id_3, 0, 8, speed500);
  //  CAN.sendMsgBuf(id_4, 0, 8, speed500);

  //    set_motor_rpm(id_4,-500);


}


void test_all_speed500() {
  Serial.println("all_speed500");
  CAN.sendMsgBuf(0x601, 0, 8, speed500);
  CAN.sendMsgBuf(0x602, 0, 8, speed500);
  CAN.sendMsgBuf(0x603, 0, 8, speed500);
  CAN.sendMsgBuf(0x604, 0, 8, speed500);

}





//arduino setup function, run at begin
void setup()
{
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

    Serial.print("get data=");
    Serial.println(data);

 

    switch (step)
    {
      case CMD:
        /*------------------GET Command---------------------*/
        switch (data)
        {
          case 'i':
            init_all();        
            get_encoder();
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
            sprintf(loop_show_str, "x_speed=%d,y_speed=%d", x_speed, y_speed);
            Serial.println(loop_show_str);


            set_base_speed(x_speed, y_speed, yaw_speed);
 
            break;

          case 's':
            stop_all();
            break;


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
