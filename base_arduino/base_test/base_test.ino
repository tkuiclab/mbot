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



unsigned char buf[8] = {0, 1, 2, 3, 4, 5, 6, 7};

// 1. shutdown
unsigned char down[8] = {0x2b, 0x40, 0x60,0, 0x06, 0,0,0};

// 2. switch on
unsigned char on0[8] = {0x2b, 0x40, 0x60, 0, 0x0E, 0,0,0};
unsigned char on[8] = {0x2b, 0x40, 0x60, 0, 7, 0,0,0};

// 2. switch off
unsigned char switchOff[8] = {0x2b, 0x40, 0x60, 0, 0xd, 0,0,0};

// 3. enable 
unsigned char enable[8] = {0x2b, 0x40, 0x60, 0, 15, 0,0,0};


// 4. 1OPMOD3
unsigned char opmod3[8]={0x2F, 0x60, 0x60, 0, 0x03, 0, 0,0};

// 5. speed=500
unsigned char speed500[8]={0x23, 0xff, 0x60, 0, 0xf4, 1, 0,0};

// 6. speed=0
unsigned char speed0[8]={0x23, 0xff, 0x60, 0, 0, 0, 0,0};



//init motor for motor(id)
void init_motor(int id){
  int delay_time = 100;
  
  
  
  CAN.sendMsgBuf(id, 0, 8, on0);
  delay(delay_time);   // delay 10 second
  
  CAN.sendMsgBuf(id, 0, 8, on);
  delay(delay_time);   // delay 10 second
  
  CAN.sendMsgBuf(id, 0, 8, enable);
  delay(delay_time);   // delay 1 second
  
  CAN.sendMsgBuf(id, 0, 8, opmod3);
  delay(delay_time);    // delay 1 second

  char *show_str = new char[20];
  sprintf(show_str,"Motor %d -- init FINISH",id);
  Serial.println(show_str);
  
}



//init all motors
void init_all(){
  init_motor(id_1);
  init_motor(id_2);
  init_motor(id_3);
  init_motor(id_4);
  
}


//restart motor for motor(id)
void restart_motor(int id){
  int delay_time = 50;
  
  CAN.sendMsgBuf(id, 0, 8, down);
  
  CAN.sendMsgBuf(id, 0, 8, on);
  
  CAN.sendMsgBuf(id, 0, 8, enable);

  CAN.sendMsgBuf(id, 0, 8, opmod3);
  
  
  char *show_str = new char[20];
  sprintf(show_str,"Motor %d -- restart FINISH",id);
  Serial.println(show_str);
  
}

//stop all motors at speed 0 
void stop_all(){
  CAN.sendMsgBuf(id_1, 0, 8, speed0);
  CAN.sendMsgBuf(id_2, 0, 8, speed0);
  CAN.sendMsgBuf(id_3, 0, 8, speed0);
  CAN.sendMsgBuf(id_4, 0, 8, speed0);
  
}


void set_motor_rpm(int id,int rpm){
  unsigned char rpm_low  = 0xff & rpm;          //get 0x00ff
  unsigned char rpm_high = (rpm >> 8) & 0xff;   //get 0xff00
  
  
  //speed for buffer 
  unsigned char buf_speed[8]={0x23, 0xff, 0x60, 0, rpm_low, rpm_high, 0,0};
  CAN.sendMsgBuf(id, 0, 8, buf_speed);

  //char *show_str = new char[32];
  //sprintf(show_str,"set Motor %d to rpm=%d(0x%04x),rpm_low=0x%02x,rpm_high=0x%02x",id,rpm,rpm,rpm_low,rpm_high);
  //Serial.println(show_str);

}


void test_all_speed500(){
  Serial.println("all_speed500");
  CAN.sendMsgBuf(id_1, 0, 8, speed500);
  CAN.sendMsgBuf(id_2, 0, 8, speed500);
  CAN.sendMsgBuf(id_3, 0, 8, speed500);
  CAN.sendMsgBuf(id_4, 0, 8, speed500);
  
}





//arduino setup function, run at begin
void setup()
{
    Serial.begin(9600);

START_INIT:

    if(CAN_OK == CAN.begin(CAN_1000KBPS))                   // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init ok!(send)");
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

//arduino loop function
void loop()
{
  //CAN.sendMsgBuf(id_1, 0, 8, switchOff);
  //Serial.println("switchOff finish");

  stop_all();
  Serial.println("Stop");

  delay(3000);
/*
  set_motor_rpm(id_1,4000);
  set_motor_rpm(id_2,4000);
  set_motor_rpm(id_3,4000);
  set_motor_rpm(id_4,4000);
  Serial.println("Run speed at 4000");

  

  delay(3000);
//*/
  
  /*
  CAN.sendMsgBuf(id_2, 0, 8, switchOff);
  Serial.println("switchOff finish");

  delay(3000);


 

  Serial.println("Enable finish");
  delay(3000);
  
  //init(id_2);

  CAN.sendMsgBuf(id_2, 0, 8, speed500);
  delay(5000);
  */
}

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
