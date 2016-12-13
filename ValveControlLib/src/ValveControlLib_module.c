/*
 * ValveControlLib_module.cpp
 *
 *  Created on: Dec 12, 2016
 *      Author: clawton
 */

#include <Python.h>
#include "ValveControlLib.h"
#include <string.h>






static PyObject *
ValveControlLib_GetLastErrorMsg(PyObject *self)
{
    char msg[1024];
    int msg_size = 1024;
    GetLastErrorMsg(msg, msg_size);

    return Py_BuildValue("s", msg);
}




static PyObject *
ValveControlLib_Initialize(PyObject *self, PyObject *args)
{
	char *port;

	if (!PyArg_ParseTuple(args, "s", &port ))
	        return NULL;
    int ret;


    ret = Initialize(port);

    return Py_BuildValue("i", ret ? 1 : 0);
}



static PyObject *
ValveControlLib_GetStatus(PyObject *self)
{
    int status=GetStatus();

   	return Py_BuildValue("i", status);
}



static PyObject *
ValveControlLib_SetPosition(PyObject *self, PyObject *args)
{
	int pos=0;

	if (!PyArg_ParseTuple(args, "i", &pos ))
	        return NULL;

    BOOL ret = SetPosition(pos);

    return Py_BuildValue("i", ret ? 1 : 0);
}







static PyMethodDef ValveControlLibMethods[] = {
    {"Initialize",  (PyCFunction)ValveControlLib_Initialize, METH_VARARGS, "Initialize the ValveControlLib library."},
    {"GetLastErrorMsg",  (PyCFunction)ValveControlLib_GetLastErrorMsg, METH_NOARGS, "Get the last error message reported by the ValveControlLib."},
    {"GetStatus",  (PyCFunction)ValveControlLib_GetStatus, METH_NOARGS, "Get the status position of the valve."},
    {"SetPosition",  (PyCFunction)ValveControlLib_SetPosition, METH_VARARGS, "Sets position of the valve."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};



PyMODINIT_FUNC
initValveControlLib_module(void)
{
	 PyObject *m = Py_InitModule("ValveControlLib_module", ValveControlLibMethods);

	 PyModule_AddIntConstant(m, "STATE_UNKNOWN", 0);
	 PyModule_AddIntConstant(m, "STATE_UNCHANGED", 0);
	 PyModule_AddIntConstant(m, "STATE_A", 1);
	 PyModule_AddIntConstant(m, "STATE_CLOSED", 2);
	 PyModule_AddIntConstant(m, "STATE_B", 3);
}


