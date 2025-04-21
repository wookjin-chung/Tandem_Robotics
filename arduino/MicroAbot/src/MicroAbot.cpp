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

#include "MicroAbot.h"

volatile MicroAbot* MicroAbot::instance = nullptr;

MicroAbot::MicroAbot() : _isServoLeftAttached(true), _isServoRightAttached(true), _isServoStandardAttached(true), 
	_sendAcknowledged(false), currentI2CState(I2C_IDLE), _commandDataReceived(false), _receivedDataUpdated(false), 
	_handshakeReceived(false), _dataAccessFlag(false), _ackByte(0), _firstByte(0), _secondByte(0), _howmanyByte(0), 
	_servoLeftPin(255), _servoRightPin(255), _servoAnglePin(255), _pAvalue(27), _pBvalue(33), _sValue(0), 
	_leftValue(0), _rightValue(0), _uleftValue(0), _pincount(0), _irSignalCount(0), _processingSignalCount(0),
	currentState(IRState::Idle)
{
    MicroAbot::instance = this;
    memset(_sendData, 0, sizeof(_sendData));
    memset(_receivedData, 0, sizeof(_receivedData));
   	initializeCommandMappings();
   	
   	for (int i = 0; i < numRCTimeFSMs; i++) {
        rcTimeFSMs[i].state = RCTIME_IDLE;
    }
	for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
        ultrasonicFSMs[i].state = UltrasonicState::Idle;
        ultrasonicFSMs[i].trig_pin = 255; 
        ultrasonicFSMs[i].echo_pin = 255;
        ultrasonicFSMs[i].measurementComplete = false;
    }	
}

MicroAbot::~MicroAbot() {
    MicroAbot::instance = nullptr;
}

void MicroAbot::receiveEventWrapper(int howMany) {
    if (MicroAbot::instance != nullptr) {
        MicroAbot::instance->receiveEvent(howMany);
    }
}

void MicroAbot::requestEventWrapper() {
    if (MicroAbot::instance != nullptr) {
        MicroAbot::instance->requestEvent();
    }
}

const char* MicroAbot::currentI2CStateToString(I2CState state) {
    switch (state) {
        case I2C_IDLE: return "I2C_IDLE";
        case RECEIVING: return "RECEIVING";
        case REQUESTED: return "REQUESTED";
        case I2C_ERROR: return "I2C_ERROR";
        default: return "Unknown State";
    }
}

// Wrapper function for function pointer mapping
void MicroAbot::initializeCommandMappings() {
    commandMappings[0] = {24, &MicroAbot::servoStandardDriveWrapper};
    commandMappings[1] = {28, &MicroAbot::servoStopWrapper};
    commandMappings[2] = {25, &MicroAbot::servoDriveWrapper};
    commandMappings[3] = {38, &MicroAbot::attachservoPinsWrapper};
    commandMappings[4] = {39, &MicroAbot::servoDetachWrapper};

    commandMappings[5] = {3, &MicroAbot::digitalReadCommandWrapper};
    commandMappings[6] = {1, &MicroAbot::digitalWriteCommandWrapper};
    commandMappings[7] = {2, &MicroAbot::digitalWriteCommandWrapper};
    commandMappings[8] = {32, &MicroAbot::analogWriteCommandWrapper};
    commandMappings[9] = {13, &MicroAbot::toneCommandWrapper};
    
    commandMappings[10] = {16, &MicroAbot::rcTimeWrapper};
	commandMappings[11] = {31, &MicroAbot::irDetectWrapper};
	commandMappings[12] = {33, &MicroAbot::irDistanceWrapper};
	
	commandMappings[13] = {10, &MicroAbot::pulseInCommandWrapper};
	commandMappings[14] = {11, &MicroAbot::pulseOutCommandWrapper};
	commandMappings[15] = {12, &MicroAbot::pulseCountCommandWrapper};
    commandMappings[16] = {35, &MicroAbot::threePinUltrasonicCommandWrapper};
    commandMappings[17] = {36, &MicroAbot::fourPinUltrasonicCommandWrapper};
}

void MicroAbot::processData(uint8_t data) {
    for (int i = 0; i < 18; ++i) {
        if (commandMappings[i].command == data && commandMappings[i].function != nullptr) {
            (this->*(commandMappings[i].function))(data);
            //Serial.print("command data is ");
            //Serial.println(data);
            break;
        }
    }
}

