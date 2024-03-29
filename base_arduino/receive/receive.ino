// demo: CAN-BUS Shield, receive data with check mode
// send data coming to fast, such as less than 10ms, you can use this way
// loovee, 2014-6-13


#include "CAN_BUS_Shield/mcp_can.h"
#include <SPI.h>

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

void setup()
{
    Serial.begin(9600);

START_INIT:

    if(CAN_OK == CAN.begin(CAN_1000KBPS))                   // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init ok!");
    }
    else
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println("Init CAN BUS Shield again");
        delay(100);
        goto START_INIT;
    }
}


void loop()
{
    unsigned char len = 0;
    unsigned char buf[8];

    if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

        unsigned long canId = CAN.getCanId();
        

        
        if( (canId != 1537)&&(canId != 1409)&&(canId != 1793)
//          (canId != 1537)&&(canId != 1538)&&(canId != 1539)&&(canId != 1540)&&
//        (canId != 1409)&&(canId != 1410)&&(canId != 1411)&&(canId != 1412)&&
//        (canId != 1793)&&(canId != 1794)&&(canId != 1795)&&(canId != 1796)
        )
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

/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
