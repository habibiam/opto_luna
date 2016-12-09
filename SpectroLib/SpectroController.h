/*
 * SpectroController.h
 *
 *  Created on: Nov 16, 2016
 *      Author: clawton
 */

#ifndef SPECTROCONTROLLER_H_
#define SPECTROCONTROLLER_H_

#include <string>

namespace SpectroLib {



class SpectroController {
public:
	SpectroController();
	virtual ~SpectroController();

	std::string GetDeviceId();
	void SetExposureMS(uint32_t exposure);
	void Capture(uint16_t *outData, uint16_t *outDataSize);

	int getPixelsPerImage();
	int readSerialNumber();

private:
	bool initialized;
	uint16_t handle;
	uint8_t port;

	void ResetSpectroBuffers();
	int getNumPixelsReady();

};

} /* namespace SpectroLib */

#endif /* SPECTROCONTROLLER_H_ */