void MicroAbot::servoStandardDriveWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	int16_t angleVal = _leftValue;
	servoStandardDrive(pin, angleVal);
}

void MicroAbot::servoStopWrapper(uint8_t data) {
	uint8_t pin1 = _pAvalue;
	uint8_t pin2 = _pBvalue;
	int16_t speedL = _leftValue;
	servoStop(pin1, pin2, speedL);
}

void MicroAbot::servoDriveWrapper(uint8_t data) {
    uint8_t pin1 = _pAvalue;
	uint8_t pin2 = _pBvalue;
	int16_t speedL = _leftValue;
	int16_t speedR = _rightValue;
    servoDrive(pin1, pin2, speedL, speedR);
}

void MicroAbot::attachservoPinsWrapper(uint8_t data) {
	uint8_t svoLeftPin = _pAvalue;
	uint8_t svoRightPin = _pBvalue;
	attachservoPins(svoLeftPin, svoRightPin);
}

void MicroAbot::servoDetachWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	servoDetach(pin);
}

void MicroAbot::digitalWriteCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint8_t state = data;
	digitalWriteCommand(pin, state);	
}

void MicroAbot::analogWriteCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint16_t value = _leftValue;
	analogWriteCommand(pin, value);	
}

void MicroAbot::digitalReadCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	bool pinFound = false;
	
	for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == pin) {
        	reqData[i].reqValue = digitalReadCommand(pin);
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) { 
        reqData[_pincount].reqPin = pin;
        reqData[_pincount].reqValue = digitalReadCommand(pin);
        _pincount++;
    }
}

void MicroAbot::toneCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint16_t frequency = _rightValue;
	uint16_t duration = _leftValue;
	toneCommand(pin, frequency, duration);
}

void MicroAbot::pulseInCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint8_t state = _sValue;
	bool pinFound = false;
	
	for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == pin) {
        	reqData[i].reqValue = pulseInCommand(pin, state);
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) { 
        reqData[_pincount].reqPin = pin;
        reqData[_pincount].reqValue = pulseInCommand(pin, state);
        _pincount++;
    }
}

void MicroAbot::pulseOutCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint16_t duration = _leftValue;
	pulseOutCommand(pin, duration);
}

void MicroAbot::pulseCountCommandWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint16_t duration = _leftValue;
	bool pinFound = false;
	
	for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == pin) {
        	reqData[i].reqValue = pulseCountCommand(pin, duration);
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) { 
        reqData[_pincount].reqPin = pin;
        reqData[_pincount].reqValue = pulseCountCommand(pin, duration);
        _pincount++;
    }
}

void MicroAbot::threePinUltrasonicCommandWrapper(uint8_t data) {
    uint8_t ping_pin = _pAvalue;
    bool fsmFound = false;
    int fsmIndex = -1;

    for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
        if (ultrasonicFSMs[i].trig_pin == ping_pin &&
    		ultrasonicFSMs[i].echo_pin == ping_pin &&
            ultrasonicFSMs[i].sensorType == UltrasonicSensorType::ThreePin) {
            fsmIndex = i;
            fsmFound = true;
            break;
        }
    }

    if (!fsmFound) {
        for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
            if (ultrasonicFSMs[i].state == UltrasonicState::Idle) {
                fsmIndex = i;
                ultrasonicFSMs[i].sensorType = UltrasonicSensorType::ThreePin;
                ultrasonicFSMs[i].trig_pin = ping_pin;
                ultrasonicFSMs[i].echo_pin = ping_pin; 
                ultrasonicFSMs[i].measurementComplete = false;
                break;
            }
        }
    }

    if (fsmIndex != -1) {
        ultrasonicFSMs[fsmIndex].state = UltrasonicState::TriggerPulse;
        ultrasonicFSMs[fsmIndex].measurementComplete = false;
    } else {
        Serial.println("초음파 FSM 슬롯이 부족합니다.");
    }
}

