/**
 * @file MicroAbot.h & MicroAbot.cpp
 * @brief Arduino library for Micro:bit (master) to Arduino Uno (slave) I2C robot.
 *
 * This library enables I2C communication between a Micro:bit acting as the master
 * and an Arduino Uno as the slave, facilitating coordinated control of the robot.
 * Use alongside the provided Micro:bit library and example codes.
 *
 * @repository https://github.com/wookjin-chung/Tandem_Robotics
 * @report_bugs mail@fribot.com
 * @created Dec 18, 2024
 * @version 0.1.0
 * @license MIT License. See LICENSE file for details.
 */

#ifndef MICROABOT_H
#define MICROABOT_H

#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>

enum I2CState {
    I2C_IDLE, RECEIVING, REQUESTED, I2C_ERROR
};

enum RCTimeFSMState {
    RCTIME_IDLE,
    RCTIME_START,
    RCTIME_READ,
    RCTIME_COMPLETE
};

enum class IRState {
    Idle,           
    SingleSignal,   
    TwoSignals,    
    ProcessComplete 
};

enum class UltrasonicSensorType {
    ThreePin,
    FourPin
};

enum class UltrasonicState {
    Idle,
    TriggerPulse,
    WaitForEchoStart,
    WaitForEchoEnd,
    Done
};

class MicroAbot {
public:
	
	MicroAbot();
    ~MicroAbot();
    
    static void receiveEventWrapper(int howMany);
    static void requestEventWrapper();
    
	void processData(uint8_t data);
    void servoStandardDriveWrapper(uint8_t data);
    void servoStopWrapper(uint8_t data);
    void servoDriveWrapper(uint8_t data);
    void attachservoPinsWrapper(uint8_t data);
    void servoDetachWrapper(uint8_t data);
    void digitalWriteCommandWrapper(uint8_t data);
    void analogWriteCommandWrapper(uint8_t data);
    void digitalReadCommandWrapper(uint8_t data);
    void toneCommandWrapper(uint8_t data);
    void pulseInCommandWrapper(uint8_t data);
	void pulseOutCommandWrapper(uint8_t data);
	void pulseCountCommandWrapper(uint8_t data);
	void threePinUltrasonicCommandWrapper(uint8_t data);
	void fourPinUltrasonicCommandWrapper(uint8_t data);
	void rcTimeWrapper(uint8_t data);
	void irDetectWrapper(uint8_t data);
	void irDistanceWrapper(uint8_t data);

	void setup();
    void loop();
 
private:
	void initialize();
    void servoStandardDrive(uint8_t pin, int16_t angleVal);
    void servoStop(uint8_t pin1, uint8_t pin2, int16_t speedL);
    void servoDrive(uint8_t pin1, uint8_t pin2, int16_t speedL, int16_t speedR);
    void attachservoPins(uint8_t svoLeftPin, uint8_t svoRightPin);
    void detachOtherServos(uint8_t newLeftPin, uint8_t newRightPin);
    void servoDetach(uint8_t pin);
	
	void digitalWriteCommand(uint8_t pin, uint8_t state);
    void analogWriteCommand(uint8_t pin, uint16_t value);
    uint32_t digitalReadCommand(uint8_t pin);
    void toneCommand(uint8_t pin, uint16_t frequency, uint16_t duration);
    uint32_t pulseInCommand(uint8_t pin, uint8_t state);
	void pulseOutCommand(uint8_t pin, uint16_t duration);
	uint32_t pulseCountCommand(uint8_t pin, uint16_t duration);
	uint32_t ping(uint8_t ping_pin);
	uint32_t hr04(uint8_t trig_pin,uint8_t echo_pin);
	uint32_t irDetect(uint8_t irLedPin, uint8_t irReceiverPin, uint16_t frequency);
	uint32_t irDistance(uint8_t irLedPin, uint8_t irReceivePin);

	void receiveEvent(int howMany);
    void requestEvent();
	const char* currentI2CStateToString(I2CState state);
	
