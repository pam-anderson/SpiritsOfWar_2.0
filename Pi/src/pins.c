//
//  How to access GPIO registers from C-code on the Raspberry-Pi
//  Example program
//  15-January-2012
//  Dom and Gert
//  Revised: 15-Feb-2013
 
 
// Access from ARM Running Linux
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
 
#define MESSAGE_PINS 4
#define DATA_PINS 20
#define FRAME_SIZE 16384
#define FILE_OFFSET 54

int readyPin = 3;
int donePin = 5;
int messagePins[] = {7, 8, 10, 11};
int dataPins[] = {12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29, 31, 32,
    33, 35, 36, 37, 38, 40};


void setGPIOs() {
    int i = 0;
    if(wiringPiSetupPhys() == -1)
        exit(1);
    pinMode(donePin, INPUT);
    pinMode(readyPin, OUTPUT);
    for(i = 0; i < MESSAGE_PINS; i++) {
        pinMode(messagePins[i], OUTPUT);
    }
    for(i = 0; i < DATA_PINS; i++) {
        pinMode(dataPins[i], OUTPUT);
    }
}

void setMessagePins(int message) {
    int i = 0;
    int bit;

    for(i = 0; i < MESSAGE_PINS; i++) {
        bit = (message >> i) & 0x1;
        digitalWrite(messagePins[i], bit);
    }
    return;
}

void setDataPins(int data) {
    int i = 0;
    int bit;
    for(i = 0; i < DATA_PINS; i++) {
        bit = (data >> i) & 0x1;
        digitalWrite(dataPins[i], bit);
    }
    digitalWrite(readyPin, 1);
    while(digitalRead(donePin) == 0) {
        //wait for pin to become 1
    }
    digitalWrite(readyPin, 0);
    return;
}

void boardIsReady() {
    while(digitalRead(donePin) == 1) {
        //wait for done pin to go to 0
    }
    return;
}


void readframe(char* background) {
    FILE* fp = fopen("frame.bmp", "r");
    FILE* bg = fopen(background, "r");
    fseek(fp, FILE_OFFSET, SEEK_SET);
    int i = 0;
    int colour;

    for(i = 0; i < FRAME_SIZE; i++) {
        colour = fgetc(fp) >> 3;
        colour |= ((fgetc(fp) >> 2) << 5);
        colour |= ((fgetc(fp) >> 3) << 11);
        if(colour == 0) {
            fseek(bg, FILE_OFFSET + (i * 3), SEEK_SET);
            colour = fgetc(bg) >> 3;
            colour |= ((fgetc(bg) >> 2) << 5);
            colour |= ((fgetc(bg) >> 3) << 11);
        }
        boardIsReady();
        setMessagePins(5);
        setDataPins(colour);
    }

    fclose(fp);

}
 
int main(int argc, char **argv)
{
    // Set up gpi pointer for direct register access
    setGPIOs();
    boardIsReady();
    setMessagePins(5);
    setDataPins(0);
    readframe("background.bmp");   
    return 0;
 
}