void MicroAbot::fourPinUltrasonicCommandWrapper(uint8_t data) {
    uint8_t trig_pin = _pAvalue;
    uint8_t echo_pin = _pBvalue;
    bool fsmFound = false;
    int fsmIndex = -1;

    for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
        if (ultrasonicFSMs[i].trig_pin == trig_pin &&
            ultrasonicFSMs[i].echo_pin == echo_pin &&
            ultrasonicFSMs[i].sensorType == UltrasonicSensorType::FourPin) {
            fsmIndex = i;
            fsmFound = true;
            break;
        }
    }

    if (!fsmFound) {
        for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
            if (ultrasonicFSMs[i].state == UltrasonicState::Idle) {
                fsmIndex = i;
                ultrasonicFSMs[i].sensorType = UltrasonicSensorType::FourPin;
                ultrasonicFSMs[i].trig_pin = trig_pin;
                ultrasonicFSMs[i].echo_pin = echo_pin;
                ultrasonicFSMs[i].measurementComplete = false;
                break;
            }
        }
    }

    if (fsmIndex != -1) {
        ultrasonicFSMs[fsmIndex].state = UltrasonicState::TriggerPulse;
        ultrasonicFSMs[fsmIndex].measurementComplete = false;
    } else {
        Serial.println("초음파 FSM 슬롯이 부족합니다.");
    }
}

void MicroAbot::rcTimeWrapper(uint8_t data) {
	uint8_t pin = _pAvalue;
	uint8_t s_value = _sValue;
	startRCTimeFSM(pin, s_value);
}

void MicroAbot::irDetectWrapper(uint8_t data) {
	uint8_t irLedPin = _pBvalue;
	uint8_t irReceiverPin = _pAvalue; 
	uint16_t frequency = _leftValue;
	bool pinFound = false;
	
	for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == irLedPin) {
        	reqData[i].reqValue = irDetect(irLedPin, irReceiverPin, frequency);
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) { 
        reqData[_pincount].reqPin = irLedPin;
        reqData[_pincount].reqValue = irDetect(irLedPin, irReceiverPin, frequency);
        _pincount++;
    }
}

void MicroAbot::irDistanceWrapper(uint8_t data) {
    IRSignal newSignal;
    newSignal.irLedPin = _pBvalue;
    newSignal.irReceivePin = _pAvalue;
    addIRSignal(newSignal);
}

void MicroAbot::addIRSignal(IRSignal newSignal) {
	
    switch (currentState) {
        case IRState::Idle:
            irSignalQueue[_irSignalCount++] = newSignal;
            currentState = IRState::SingleSignal;
            break;
            
        case IRState::SingleSignal:
            if (irSignalQueue[0].irLedPin == newSignal.irLedPin && irSignalQueue[0].irReceivePin == newSignal.irReceivePin) {
                currentState = IRState::ProcessComplete;
            } else {
                irSignalQueue[_irSignalCount++] = newSignal;
                currentState = IRState::TwoSignals;
            }
            break;
            
    	case IRState::TwoSignals:
            if (_irSignalCount >= 2) {
                processTwoIRSignals(irSignalQueue[0].irLedPin, irSignalQueue[0].irReceivePin, irSignalQueue[1].irLedPin, irSignalQueue[1].irReceivePin);
                _irSignalCount = 0;  
                currentState = IRState::Idle;
            }
            break;
            
		case IRState::ProcessComplete:
            processIRSignal(irSignalQueue[0].irLedPin, irSignalQueue[0].irReceivePin);
            _irSignalCount = 0;  
            currentState = IRState::Idle;
            break;

        default:
        	currentState = IRState::Idle;
            Serial.println("State unchanged.");
            break;
    }
}

// FSM state management
// rcTime FSM routine
void MicroAbot::startRCTimeFSM(uint8_t pin, uint8_t mode) {
    rcTimeFSMs[_currentFSMIndex].pin = pin;
    rcTimeFSMs[_currentFSMIndex].mode = mode;
    rcTimeFSMs[_currentFSMIndex].state = RCTIME_START;
    _currentFSMIndex = (_currentFSMIndex + 1) % numRCTimeFSMs; 
}

