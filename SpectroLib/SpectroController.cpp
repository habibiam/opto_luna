/*
 * SpectroController.cpp
 *
 *  Created on: Nov 16, 2016
 *      Author: clawton
 */

#include "SpectroController.h"

#include <iostream>
#include <stdexcept>
#include <sstream>
#include <string.h>
#include <stdint.h>


#include "dln_generic.h"
#include "dln_gpio.h"
#include "dln_spi_master.h"
#include "dln_pwm.h"




namespace SpectroLib {

SpectroController::SpectroController() :
		initialized(false),
		handle(HDLN_INVALID_HANDLE),
		port(0)
{
	DLN_RESULT result = DlnConnect("localhost", DLN_DEFAULT_SERVER_PORT);
	if (!DLN_SUCCEEDED(result)) {
		throw std::runtime_error("Could not connect to DLN_SRV.  Is it running?");
	}

	//std::cout << "Connected to DLN_SRV on localhost." << std::endl;

	result = DlnOpenDevice(port, &handle);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		throw std::runtime_error("Could not open DLN device 0.");
	}

	uint16_t conflict=0;
	result = DlnSpiMasterEnable(handle, port, &conflict);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterEnable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	result = DlnPwmDisable(handle, port);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnPwmDisable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	uint32_t frequency = 24 * 1000000; //24MHz
	uint32_t actual_frequency = 0;
	result = DlnSpiMasterSetFrequency(handle, port, frequency, &actual_frequency);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrequency() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	result = DlnSpiMasterSetMode(handle, port, DLN_SPI_MASTER_CPOL_0|DLN_SPI_MASTER_CPHA_1);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetMode() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	uint8_t channel = 0;
	result = DlnPwmChannelEnable(handle, port, channel);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetMode() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	uint8_t frame_size = 8;
	result = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	result = DlnSpiMasterSSBetweenFramesDisable(handle, port);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSSBetweenFramesDisable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}


	uint8_t SS = 0xFE; // Set select slave 11111110 (active when low)
	result = DlnSpiMasterSetSS(handle, port, SS);
	if (!DLN_SUCCEEDED(result)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetSS() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	initialized = true;

}

SpectroController::~SpectroController()
{
	initialized = false;

	return; // Hmmm the below is causing a hang.

	if (handle != HDLN_INVALID_HANDLE) {
		DlnCloseHandle(handle);
	    handle = HDLN_INVALID_HANDLE;
	}

	DlnDisconnectAll();
}


int SpectroController::readSerialNumber()
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	uint8_t frame_size = 8;
	DLN_RESULT fsresult = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(fsresult)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << fsresult;
		throw std::runtime_error(ss.str());
	}

	uint16_t array_element_count = 3;
	uint8_t *write_buffer = new uint8_t[array_element_count];
	uint8_t *read_buffer = new uint8_t[array_element_count];

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);


	// See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	// array elements = 3: address, LSB_high, LSB_low.
	// address format: 6 register address bits, 1 R/W bit, 1 Don't Care bit. (R/W: 1 = read, 0 = write)

	write_buffer[0] =  0x06; //00000110
	write_buffer[1] =  0;
	write_buffer[2] =  0;

	read_buffer[0] =  0x06; //00000110
	read_buffer[1] =  0;
	read_buffer[2] =  0;


	DLN_RESULT result = -1;

	result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterReadWrite() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	// 47111
	union NC
	{
		uint16_t n;
		unsigned char c[2];
	};

	NC nc;

	nc.c[0] = read_buffer[2];
	nc.c[1] = read_buffer[1];

	uint16_t id = nc.n;

	return static_cast<int>(id);



}

void SpectroController::SetExposureMS(uint32_t exposure)
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	// 1ms = 1000000ns
	// Exposure register is in 200ns units.

	uint8_t frame_size = 8;
	DLN_RESULT fsresult = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(fsresult)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << fsresult;
		throw std::runtime_error(ss.str());
	}


	uint32_t write_value = (exposure * 1000000) / 200;

	uint16_t array_element_count = 3;
	uint8_t *write_buffer = new uint8_t[array_element_count];
	uint8_t *read_buffer = new uint8_t[array_element_count];

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);

	// See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	// Write LSB of exposure into address 9;
	// array elements = 3: address, LSB_high, LSB_low.
	// address format: 6 register address bits, 1 R/W bit, 1 Don't Care bit. (R/W: 1 = read, 0 = write)

	write_buffer[0] =  0x24; //00100100
	write_buffer[1] = (write_value & 0x000000FF);
	write_buffer[2] = (write_value & 0x0000FF00) >> 8;


	DLN_RESULT result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterSSBetweenFramesDisable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);

	// Write MSB of exposure into address 10;
	// array elements = 3: address, LSB_high, LSB_low.
	write_buffer[0] = 0x28; // See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	write_buffer[1] = (write_value & 0xFF000000) >> 24;
	write_buffer[2] = (write_value & 0x00FF0000) >> 16;


	result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterSSBetweenFramesDisable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}



	delete [] write_buffer;
	delete [] read_buffer;


}


