//============================================================================
// Name        : LibSmithLibTest.cpp
// Author      : clawton@dlssolutions.com
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include "ValveControl.h"

using namespace std;

int main() {
	cout << "Start..." << endl;

	ValveControlLib::ValveControl valve;
	valve.Initialize("/dev/ttyUSB0");

	int V;

	valve.CmdGetStatus(V);
	cout << "Current Position: " << V << endl;

	cout << "Move to A...";
	valve.CmdSetValve(STATE_A);
	valve.CmdGetStatus(V);
	cout << V << endl;

	cout << "Move to B...";
	valve.CmdSetValve(STATE_B);
	valve.CmdGetStatus(V);
	cout << V << endl;

	cout << "Move to Closed...";
	valve.CmdSetValve(STATE_CLOSED);
	valve.CmdGetStatus(V);
	cout << V << endl;


	return 0;
}