void MicroAbot::processRCTimeFSM(RCTimeFSM &fsm) {
    switch (fsm.state) {
        case RCTIME_IDLE:
            break;

        case RCTIME_START:
        	if (fsm.mode == 1) {
        		pinMode(fsm.pin, OUTPUT);
                digitalWrite(fsm.pin, HIGH);
                delay(1);   // charge the capacitor
            	pinMode(fsm.pin, INPUT);
            	fsm.startTime = micros();
            	fsm.state = RCTIME_READ;
			}
            break;

        case RCTIME_READ:
            uint32_t elapsedTime = micros() - fsm.startTime;
            const uint32_t maxElapsedTime = 100000; // max time 100 ms

            if (digitalRead(fsm.pin) == LOW || elapsedTime >= maxElapsedTime) {
                fsm.value = elapsedTime;
                // Set data access flags
                while (_dataAccessFlag);
                _dataAccessFlag = true;
                storeRCTimeData(fsm.pin, fsm.value);
                _dataAccessFlag = false;
                
                fsm.state = RCTIME_COMPLETE;
            }
            break;

        case RCTIME_COMPLETE:
            fsm.state = RCTIME_IDLE;
            break;
    }
}

void MicroAbot::storeRCTimeData(uint8_t pin, uint32_t value) {
    bool pinFound = false;
    for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == pin) {
            reqData[i].reqValue = value;
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) {
        reqData[_pincount].reqPin = pin;
        reqData[_pincount].reqValue = value;
        _pincount++;
    }
}

// irSensor signal state machine 
void MicroAbot::processIRSignal(uint8_t irLedPin, uint8_t irReceivePin) {
    IRSensorData sensor = {0, irLedPin, irReceivePin};

    for (unsigned int f = 38000; f <= 42000; f += 500) {
        measureDistanceForFrequency(sensor, f);
    }
    //Serial.print("pin is: );
    //Serial.print(sensor.irLedPin);
    //Serial.print("Sensor Distance: ");
    //Serial.println(sensor.distance);
    saveResultToRequestData(sensor.irLedPin, sensor.distance);
}

void MicroAbot::processTwoIRSignals(uint8_t irLedPin1, uint8_t irReceivePin1, uint8_t irLedPin2, uint8_t irReceivePin2) {
    IRSensorData sensor1 = {0, irLedPin1, irReceivePin1};
    IRSensorData sensor2 = {0, irLedPin2, irReceivePin2};
    //Serial.print(sensor1.irReceivePin);
    //Serial.print(" ; ");
    //Serial.println(sensor2.irReceivePin);

    for (unsigned int f = 38000; f <= 42000; f += 500) {
    	measureDistanceForFrequency(sensor1, f);
    	measureDistanceForFrequency(sensor2, f);
    }
    saveResultToRequestData(sensor1.irLedPin, sensor1.distance);
    saveResultToRequestData(sensor2.irLedPin, sensor2.distance);
    //Serial.print("Sensor 1 Distance: ");
    //Serial.println(sensor1.distance);
    //Serial.print("Sensor 2 Distance: ");
    //Serial.println(sensor2.distance);
}

void MicroAbot::saveResultToRequestData(uint8_t pin, uint32_t value) {
	bool pinFound = false;
    for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == pin) {
            reqData[i].reqValue = value;
            pinFound = true;
            break;
        }
    }
    if (!pinFound && _pincount < 10) {
        reqData[_pincount].reqPin = pin;
        reqData[_pincount].reqValue = value;
        _pincount++;
    }
}