int SpectroController::getPixelsPerImage()
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	uint8_t frame_size = 8;
	DLN_RESULT fsresult = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(fsresult)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << fsresult;
		throw std::runtime_error(ss.str());
	}

	uint16_t array_element_count = 3;
	uint8_t *write_buffer = new uint8_t[array_element_count];
	uint8_t *read_buffer = new uint8_t[array_element_count];

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);


	// See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	// array elements = 3: address, LSB_high, LSB_low.
	// address format: 6 register address bits, 1 R/W bit, 1 Don't Care bit. (R/W: 1 = read, 0 = write)

	write_buffer[0] =  0x16; //00010110
	write_buffer[1] =  0;
	write_buffer[2] =  0;

	read_buffer[0] =  0x16; //00010110
	read_buffer[1] =  0;
	read_buffer[2] =  0;


	DLN_RESULT result = -1;

	result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterReadWrite() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	// 47111
	union NC
	{
		uint16_t n;
		unsigned char c[2];
	};

	NC nc;

	nc.c[0] = read_buffer[2];
	nc.c[1] = read_buffer[1];

	uint16_t id = nc.n;

	return static_cast<int>(id);



}

int SpectroController::getNumPixelsReady()
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	uint8_t frame_size = 8;
	DLN_RESULT fsresult = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(fsresult)) {
		DlnDisconnectAll();
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << fsresult;
		throw std::runtime_error(ss.str());
	}

	uint16_t array_element_count = 3;
	uint8_t *write_buffer = new uint8_t[array_element_count];
	uint8_t *read_buffer = new uint8_t[array_element_count];

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);


	// See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	// array elements = 3: address, LSB_high, LSB_low.
	// address format: 6 register address bits, 1 R/W bit, 1 Don't Care bit. (R/W: 1 = read, 0 = write)

	write_buffer[0] =  0x32; //00110010
	write_buffer[1] =  0;
	write_buffer[2] =  0;

	read_buffer[0] =  0x32; //00110010
	read_buffer[1] =  0;
	read_buffer[2] =  0;


	DLN_RESULT result = -1;

	result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterReadWrite() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	// 47111
	union NC
	{
		uint16_t n;
		unsigned char c[2];
	};

	NC nc;

	nc.c[0] = read_buffer[2];
	nc.c[1] = read_buffer[1];

	uint16_t id = nc.n;

	return static_cast<int>(id);



}


void SpectroController::ResetSpectroBuffers()
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}


	uint8_t frame_size = 16;
	DLN_RESULT result = DlnSpiMasterSetFrameSize(handle, port, frame_size);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnSpiMasterSetFrameSize() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	result = DlnSpiMasterSSBetweenFramesDisable(handle, port);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnSpiMasterSSBetweenFramesDisable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	uint16_t array_element_count = 2;
	uint8_t *write_buffer = new uint8_t[array_element_count];
	uint8_t *read_buffer = new uint8_t[array_element_count];

	memset(write_buffer, 0, sizeof(uint8_t) * array_element_count);
	memset(read_buffer, 0, sizeof(uint8_t) * array_element_count);

	// See Document Digital Image Sensor Board (DISB) for S11639-01 (DISB-101)
	// array elements = 2: address, 5 bits.
	// address format: 6 register address bits, 1 R/W bit, 1 Don't Care bit. (R/W: 1 = read, 0 = write)

	write_buffer[0] =  0x20; //00100000
	write_buffer[1] = 0x10; // Only care about lower 5 bits (bit 4 = soft reset)



	result = DlnSpiMasterReadWrite(handle, port, array_element_count, write_buffer, read_buffer);
	if (!DLN_SUCCEEDED(result)) {
		delete [] write_buffer;
		delete [] read_buffer;
		std::stringstream ss;
		ss << "DlnSpiMasterReadWrite() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	delete [] write_buffer;
	delete [] read_buffer;
}




