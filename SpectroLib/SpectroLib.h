/*
 * SprectroLib.h
 *
 *  Created on: Dec 8, 2016
 *      Author: optokey
 */

#ifndef SPECTROLIB_H_
#define SPECTROLIB_H_

#include <stdint.h>

extern "C" {



bool Initialize();
void GetLastErrorMsg(char *msg, int msg_size);
bool ReadSerialNumber(int *SerialNumber);
bool SetExposureMS(uint32_t exposure);
bool CaptureSingleSpectrum(uint16_t *output_data, uint16_t *output_size);

bool CaptureContinuousSpectrum(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS);
bool IsCaptureContinuousSpectrumDone();
void ExitCaptureContinuousSpectrum();


}



#endif /* SPECTROLIB_H_ */