// ultrasonic sensor distance measuring FSM -- nonblocking code (pulseIn)
void MicroAbot::processUltrasonicFSM(UltrasonicFSM& fsm) {
    switch (fsm.state) {
        case UltrasonicState::Idle:
            break;

        case UltrasonicState::TriggerPulse:
            if (fsm.sensorType == UltrasonicSensorType::ThreePin) {
                // 3pin sensor trigger pulse sending
                pinMode(fsm.trig_pin, OUTPUT);
                digitalWrite(fsm.trig_pin, LOW);
                delayMicroseconds(2);
                digitalWrite(fsm.trig_pin, HIGH);
                delayMicroseconds(5);
                digitalWrite(fsm.trig_pin, LOW);

                // setup echo pin
                pinMode(fsm.echo_pin, INPUT);
            } else if (fsm.sensorType == UltrasonicSensorType::FourPin) {
                // 4pin sensor trigger pulse sending
                pinMode(fsm.trig_pin, OUTPUT);
                digitalWrite(fsm.trig_pin, LOW);
                delayMicroseconds(2);
                digitalWrite(fsm.trig_pin, HIGH);
                delayMicroseconds(10);
                digitalWrite(fsm.trig_pin, LOW);

                // setup echo pin
                pinMode(fsm.echo_pin, INPUT);
            }
            fsm.triggerTime = micros();
            fsm.state = UltrasonicState::WaitForEchoStart;
            break;

        case UltrasonicState::WaitForEchoStart:
            if (digitalRead(fsm.echo_pin) == HIGH) {
                fsm.echoStartTime = micros();
                fsm.state = UltrasonicState::WaitForEchoEnd;
            } else if (micros() - fsm.triggerTime > 30000) {
                // 30ms timeout --- approx. 4 meter
                fsm.duration = 0;
                fsm.state = UltrasonicState::Done;
            }
            break;

        case UltrasonicState::WaitForEchoEnd:
            if (digitalRead(fsm.echo_pin) == LOW) {
                uint32_t echoEndTime = micros();
                fsm.duration = echoEndTime - fsm.echoStartTime;
                fsm.state = UltrasonicState::Done;
            } else if (micros() - fsm.echoStartTime > 30000) {
                // 30ms timeout --- approx. 4 meter
                fsm.duration = 0;
                fsm.state = UltrasonicState::Done;
            }
            break;

        case UltrasonicState::Done:
            fsm.measurementComplete = true;
            fsm.state = UltrasonicState::Idle;

            // save to reqData
			bool pinFound = false;
            for (int i = 0; i < _pincount; ++i) {
                if (reqData[i].reqPin == fsm.trig_pin) {
                    reqData[i].reqValue = fsm.duration;
                    pinFound = true;
                    break;
                }
            }
            if (!pinFound) {
                if (_pincount >= 10) {
                    _pincount = 0; 
                }
                reqData[_pincount].reqPin = fsm.trig_pin;
                reqData[_pincount].reqValue = fsm.duration;
                _pincount++;
            }
			// Serial.print(" pin = ");
			// Serial.println(fsm.trig_pin);
            // Serial.print(" duration = ");
            // Serial.println(fsm.duration);
            break;
    }
}

// abot operation 
const uint8_t MicroAbot::SERVO_PINS[][2] = {{13, 12}, {11, 10}, {9, 8}};

bool MicroAbot::isalivePin(uint8_t pin) {
	return pin != 33;
};
bool MicroAbot::arePinsValidPair(uint8_t pin1, uint8_t pin2) {
    for (const auto &pair : SERVO_PINS) {
        if ((pair[0] == pin1 && pair[1] == pin2) || (pair[0] == pin2 && pair[1] == pin1)) {
            return true;
        }
    }
    return false;
}

void MicroAbot::initialize() {
	this->attachservoPins(255, 255); // servo inactive state 
    Serial.println("MicroAbot software ver. @0.1.0");
    Serial.println("MicroAbot initialized .... ");
}

void MicroAbot::setup() {
	Wire.begin(0x5D); // Slave address 0x5D = 93
    Wire.onReceive(MicroAbot::receiveEventWrapper);
    Wire.onRequest(MicroAbot::requestEventWrapper);
    initialize();
}

void MicroAbot::loop() {

    if (this->currentI2CState == I2C_IDLE && _receivedDataUpdated && _commandDataReceived) {
		this->processData(_secondByte);
		_commandDataReceived = false;
        _receivedDataUpdated = false;
    } else if (this->currentI2CState == I2C_ERROR) {
    	handleI2CError();	
	}
	
   	processRCTimeFSM(rcTimeFSMs[0]);
   	processRCTimeFSM(rcTimeFSMs[1]);
   	for (int i = 0; i < NUM_ULTRASONIC_SENSORS; ++i) {
        processUltrasonicFSM(ultrasonicFSMs[i]);
    }
}

// return data prepared for requestEvent
void MicroAbot::prepareDataFor0x18Return(uint8_t requestedPin) {
    bool pinFound = false;

    for (int i = 0; i < _pincount; i++) {
        if (reqData[i].reqPin == requestedPin) {
            uint32_t value = reqData[i].reqValue;
            for (int j = 0; j < 4; j++) {
                _sendData[j] = (value >> (j * 8)) & 0xFF; 
            }
            pinFound = true;
            break;
        }
    }
    // If no matching pin is found, prepare to send a default or error value
    if (!pinFound) {
        // define an appropriate default/error response
        for (int j = 0; j < 4; j++) {
            _sendData[j] = 0xFF; 
        }
    }
}

