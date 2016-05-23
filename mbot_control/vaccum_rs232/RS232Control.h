//-------cssl include-------//
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <termios.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>

#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#include "cssl/cssl.h"
#include "cssl/port.h"
#include "cssl/cssl.c"
//#include "cssl/info.h"
#define VERSION "by Lain-Jinn Hwang\n"
#include "math.h"

double pre_v_l=0;
double pre_v_r=0;
//-------cssl variable-------//
char *echo ="\r";
cssl_t *serial=0;




//====================//
//   cssl callback    //
//====================//
static void mcssl_callback(int id, uint8_t *buf, int length)
{
    int i;

    if (length == 0) return;

    for(i=0;i<length;i++) {
        putchar(buf[i]);
    }

    fflush(stdout);
    
}

//====================//
//   cssl init        //
//====================//
int mcssl_init()
{
    //char *devs="/dev/ttyUSB0";
    char *devs="/dev/ttyACM0";
    int serial_speed = 9600;

    cssl_start();

    // modify 9600 to desire value 
    printf("(Base Node) Open RS232(%s)\n",devs);
    serial=cssl_open(devs, mcssl_callback, 0, serial_speed, 8, 0, 1);

    if (!serial){
        printf("%s\n",cssl_geterrormsg());
	printf("(Base Node) Open RS232(%s) fail\n",devs);
        //puts("\n--->RS232 OPEN FAIL (cssl_open error) <---");
        fflush(stdout);

	//-------try to open /dev/ttyACM3 -------
	char *dev_ACM1="/dev/ttyACM3";
	printf("(Base Node) Open RS232(%s)\n",dev_ACM1);
	serial=cssl_open(dev_ACM1, mcssl_callback, 0, serial_speed, 8, 0, 1);
	
	if (!serial){
		printf("(Base Node) Open RS232(%s) fail\n",dev_ACM1);
		fflush(stdout);
        	return -1;
	}
    }
    cssl_setflowcontrol(serial, 0, 0);


    return 1;
}

//====================//
//   cssl finish      //
//====================//
void mcssl_finish(){

    cssl_close(serial);
    cssl_stop();

}

void mcssl_motor_stop(){
	printf("(Base Node) stop all motors\n");
	cssl_putchar(serial,'s');
}

void mcssl_motor_init(){
	printf("(Base Node) init all motors\n");
	cssl_putchar(serial,'i');
}

//sennd speed to arduino
void mcssl_base_spped(int x_speed, int y_speed,int yaw_speed){
   // printf("(Base Node) x_speed=%d,y_speed=%d,yaw_speed=%d\n",x_speed, y_speed,yaw_speed);
 
    cssl_putchar(serial,'x');
    cssl_putchar(serial,x_speed);
    cssl_putchar(serial,'y');
    cssl_putchar(serial,y_speed);
    cssl_putchar(serial,'w');
    cssl_putchar(serial,yaw_speed);
    cssl_putchar(serial,'r');
}

void mcssl_base_position_index(int point_index){
    printf("(Base Node) point=%d\n",point_index);
    cssl_putchar(serial,'a');
    cssl_putchar(serial,point_index);
    cssl_putchar(serial,'b');

}
