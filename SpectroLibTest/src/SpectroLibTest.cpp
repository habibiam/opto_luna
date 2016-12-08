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
#include "SpectroLib.h"

using namespace std;



int main() {

//	try {
//		SpectroLib::SpectroController controller;
//		controller.readSerailNumber();
//		controller.getPixelsPerImage();
//		controller.SetExposureMS(250);
//		controller.ResetSpectroBuffers();
//
//		uint16_t size = 2048;
//		uint16_t data[size];
//		controller.Capture(&data[0], &size);
//
//		for (int i=0; i<size; i++) {
//			std::cout << i << "," << data[i] << std::endl;
//		}
//		std::cout << std::endl;
//		std::cout.flush();
//
//
//		cout << "Done." << endl;
//	}
//	catch (std::runtime_error &ex)
//	{
//		cout << ex.what();
//	}

	Initialize();
	int sn;
	ReadSerialNumber(&sn);

	std::cout << "SerialNumber: " << sn << std::endl;

	SetExposureMS(250);

	uint16_t size = 2048;
	uint16_t data[size];

	//CaptureSingleSpectrum(&data[0], &size);

//	for (int i=0; i<size; i++) {
//		std::cout << i << "," << data[i] << std::endl;
//	}
//	std::cout << std::endl;
//	std::cout.flush();


	uint32_t delay_between = 0;
	uint32_t duration_ms = 5000;
	CaptureContinuousSpectrum("/home/optokey/foo.csv", delay_between, duration_ms);

	std::cout << "Done." << std::endl;

	return 0;
}