// receiveEvent data treatment
void MicroAbot::handleOneByteCommand(uint8_t ack) {
	switch (ack) {
        case 0x00:
            _sendAcknowledged = true;
            break;
        case 0xAA:
        	_handshakeReceived = true;
        	//Serial.println("0xAA data received");
        	break;
        default:
        	Serial.print(ack);
            handleCommandError("unknown oneByte data");
            break;
    }
}

void MicroAbot::handleReadCommand(uint8_t secondByte) {
    this->prepareDataFor0x18Return(secondByte);
}

void MicroAbot::handleTwoByteCommand(uint8_t secondByte) {
	if (secondByte > 0x00 && secondByte < 0x63) {
		_commandDataReceived = true;
    } else {
        handleCommandError("unknown 2-byte data");
    }
}

void MicroAbot::handleCommandError(const char* errorMessage) {
    Serial.print(" -- error: ");
    Serial.println(errorMessage);
}

void MicroAbot::handleMultiByteData(uint8_t* data, uint8_t howmany) {

	switch (howmany) {
        case 4:  // Handle 4-byte data
            _pAvalue = data[1];
            _pBvalue = data[2];
            _sValue = data[3];
            break;

        case 8:  // Handle 8-byte data
            _pAvalue = data[1];
            _pBvalue = data[2];
            _sValue = data[3];
            _uleftValue = ((uint16_t)data[5] << 8) | data[4];
            _leftValue = ((int16_t)data[5] << 8) | data[4];
            break;

        case 12:  // Handle 12-byte data
            _pAvalue = data[1];
            _pBvalue = data[2];
            _sValue = data[3];
            _uleftValue = ((uint16_t)data[5] << 8) | data[4];
            _leftValue = ((int16_t)data[5] << 8) | data[4];
            _rightValue = ((int16_t)data[9] << 8) | data[8];
            break;

        default: // Handle other cases or throw an error
            Serial.println("Error: Unexpected data size");
            break;
    }
}

void MicroAbot::handleI2CError() {
	Wire.end();
    delay(100); // Short delay before reinitializing
    Wire.begin(0x5D);
	Serial.println("I2C Error Occurred");
	this->currentI2CState = I2C_IDLE;
}

void MicroAbot::receiveEvent(int howMany) {
    if (instance == nullptr || this->currentI2CState != I2C_IDLE) {
        return; // Exit if instance is null or state is not idle
    }
    this->currentI2CState = RECEIVING;

    // Serial.println("I2C START!");
    if (howMany <= 0) {
        handleI2CError();
        this->currentI2CState = I2C_IDLE;
        return;
    }

    if (howMany == 1) {
        _ackByte = Wire.read();
        handleOneByteCommand(_ackByte);
        // Serial.print("1-byte : [");
        // Serial.print(_ackByte);
        // Serial.print("]");

    } else if (howMany == 2) {
        _firstByte = Wire.read();
        _secondByte = Wire.read();
        if (_firstByte == 0x18) {
            handleReadCommand(_secondByte);
        } else if (_firstByte == 0x00) {
            handleTwoByteCommand(_secondByte);
        } else {
            // Do nothing or add additional handling if required
        }
        /* Print command byte data
        Serial.print("first-byte : [");
        Serial.print(_firstByte);
        Serial.print("] command-byte : [");
        Serial.print(_secondByte);
        Serial.println("]");
        */

    } else if (howMany >= 4 && howMany <= sizeof(_receivedData)) {
        memset(_receivedData, 0, sizeof(_receivedData));
        for (int i = 0; i < howMany; i++) {
            _receivedData[i] = Wire.read();
        }
        handleMultiByteData(_receivedData, howMany);
        _howmanyByte = howMany;
        _receivedDataUpdated = true;
        /* Print the receiveBuffer values
        Serial.print("    Received data : ");
        for (int i = 0; i < howMany; i++) {
            Serial.print(_receivedData[i]);
            Serial.print(" ");
        }
        Serial.println();
        // Serial.flush(); // Ensure all serial data is sent before continuing
        */

    } else {
        handleI2CError(); // Handle cases where howMany is 3 or > sizeof(_receivedData)
    }
    this->currentI2CState = I2C_IDLE;
}

