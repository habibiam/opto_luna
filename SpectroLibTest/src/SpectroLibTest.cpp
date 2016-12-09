//============================================================================
// Name        : SpectroLibTest.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <stdexcept>

#include <stdint.h>
#include <unistd.h>
#include "SpectroLib.h"

using namespace std;



int main() {

	char error[1024];
	bool err = false;
	err = Initialize();
	if (!err)
	{
		GetLastErrorMsg((char *)&error, 1024);
		std::cout << "Error: " << error << std::endl;
	}

	int sn;
	err = ReadSerialNumber(&sn);
	if (!err)
	{
		GetLastErrorMsg((char *)&error, 1024);
		std::cout << "Error: " << error << std::endl;
	}

	std::cout << "SerialNumber: " << sn << std::endl;

	err = SetExposureMS(250);
	if (!err)
	{
		GetLastErrorMsg((char *)&error, 1024);
		std::cout << "Error: " << error << std::endl;
	}

	//uint16_t size = 2048;
	//uint16_t data[size];

	//CaptureSingleSpectrum(&data[0], &size);

//	for (int i=0; i<size; i++) {
//		std::cout << i << "," << data[i] << std::endl;
//	}
//	std::cout << std::endl;
//	std::cout.flush();


	uint32_t delay_between = 0;
	uint32_t duration_ms = 1000 * 10; // capture for 10 seconds.
	CaptureContinuousSpectrum("foo.csv", delay_between, duration_ms);

	int count=0;
	while (IsCaptureContinuousSpectrumDone() == false)
	{
		usleep(200000);
		count++;
//		if (count > 50)
//		{
//			ExitCaptureContinuousSpectrum();
//		}
	}
	GetLastErrorMsg((char *)&error, 1024);
	std::cout << "A) Error: " << error << std::endl;

	std::cout << "Done." << std::endl;

	return 0;
}
