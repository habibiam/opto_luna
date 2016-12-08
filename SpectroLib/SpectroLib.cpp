/*
 * SpectgroLib.cpp
 *
 *  Created on: Dec 8, 2016
 *      Author: optokey
 */

#include "SpectroLib.h"
#include "SpectroController.h"

#include <iostream>
#include <fstream>

#include <stdexcept>
#include <memory>
#include <chrono>
#include <thread>
#include <string>
#include <sstream>
#include <ctime>
#include <iomanip>



std::shared_ptr<SpectroLib::SpectroController> controller(nullptr);

//SpectroLib::SpectroController *controller = nullptr;


bool Initialize()
{
	try {
		controller = std::make_shared<SpectroLib::SpectroController>();
		//controller = new SpectroLib::SpectroController();
	}
	catch (std::runtime_error &ex)
	{
		//cout << ex.what();
		return false;
	}

	return true;
}

bool ReadSerialNumber(int *SerialNumber)
{
	if (SerialNumber == nullptr)
	{
		return false;
	}

	try {
		*SerialNumber = controller->readSerialNumber();
	}
	catch (std::runtime_error &ex)
	{
		//cout << ex.what();
		return false;
	}

	return true;
}

bool SetExposureMS(uint32_t exposure)
{
	try {
		controller->SetExposureMS(exposure);
	}
	catch (std::runtime_error &ex)
	{
		//cout << ex.what();
		return false;
	}

	return true;
}

bool CaptureSingleSpectrum(uint16_t *output_data, uint16_t *output_size)
{
	if (output_data == nullptr || output_size == nullptr)
	{
		return false;
	}

	try {
		controller->Capture(output_data, output_size);
	}
	catch (std::runtime_error &ex)
	{
		//cout << ex.what();
		return false;
	}

	return true;
}

bool CaptureContinuousSpectrum(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS)
{
	if (filename == nullptr)
	{
		return false;
	}

	std::ofstream myfile;
	myfile.open (filename, std::ios::trunc);
	if (myfile.is_open() == false)
	{
		return false;
	}

	std::stringstream ss;

	ss << "Pixels,,,";
	int c=2048;
	for(int i =0; i < c; i++)
	{
		ss << i;
		if (i < c-1)
			ss << ",";
	}
	ss << std::endl;

	ss << "Wavelength,,,";
	for(int i =0; i < c; i++)
	{
		ss << 0;
		if (i < c-1)
			ss << ",";
	}
	ss << std::endl;

	myfile << ss.str();
	ss.str("");


	auto start_time = std::chrono::high_resolution_clock::now();
	auto current_time = std::chrono::high_resolution_clock::now();
	auto elapsedMS = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();

	while (elapsedMS < durationMS)
	{
		uint16_t size = 2048;
		uint16_t data[size];

		CaptureSingleSpectrum(&data[0], &size);


		std::this_thread::sleep_for(std::chrono::milliseconds(delayBetweenMS));

		current_time = std::chrono::high_resolution_clock::now();
		elapsedMS = std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count();


		std::time_t t = std::time(nullptr);
		std::tm tm = *std::localtime(&t);
		char tstr[64];

		std::strftime(tstr, sizeof(tstr), "%m/%d/%Y,%r", &tm);
		ss << tstr << "," << t;
		for(int i =0; i < c; i++)
		{
			ss << data[i];
			if (i < c-1)
				ss << ",";
		}
		ss << std::endl;
		myfile << ss.str();
		ss.str("");
	}

	myfile.close();


	return true;


}