void MicroAbot::requestEvent() {
	if (instance == nullptr || this->currentI2CState != I2C_IDLE) {
        return; // Exit if instance is null or state is not idle
    }
    this->currentI2CState = REQUESTED;

    if (_handshakeReceived) {
    	uint8_t handshakeResponse = 0x55;
        Wire.write(&handshakeResponse, 1);
        _handshakeReceived = false; 
        
	} else if (_sendAcknowledged) {
        byte ack = 0x00;
        Wire.write(&ack, sizeof(ack));
        _sendAcknowledged = false;
        
    } else if (_firstByte == 0x18) {
        Wire.write(_sendData, 4);
        _firstByte = 0x99;  // initialize to the default value 0x99
    
    } else {
        // Default response or error handling
        byte defaultResponse = 0xFF; // Choose an appropriate default response
        Wire.write(&defaultResponse, sizeof(defaultResponse));
    }

	this->currentI2CState = I2C_IDLE;
}

// abot defined functions 
void MicroAbot::servoStandardDrive(uint8_t pin, int16_t angleVal) {
	if (pin != _servoAnglePin || !_isServoStandardAttached) {
        servoStandard.detach();
        servoStandard.attach(pin);
        _servoAnglePin = pin;
        _isServoStandardAttached = true;
    }
    if (angleVal >= 0 && angleVal <= 180) {
        servoStandard.write(angleVal);
    } else {
    	Serial.println("Error: Invalid input value");
	}
}

void MicroAbot::servoStop(uint8_t pin1, uint8_t pin2, int16_t speedL) {
	if (this->isalivePin(pin2) == true && _howmanyByte == 8) {
		servoLeft.writeMicroseconds(1500);
        servoRight.writeMicroseconds(1500+speedL);	
	} else if (this->isalivePin(pin2) == true && _howmanyByte == 4) {
		servoLeft.writeMicroseconds(1500);
        servoRight.writeMicroseconds(1500);
	} else if (_howmanyByte == 4) {
		if (pin1 == _servoLeftPin) {
        	servoLeft.writeMicroseconds(1500);
		} else if (pin1 == _servoRightPin) {
			servoRight.writeMicroseconds(1500);
		} else if (pin1 == _servoAnglePin) {
			servoStandard.write(90);
		}
	}
}

void MicroAbot::servoDrive(uint8_t pin1, uint8_t pin2, int16_t speedL, int16_t speedR) {
	if (this->isalivePin(pin2) == true && _howmanyByte == 12) {
		servoLeft.writeMicroseconds(1500+speedL);
        servoRight.writeMicroseconds(1500+speedR);
        //Serial.println("   --> Driving both servos");
	} else if (this->isalivePin(pin2) == true && _howmanyByte == 8) {
		//Serial.println("   --> Driving left servo only");
		servoLeft.writeMicroseconds(1500+speedL);
        servoRight.writeMicroseconds(1500);	
	} else if (this->isalivePin(pin2) != true && _howmanyByte == 8) {
		//Serial.println("   --> Driving single servo");
        if (pin1 == _servoLeftPin) {
        	servoLeft.writeMicroseconds(1500+speedL);
		} else if (pin1 == _servoRightPin) {
			servoRight.writeMicroseconds(1500+speedL);
		}
	}
}

void MicroAbot::detachOtherServos(uint8_t newLeftPin, uint8_t newRightPin) {
    for (int i = 0; i < 3; i++) {
        uint8_t leftPin = SERVO_PINS[i][0];
        uint8_t rightPin = SERVO_PINS[i][1];
        if (leftPin != newLeftPin && rightPin != newRightPin) {
            if (servoLeft.attached() && _servoLeftPin == leftPin) {
                servoLeft.detach();
                _isServoLeftAttached = false;
            }
            if (servoRight.attached() && _servoRightPin == rightPin) {
                servoRight.detach();
                _isServoRightAttached = false;
            }
        }
    }
}