void SpectroController::Capture(uint16_t *outData, uint16_t *outDataSize)
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	ResetSpectroBuffers();

	// delay between slave select = 208
	uint32_t delay = 208;
	uint32_t actual_delay = 0;
	DLN_RESULT result = DlnSpiMasterSetDelayBetweenSS(handle, port, delay, &actual_delay);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnSpiMasterSetDelayBetweenSS() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	result = DlnSpiMasterSSBetweenFramesEnable(handle, port);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnSpiMasterSSBetweenFramesEnable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	// a clock signal on one of the DLN I/O pins is used to trigger DISB over SPI. This signal is ignored if a measurement is in progress.
	// set trig frequency (for automatic triggering) handle 0, port 0, channel 0, frequency: e.g. 100Hz
	// PWN 0 CHANNEL 0 is on DLN SUBD #8, which is connected to DISB EXTTRIG-1
	uint32_t frequency = 100;
	uint32_t actual_frequency = 0;
	result = DlnPwmSetFrequency(handle, port, 0, frequency, &actual_frequency);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnPwmSetFrequency() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}


	// duty cycle 50
	double duty_cycle = 50;
	double actual_duty_cycle = 50;
	result = DlnPwmSetDutyCycle(handle, port, 0, duty_cycle, &actual_duty_cycle);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnPwmSetDutyCycle() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}


	// enable pwm
	uint16_t conflict = 0;
	result = DlnPwmEnable(handle, port, &conflict);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnPwmEnable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}

	// Set to return image data.
	// slave select DISB image; 11111101
	uint8_t SS = 0xFD;
	result = DlnSpiMasterSetSS(handle, port, SS);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnSpiMasterSetSS() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}



	// enable DLN pin 1; i.e. SUBD #2: "Data ready"
	uint8_t pin = 1;
	result = DlnGpioPinEnable(handle, pin);
	if (!DLN_SUCCEEDED(result)) {
		std::stringstream ss;
		ss << "DlnGpioPinEnable() failed.  Result=" << result;
		throw std::runtime_error(ss.str());
	}




	uint16_t count = 2048;
	uint16_t *read_buffer = new uint16_t[count];
	memset(read_buffer, 0, sizeof(uint16_t) * count);


	uint16_t chunk_size = 128;
	uint16_t *write_buffer = new uint16_t[chunk_size];
	uint16_t *chunk_buffer = new uint16_t[chunk_size];

	int16_t tot_read = 0;
	while (tot_read < count)
	{

		memset(write_buffer, 0, sizeof(uint16_t) * chunk_size);
		memset(chunk_buffer, 0, sizeof(uint16_t) * chunk_size);


		bool dataReady = false;
		while(dataReady == false) {

			// keep polling the data ready pin until DISB reports data ready
			uint8_t value = 0;
			result = DlnGpioPinGetVal(handle, pin, &value);
			if (!DLN_SUCCEEDED(result)) {
				std::stringstream ss;
				ss << "DlnGpioPinGetVal() failed.  Result=" << result;
				throw std::runtime_error(ss.str());
			}

			if(value != 0) dataReady = true;
		}

		//int num_to_read = getNumPixelsReady();

		int num_to_read = chunk_size;
		//result = DlnSpiMasterReadWrite16(handle, port, chunk_size, write_buffer, chunk_buffer);
		result = DlnSpiMasterReadWrite16(handle, port, num_to_read, write_buffer, chunk_buffer);
		if (!DLN_SUCCEEDED(result)) {
			//delete [] outData;
			delete [] write_buffer;
			std::stringstream ss;
			ss << "DlnSpiMasterReadWrite16() failed.  Result=" << result;
			throw std::runtime_error(ss.str());
		}

//		memcpy(read_buffer + tot_read, chunk_buffer, chunk_size * sizeof(uint16_t));
//		tot_read+=chunk_size;
		memcpy(read_buffer + tot_read, chunk_buffer, num_to_read * sizeof(uint16_t));
		tot_read+=num_to_read;
	}

	memcpy(outData, read_buffer, sizeof(uint16_t) * count);





	delete [] write_buffer;

}







std::string SpectroController::GetDeviceId()
{
	if (!initialized)
	{
		std::stringstream ss;
		ss << "SpectroLib library not initialized.";
		throw std::runtime_error(ss.str());
	}

	uint32_t id;
	DLN_RESULT result = DlnGetDeviceId(handle, &id);
	if (!DLN_SUCCEEDED(result)) {
		throw std::runtime_error("Failed to GetDevice Id");
	}

	std::stringstream ss;
	ss << id;
	return ss.str();
}

} /* namespace SpectroLib */
