#ifndef RFID_h
#define RFID_h

#include <SPI.h>
#if defined(ARDUINO) && (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#endif

class RFID
{
public:
    void Write_MFRC522(unsigned char addr, unsigned char val);
	unsigned char Read_MFRC522(unsigned char addr);
	void SetBitMask(unsigned char reg, unsigned char mask);
	void ClearBitMask(unsigned char reg, unsigned char mask);
	void AntennaOn(void);
	void AntennaOff(void);
	void MFRC522_Reset(void);
	void MFRC522_Init(void);
	unsigned char MFRC522_Request(unsigned char reqMode, unsigned char *TagType);
	unsigned char MFRC522_ToCard(unsigned char command, unsigned char *sendData, unsigned char sendLen, unsigned char *backData, unsigned int *backLen);
	unsigned char MFRC522_Anticoll(unsigned char *serNum);
	void CalulateCRC(unsigned char *pIndata, unsigned char len, unsigned char *pOutData);
	unsigned char MFRC522_SelectTag(unsigned char *serNum);
	unsigned char MFRC522_Auth(unsigned char authMode, unsigned char BlockAddr, unsigned char *Sectorkey, unsigned char *serNum);
	unsigned char MFRC522_Read(unsigned char blockAddr, unsigned char *recvData);
	unsigned char MFRC522_Write(unsigned char blockAddr, unsigned char *writeData);
	void MFRC522_Halt(void);
	unsigned char serNum[5];
};
#endif
//
// END OF FILE
//