void MicroAbot::attachservoPins(uint8_t svoLeftPin, uint8_t svoRightPin) {
	if (!arePinsValidPair(svoLeftPin, svoRightPin)) {
        //Serial.println("Error: wrong servo pins");
        return;
    }
    // Detach all other servos except the new pair
    this->detachOtherServos(svoLeftPin, svoRightPin);
    
	// Attach new servo pins
    if (!servoLeft.attached()) {
        servoLeft.attach(svoLeftPin);
        _servoLeftPin = svoLeftPin;  // Update the pin number
        _isServoLeftAttached = true;
    }
    if (!servoRight.attached()) {
        servoRight.attach(svoRightPin);
        _servoRightPin = svoRightPin;  // Update the pin number
        _isServoRightAttached = true;
    }
}

void MicroAbot::servoDetach(uint8_t pin) {
	if ((_servoAnglePin != pin && _servoLeftPin != pin && _servoRightPin != pin) || (!_isServoStandardAttached && !_isServoLeftAttached && !_isServoRightAttached)) {
        Serial.println("Error: No servo is engaged on this pin");
        return;
    }
	if (_servoAnglePin == pin && _isServoStandardAttached) {
        servoStandard.detach();
        _isServoStandardAttached = false;
        //Serial.println(" Standard servo detached ... ");
    }
    else if (_servoLeftPin == pin && _isServoLeftAttached) {
        servoLeft.detach();
        _isServoLeftAttached = false;
        //Serial.println(" Left servo detached ... ");
    }
    else if (_servoRightPin == pin && _isServoRightAttached) {
        servoRight.detach();
        _isServoRightAttached = false;
        //Serial.println(" Right servo detached ... ");
    }
}

void MicroAbot::digitalWriteCommand(uint8_t pin, uint8_t state) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, (state != 2) ? HIGH : LOW);
}

void MicroAbot::analogWriteCommand(uint8_t pin, uint16_t value) {
    if (this->currentI2CState == I2C_IDLE) {
        analogWrite(pin, value); 
    }
}

uint32_t MicroAbot::digitalReadCommand(uint8_t pin) {
    pinMode(pin, INPUT);
	return static_cast<uint32_t>(digitalRead(pin));
}

void MicroAbot::toneCommand(uint8_t pin, uint16_t frequency, uint16_t duration) {
    tone(pin, frequency, duration);
}

uint32_t MicroAbot::pulseInCommand(uint8_t pin, uint8_t state) {
    pinMode(pin, INPUT);
    return pulseIn(pin, state);
}

void MicroAbot::pulseOutCommand(uint8_t pin, uint16_t duration) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);
    delayMicroseconds(duration);
    digitalWrite(pin, LOW);
}

uint32_t MicroAbot::pulseCountCommand(uint8_t pin, uint16_t duration) {
    pinMode(pin, INPUT);
    uint32_t startTime = micros();
    uint32_t endTime = startTime + static_cast<uint32_t>(duration);
    uint32_t count = 0;

    while (micros() < endTime) {
        if (digitalRead(pin) == HIGH) {
            count++;
            while (digitalRead(pin) == HIGH);
        }
    }
	return count;
}

uint32_t MicroAbot::irDetect(uint8_t irLedPin, uint8_t irReceiverPin, uint16_t frequency) {
	_irLedPin = irLedPin;
	_irReceiverPin = irReceiverPin;
	pinMode(_irLedPin, OUTPUT);
    pinMode(_irReceiverPin, INPUT);
    tone(_irLedPin, frequency, 8);
    
	unsigned long startTime = millis();
    while(millis() - startTime < 1);
    
    uint8_t _lastReadValue_ir = digitalRead(_irReceiverPin);
    
    startTime = millis();
    while(millis() - startTime < 1);
    
    return static_cast<uint32_t>(_lastReadValue_ir);
}

void MicroAbot::measureDistanceForFrequency(IRSensorData& sensor, unsigned int frequency) {
    pinMode(sensor.irLedPin, OUTPUT);
    tone(sensor.irLedPin, frequency, 8); 

    unsigned long startTime = micros();
    while (micros() - startTime < 1000);  

    pinMode(sensor.irReceivePin, INPUT);
    uint8_t readValue = digitalRead(sensor.irReceivePin);

	startTime = micros();
    while (micros() - startTime < 1000); 

    sensor.distance += static_cast<uint32_t>(readValue); 
}

