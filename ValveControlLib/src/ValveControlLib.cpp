/*
 * ValveControlLib.cpp
 *
 *  Created on: Dec 12, 2016
 *      Author: clawton
 */
 
 #include "ValveControlLib.h"
 #include "ValveControl.h"
 
 #include <string.h>

ValveControlLib::ValveControl theValve;

BOOL Initialize(const char *port)
{
	return theValve.Initialize(std::string(port)) ? 1 : 0;
}

void GetLastErrorMsg(char *msg, int msg_size)
{
	if (msg == NULL || msg_size == 0)
	{
		return;
	}
	
	std::string err = theValve.GetLastErrorMsg();
	
	strncpy(msg,err.c_str(), msg_size);
}

int GetStatus(void)
{
	int v=0;
	bool ret = theValve.CmdGetStatus(v);
	if (ret == false)
	{
		return 0;
	}
	else
	{
		return v;
	}
}

BOOL SetPosition(int pos)
{
	if (pos < STATE_UNKNOWN || pos > STATE_B)
	{
		return 0;
	}
	
	bool ret = theValve.CmdSetValve(pos);
	
	return ret ? 1 : 0;
}


