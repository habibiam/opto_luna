/*
 * ValveControl.h
 *
 *  Created on: Dec 12, 2016
 *      Author: clawton
 */

#ifndef SRC_VALVECONTROL_H_
#define SRC_VALVECONTROL_H_

#include <string>
#define BYTE unsigned char

namespace ValveControlLib {

#define STATE_UNKNOWN	0
#define STATE_UNCHANGED 0
#define STATE_A			1
#define STATE_CLOSED	2
#define STATE_B			3

class ValveControl {
public:
	ValveControl();
	virtual ~ValveControl();

	bool Initialize(const std::string serialPort);

	bool CmdGetStatus(int &VStatus);
	bool CmdSetValve(int VSet);

	std::string GetLastErrorMsg();


private:
	int set_interface_attribs (int fd, int speed, int parity);
	void set_blocking (int fd, int should_block);

	std::string lastErrorMsg;
	int m_fd;

	BYTE m_pCommand[256];
	BYTE m_nAddress;
	BYTE m_pResponse[256];
	size_t m_nBytes;

	void Create(BYTE dest, const BYTE* pdata, unsigned int bytes, const char * desc,
		char *pUserData, int timeout, int retries);

	void FormatCommand(BYTE dest, BYTE*& pd, int& i, const BYTE* pdata, unsigned int length);

	bool DoCommand();

	bool CmdGetAllStatus(int &V1Status, int& V2Status, int& V3Status, int& V4Status);
	bool CmdSetAllValves(int V1Set, int V2Set, int V3Set, int V4Set);

};

} /* namespace ValveControlLib */

#endif /* SRC_VALVECONTROL_H_ */
