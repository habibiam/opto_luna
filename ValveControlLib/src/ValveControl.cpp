/*
 * ValveControl.cpp
 *
 *  Created on: Dec 12, 2016
 *      Author: clawton
 */

#include "ValveControl.h"

#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <sstream>
#include <cassert>
#include <iostream>

#include <sys/ioctl.h>


namespace ValveControlLib {

//-------------------------------------------------------------------------

#define SPI_ADDRESS		12		// Where did 12 come from? We saw it on the Windows LabSmith GUI tool!

#define CB_GETSTATUS	0x1A
#define CV_SETVALVES	0x07


// NOTE!!! For this Optokey code, we assume only 1 (one) valve is attached and it
// will *ALWAYS* be in position 4!!!!


ValveControl::ValveControl() :
		m_fd(-1),
		m_nAddress(SPI_ADDRESS),
		m_nBytes(0)
{
}

ValveControl::~ValveControl()
{
	if (m_fd != -1)
	{
		close(m_fd);
		m_fd = -1;
	}
}

std::string ValveControl::GetLastErrorMsg()
{
	return lastErrorMsg;
}


bool ValveControl::Initialize(const std::string serialPort)
{
    lastErrorMsg = "OK";

	m_fd = open (serialPort.c_str(), O_RDWR | O_NOCTTY | O_SYNC);
	if (m_fd < 0)
	{
    		std::stringstream ss;
            ss << "error " << errno << " opening " << serialPort << " : " << strerror (errno);
            lastErrorMsg = ss.str();
	        return false;
	}

	int r = 0;
 	r = set_interface_attribs (m_fd, B57600, 0);  // set speed to 57600 bps, 8n1 (no parity)
 	if (r < 0) {
 		close(m_fd);
 		return false;
 	}
//	r = set_blocking (fd, 0); // set no blocking
// 	if (r < 0) {
// 		close(fd);
// 		return false;
// 	}

//	write (fd, "hello!\n", 7);           // send 7 character greeting
//
//	usleep ((7 + 25) * 100);             // sleep enough to transmit the 7 plus
//	                                     // receive 25:  approx 100 uS per char transmit
//	char buf [100];
//	int n = read (fd, buf, sizeof buf);  // read up to 100 characters if ready to read

	return true;

}


int ValveControl::set_interface_attribs (int fd, int speed, int parity)
{
        struct termios tty;
        memset (&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
        		std::stringstream ss;
                ss << "error " << errno << " from tcgetattr";
                lastErrorMsg = ss.str();
                return -1;
        }

        cfsetospeed (&tty, speed);
        cfsetispeed (&tty, speed);

        tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;     // 8-bit chars
        // disable IGNBRK for mismatched speed tests; otherwise receive break
        // as \000 chars
        tty.c_iflag &= ~IGNBRK;         // disable break processing
        tty.c_lflag = 0;                // no signaling chars, no echo,
                                        // no canonical processing
        tty.c_oflag = 0;                // no remapping, no delays
        tty.c_cc[VMIN]  = 0;            // read doesn't block
        tty.c_cc[VTIME] = 5;            // 0.5 seconds read timeout

        tty.c_iflag &= ~(IXON | IXOFF | IXANY); // shut off xon/xoff ctrl

        tty.c_cflag |= (CLOCAL | CREAD);// ignore modem controls,
                                        // enable reading
        tty.c_cflag &= ~(PARENB | PARODD);      // shut off parity
        tty.c_cflag |= parity;
        tty.c_cflag &= ~CSTOPB;
        tty.c_cflag &= ~CRTSCTS;

        if (tcsetattr (fd, TCSANOW, &tty) != 0)
        {
        		std::stringstream ss;
                ss << "error " << errno << " from tcsetattr";
                lastErrorMsg = ss.str();

                return -1;
        }
        return 0;
}

void ValveControl::set_blocking (int fd, int should_block)
{
        struct termios tty;
        memset (&tty, 0, sizeof tty);
        if (tcgetattr (fd, &tty) != 0)
        {
			std::stringstream ss;
			ss << "error " << errno << " from tggetattr";
			lastErrorMsg = ss.str();
			return;
        }

        tty.c_cc[VMIN]  = should_block ? 1 : 0;
        tty.c_cc[VTIME] = 5;            // 0.5 seconds read timeout

        if (tcsetattr (fd, TCSANOW, &tty) != 0)
        {
			std::stringstream ss;
			ss << "error " << errno << " setting term attributes";
			lastErrorMsg = ss.str();
        }
}




void ValveControl::Create(BYTE dest, const BYTE* pdata, unsigned int bytes, const char * desc,
	char * pUserData, int timeout, int retries)
{
	//m_bFlags = 0;
	//m_pUserData = pUserData;
	//m_nResp = 0;
	//m_nRetries = retries;
	//m_nTimeout = timeout;

	//if (desc) _tcscpy(m_StatusDesc, desc);
	//else _tcscpy(m_StatusDesc, _T("Working..."));

	int i = 0;
	BYTE* pd = m_pCommand;
	FormatCommand(dest, pd,i, pdata, bytes);
	m_nBytes = pd - m_pCommand;
}

void ValveControl::FormatCommand(BYTE dest, BYTE*& pd, int& i, const BYTE* pdata, unsigned int length)
{
	BYTE checksum = 0;
		BYTE* start = pd;

		*(pd++) = '%';
		checksum -= *(pd++) = dest<<1;
		checksum -= *(pd++) = (BYTE)(length + 1);
		BYTE* end = pd+length;
		while (pd < end) checksum -= *(pd++) = *(pdata++);
		*(pd++) = checksum;
		i = pd - start;
}


bool ValveControl::DoCommand()
{
	int num_written = write(m_fd, m_pCommand, m_nBytes);
	if (num_written < 0)
	{
		std::stringstream ss;
		ss << "error " << errno << " from write";
		lastErrorMsg = ss.str();

		return false;
	}

	assert(num_written == static_cast<int>(m_nBytes));

	usleep(50000);

	int count;
	ioctl(m_fd, FIONREAD, &count);

	if (count)
	{
		memset(m_pResponse, 0, 256);
		int num_read = read(m_fd, m_pResponse, count);
		if (num_read < 0)
		{
			std::stringstream ss;
			ss << "error " << errno << " from read";
			lastErrorMsg = ss.str();
			return false;
		}
	}

	return true;
}



//bool ValveControl::CmdScanValves()
//{
////	if (!IsOnline()) return false;
////
////	if (m_nFirmwareVer < 0xB)
////	{
////		m_bV1Missing = false;//assume 4 valves are present
////		m_bV2Missing = false;
////		m_bV3Missing = false;
////		m_bV4Missing = false;
////		return true;
////	}
//
//	BYTE	command[12];
//	BYTE	*pc = &command[0];
//
//	*pc = BYTE(CV_SCANVALVES);
//
//	CCommand* pCommand = m_pInterface->LockCommand();
//	pCommand->Create( m_nAddress, command, 1, L"Scanning for valves...");
//	bool retval = m_pInterface->DoCommand();
//	if (retval)
//	{
//		BYTE s = pCommand->m_pResponse[2] ;
//		m_bV1Missing = (s&0x1)!= 0;
//		m_bV2Missing = (s&0x2)!= 0;
//		m_bV3Missing = (s&0x4)!= 0;
//		m_bV4Missing = (s&0x8)!= 0;
//	}
//
//	m_pInterface->UnlockCommand();
//
//	return retval;
//}




bool ValveControl::CmdGetAllStatus(int &V1Status, int& V2Status, int& V3Status, int& V4Status)
{
	if (m_fd < 0) return false;
	//this is an efficient state poll.
	BYTE	command[12];
	BYTE	*pc = &command[0];

	*pc = CB_GETSTATUS;

	//Create(BYTE dest, const BYTE* pdata, unsigned int bytes, const char * desc,
	//	char * pUserData, int timeout, int retries)

	Create( m_nAddress, command, 1, "Reading 4VM Status...", NULL, 200, 0);
	bool retval = DoCommand();

	if (retval)
	{
		BYTE s = m_pResponse[2];
		V4Status = s&0x0F;
		s>>=4;
		V3Status = s&0x0F;
		s = m_pResponse[3];
		V2Status = s&0x0F;
		s>>=4;
		V1Status = s& 0x0F;
//		bool m_bDone = ((V1Status&0x4)==0)
//			&&((V2Status&0x4)==0)
//			&&((V3Status&0x4)==0)
//			&&((V4Status&0x4)==0);

		//std::cout << "Get Status Done:" << m_bDone << std::endl;

		lastErrorMsg = "OK";

	}

	return retval;
}


bool ValveControl::CmdSetAllValves(int V1Set, int V2Set, int V3Set, int V4Set)
{
	if (m_fd < 0) return false;

	BYTE t = V1Set&0x03;
	t<<=2;
	t|= V2Set&0x03;
	t<<=2;
	t|= V3Set&0x03;
	t<<=2;
	t|= V4Set&0x03;
	BYTE	command[12];
	BYTE	*pc = &command[0];

	*(pc++) = CV_SETVALVES;
	*(pc) = t;

	Create( m_nAddress, command, 2, "Setting 4VM state...", NULL, 200, 0);

	bool retval = DoCommand();
	if (retval)
	{

		int V1=STATE_UNKNOWN;
		int V2=STATE_UNKNOWN;
		int V3=STATE_UNKNOWN;
		int V4=STATE_UNKNOWN;

		int count = 0;
		int max_tries = 4 * 10; // 10 seconds

		while (V1 != V1Set && V2 != V2Set && V3 != V3Set && V4 != V4Set && count < max_tries)
		{
			usleep(static_cast<int>(100000.0 * 2.5)); // 0.25 seconds this is so the script status is correct immediately following a motion to the original valve position
			CmdGetAllStatus(V1, V2, V3, V4);
			count++;
		}

		if (count >= max_tries)
		{
			lastErrorMsg = "Timed out waiting for movement to complete.";
			return false;
		}

	}
	return retval;
}

bool ValveControl::CmdGetStatus(int &VStatus)
{
	int V1=0;
	int V2=0;
	int V3=0;
	int V4=0;

	bool ret = CmdGetAllStatus(V1, V2, V3, V4);

	VStatus = V4;
	return ret;
}

bool ValveControl::CmdSetValve(int VSet)
{
	return CmdSetAllValves(VSet,VSet,VSet,VSet);

}


} /* namespace ValveControlLib */