	void handleI2CError();
    void handleMultiByteData(uint8_t* data, uint8_t howmany);
    void handleOneByteCommand(uint8_t ack);
    void handleReadCommand(uint8_t secondByte);
    void handleTwoByteCommand(uint8_t secondByte);
    void handleCommandError(const char* errorMessage);
    void prepareDataFor0x18Return(uint8_t requestedPin);
	
	bool isalivePin(uint8_t pin);
    bool arePinsValidPair(uint8_t pin1, uint8_t pin2);
	
    I2CState currentI2CState;
    static volatile MicroAbot* instance;
    
	volatile bool _sendAcknowledged;
	volatile bool _handshakeReceived;
	volatile bool _commandDataReceived;
	volatile bool _receivedDataUpdated;
	
	Servo servoLeft, servoRight, servoStandard;
	static const uint8_t SERVO_PINS[][2];
	
	bool _isServoLeftAttached;
	bool _isServoRightAttached;
	bool _isServoStandardAttached;

	volatile uint8_t _ackByte, _firstByte, _secondByte, _howmanyByte;
	volatile uint8_t _pAvalue, _pBvalue, _sValue;
	volatile int16_t _leftValue, _rightValue;
	volatile uint16_t _uleftValue;
	volatile uint8_t _servoLeftPin, _servoRightPin, _servoAnglePin;
	volatile uint8_t _irLedPin, _irReceiverPin;
	uint8_t _sendData[4], _receivedData[12];
	
	struct CommandMapping {
        uint8_t command;
        void (MicroAbot::*function)(uint8_t);
    };
    CommandMapping commandMappings[18];
	void initializeCommandMappings();
	
	struct RequestData {
    	uint8_t reqPin;
    	uint32_t reqValue;
    	RequestData() : reqPin(255), reqValue(0) {}
	};
	RequestData reqData[10]; 
	uint8_t _pincount;
    volatile bool _dataAccessFlag;
	
	// rcTime FSM manage
	static const int numRCTimeFSMs = 2; 
	struct RCTimeFSM {
    	RCTimeFSMState state;
    	uint8_t pin;
    	uint8_t mode;
    	uint32_t value;
    	uint32_t startTime;
	};
	RCTimeFSM rcTimeFSMs[numRCTimeFSMs];
	uint8_t _currentFSMIndex = 0;

	void startRCTimeFSM(uint8_t data, uint8_t mode);
	void processRCTimeFSM(RCTimeFSM &fsm);
	void storeRCTimeData(uint8_t pin, uint32_t value);
	void saveResultToRequestData(uint8_t pin, uint32_t value);

	// irDistance processing
	struct IRSignal {
    	uint8_t irReceivePin;
    	uint8_t irLedPin;
	};
	IRSignal irSignalQueue[2]; 
	int _irSignalCount; 
	uint8_t _processingSignalCount;

	struct IRSensorData {
		uint32_t distance;
   		uint8_t irLedPin;
   		uint8_t irReceivePin;
	};
	IRSensorData measIRValue[2];
	void addIRSignal(IRSignal newSignal);
	void processIRSignal(uint8_t irLedPin, uint8_t irReceivePin);
	void processTwoIRSignals(uint8_t irLedPin1, uint8_t irReceivePin1, uint8_t irLedPin2, uint8_t irReceivePin2);
	void measureDistanceForFrequency(IRSensorData& sensor, unsigned int frequency);

	IRState currentState;

	// ultrasonic distance measure processing
	static const int NUM_ULTRASONIC_SENSORS = 2; 
	struct UltrasonicFSM {
   		UltrasonicSensorType sensorType;
   		uint8_t trig_pin;   // 3pin sensor trigger/echo
   		uint8_t echo_pin;   // 4pin sensor echo
   		UltrasonicState state;
   		uint32_t triggerTime;
   		uint32_t echoStartTime;
   		uint32_t duration;
   		bool measurementComplete;
	};
	UltrasonicFSM ultrasonicFSMs[NUM_ULTRASONIC_SENSORS];
	void processUltrasonicFSM(UltrasonicFSM& fsm);
};

#endif // MICROABOT_H
