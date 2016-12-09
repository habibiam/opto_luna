/*
 * SprectroLib.h
 *
 *  Created on: Dec 8, 2016
 *      Author: optokey
 */

#ifndef SPECTROLIB_H_
#define SPECTROLIB_H_

#include <stdint.h>

#ifdef __cplusplus
#define BOOL bool
#else
#define BOOL int
#endif

#ifdef __cplusplus
extern "C" {
#endif



BOOL Initialize(void);
void GetLastErrorMsg(char *msg, int msg_size);
BOOL ReadSerialNumber(int *SerialNumber);
BOOL SetExposureMS(uint32_t exposure);
BOOL CaptureSingleSpectrum(uint16_t *output_data, uint16_t *output_size);

BOOL CaptureContinuousSpectrum(const char *filename, uint32_t delayBetweenMS, uint32_t durationMS);
BOOL IsCaptureContinuousSpectrumDone(void);
void ExitCaptureContinuousSpectrum(void);

#ifdef __cplusplus
}
#endif



#endif /* SPECTROLIB_H_ */
