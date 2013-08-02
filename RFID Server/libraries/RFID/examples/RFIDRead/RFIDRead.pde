#include <SPI.h>
#include "RFID.h"
#define	uchar	unsigned char
#define	uint	unsigned int
#define MI_OK                 0
#define MI_NOTAGERR           1
#define MI_ERR                2
#define MAX_LEN 16
#define PICC_REQIDL           0x26               //????????????

RFID rfid;

void setup() {                
	Serial.begin(9600); 
	SPI.begin();
	pinMode(10,OUTPUT);             // Set digital pin 10 as OUTPUT to connect it to the RFID /ENABLE pin 
    digitalWrite(10, LOW);          // Activate the RFID reader
	pinMode(5,OUTPUT);               // Set digital pin 10 , Not Reset and Power-down
    digitalWrite(5, HIGH);
	rfid.MFRC522_Init();  
}

void loop() {
  	uchar i,tmp;
	uchar status;
        uchar str[MAX_LEN];
        uchar RC_size;
        uchar blockAddr;
        String mynum = "";

		status = rfid.MFRC522_Request(PICC_REQIDL, str);	
		if (status == MI_OK)
		{
                        Serial.println("Card detected");
			Serial.print(str[0],BIN);
                        Serial.print(" , ");
			Serial.print(str[1],BIN);
                        Serial.println(" ");
		}

		status = rfid.MFRC522_Anticoll(str);
		memcpy(rfid.serNum, str, 5);
		if (status == MI_OK)
		{

                        Serial.println("The card's number is  : ");
			Serial.print(rfid.serNum[0],DEC);
                        Serial.print(" , ");
			Serial.print(rfid.serNum[1],DEC);
                        Serial.print(" , ");
			Serial.print(rfid.serNum[2],DEC);
                        Serial.print(" , ");
			Serial.print(rfid.serNum[3],DEC);
                        Serial.print(" , ");
			Serial.print(rfid.serNum[4],DEC);
                        Serial.println(" ");
                        
			delay(1000);
		}
		
		rfid.MFRC522_Halt();	           
          
}
