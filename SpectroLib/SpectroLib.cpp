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
#include <atomic>

#include <string.h>
#include <unistd.h>



std::shared_ptr<SpectroLib::SpectroController> controller(nullptr);
std::thread continuousCaptureThread;
bool continuousCaptureThreadRetCode = false;
std::atomic<bool> continuousCaptureThreadExitFlag(false);
std::atomic<bool> continuousCaptureThreadDone(true);

std::string lastError;


void CaptureContinuousSpectrumThread(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS);

bool Initialize()
{
	try {
		lastError = "OK";
		controller = std::make_shared<SpectroLib::SpectroController>();
	}
	catch (std::runtime_error &ex)
	{
		lastError = ex.what();
		return false;
	}

	return true;
}

void GetLastErrorMsg(char *msg, int msg_size)
{
	strncpy(msg, lastError.c_str(), msg_size);
}

bool ReadSerialNumber(int *SerialNumber)
{
	lastError = "OK";
	if (SerialNumber == nullptr)
	{
		lastError = "Invalid Argument";
		return false;
	}

	*SerialNumber = -1;
	if (controller == nullptr)
	{
		lastError = "SpectroLib library not initialized.";
		return false;
	}

	try {
		*SerialNumber = controller->readSerialNumber();
	}
	catch (std::runtime_error &ex)
	{
		lastError = ex.what();
		return false;
	}

	return true;
}

bool SetExposureMS(uint32_t exposure)
{
	lastError = "OK";
	if (controller == nullptr)
	{
		lastError = "SpectroLib library not initialized.";
		return false;
	}

	try {
		controller->SetExposureMS(exposure);
	}
	catch (std::runtime_error &ex)
	{
		lastError = ex.what();
		return false;
	}

	return true;
}

bool CaptureSingleSpectrum(uint16_t *output_data, uint16_t *output_size)
{
	lastError = "OK";
	if (controller == nullptr)
	{
		lastError = "SpectroLib library not initialized.";
		return false;
	}

	if (output_data == nullptr || output_size == nullptr)
	{
		lastError = "Invalid Argument";
		return false;
	}

	try {
		controller->Capture(output_data, output_size);
	}
	catch (std::runtime_error &ex)
	{
		lastError = ex.what();
		return false;
	}

	return true;
}

bool CaptureContinuousSpectrum(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS)
{
	lastError = "OK";
	if (controller == nullptr)
	{
		lastError = "SpectroLib library not initialized.";
		return false;
	}

	if (filename == nullptr)
	{
		lastError = "Invalid Argument";
		return false;
	}


	continuousCaptureThread = std::thread(CaptureContinuousSpectrumThread, filename, delayBetweenMS, durationMS);
	continuousCaptureThread.detach();

	usleep(50000);

	return true;

}


void CaptureContinuousSpectrumThread(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS)
{
	continuousCaptureThreadDone = false;

	try
	{
		//std::cout << "Start  thread..." << std::endl;
		std::ofstream myfile;
		myfile.open (filename, std::ios::trunc);
		if (myfile.is_open() == false)
		{
			lastError = "Could not open output file.";
			//std::cout << lastError << std::endl;
			continuousCaptureThreadDone = true;
			return;
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

		bool error=false;
		while (elapsedMS < durationMS && continuousCaptureThreadExitFlag == false)
		{
			uint16_t size = 2048;
			uint16_t data[size];

			if (!CaptureSingleSpectrum(&data[0], &size))
			{
				// Don't change last error here.
				error = true;
				break;
			}


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
		if (error)
		{
			continuousCaptureThreadDone = true;
			//std::cout << lastError << std::endl;
			return;
		}

//		if (continuousCaptureThreadExitFlag)
//		{
//			std::cout << "Early exit!" << std::endl;
//		}

		continuousCaptureThreadDone = true;
//		std::cout << "Success exit" << std::endl;
	}
	catch (std::exception &ex)
	{
		lastError = ex.what();
		continuousCaptureThreadDone = true;
	}
}

bool IsCaptureContinuousSpectrumDone()
{
	return continuousCaptureThreadDone;
}

void ExitCaptureContinuousSpectrum()
{
	if (continuousCaptureThreadDone == false)
	{
		continuousCaptureThreadExitFlag = true;
		while (continuousCaptureThreadDone != true)
		{
			usleep(5000);
		}
		//continuousCaptureThread.join();
	}
}







