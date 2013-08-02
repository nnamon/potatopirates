#include <SPI.h>
#include <NewPing.h>
#include "RFID.h"
#define	uchar	unsigned char
#define	uint	unsigned int

#define TRIGGER_PIN  9  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 150 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

#define MI_OK                 0
#define MI_NOTAGERR           1
#define MI_ERR                2
#define MAX_LEN 16
#define MAX_RFID_LEN 5
#define PICC_REQIDL           0x26               //????????????

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

RFID rfid;
uchar oldStr[MAX_LEN];

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
	checkSonar();
	checkRfid();
	delay(500);
}

void checkSonar() {
	unsigned int uS = sonar.ping_median(5) / US_ROUNDTRIP_CM;
	if (uS != 0) {
		Serial.print("ping,");
		Serial.println(uS);
	}
}

void checkRfid() {
	uchar i,tmp;
	uchar status;
	uchar str[MAX_LEN];
	uchar RC_size;
	uchar blockAddr;
	String mynum = "";

	status = rfid.MFRC522_Request(PICC_REQIDL, str);	
	status = rfid.MFRC522_Anticoll(str);

	if (status == MI_OK) {
		boolean sameCode = true;
		for (int i=0;i<MAX_RFID_LEN;i++)
			if (oldStr[i] != str[i])	
				sameCode = false;

		if (!sameCode) {
			Serial.print("rfid,");
			for (int i=0;i<MAX_RFID_LEN;i++)
				Serial.print(str[i], HEX);
	  
			Serial.println();	
			for (int i=0;i<MAX_RFID_LEN;i++)
				oldStr[i] = str[i];
		
		}
	} else {
                if (oldStr[0] != 0)
                        Serial.println("rcard");
		oldStr[0] = 0;
	}

	rfid.MFRC522_Halt();
}
