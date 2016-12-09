#include <Python.h>
#include "SpectroLib.h"

static PyObject *
SpectroLib_Initialize(PyObject *self)
{
    int ret;


    ret = Initialize();

    return Py_BuildValue("i", ret ? 1 : 0);
}



static PyObject *
SpectroLib_GetLastErrorMsg(PyObject *self)
{
    char msg[1024];
    int msg_size = 1024;
    GetLastErrorMsg(msg, msg_size);

    return Py_BuildValue("s", msg);
}

static PyObject *
SpectroLib_ReadSerialNumber(PyObject *self)
{
    int sn;
    ReadSerialNumber(&sn);
    char msg[64];
    sprintf(msg, "%d", sn);


    return Py_BuildValue("s", msg);
}


static PyObject *
SpectroLib_SetExposureMS(PyObject *self, PyObject *args)
{
    int exposure;
	if (!PyArg_ParseTuple(args, "i", &exposure))
	        return NULL;

	SetExposureMS(exposure);

	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *
SpectroLib_CaptureSingleSpectrum(PyObject *self)
{
	uint16_t size = 2048;
	uint16_t data[size];

	CaptureSingleSpectrum(&data[0], &size);


	PyObject *pylist, *item;
	int i;
	pylist = PyList_New(size);
	if (pylist != NULL) {
	  for (i=0; i<size; i++) {
		item = PyInt_FromLong(data[i]);
		PyList_SET_ITEM(pylist, i, item);
	  }
	}
	return pylist;
}



static PyObject *
SpectroLib_CaptureContinuousSpectrum(PyObject *self, PyObject *args)
{
	char *filename;
    int delayBetweenMS;
    int durationMS;

	if (!PyArg_ParseTuple(args, "sii", &filename, &delayBetweenMS, &durationMS ))
	        return NULL;

	CaptureContinuousSpectrum(filename,  (uint32_t)delayBetweenMS, (uint32_t)durationMS);

	Py_INCREF(Py_None);
	return Py_None;
}


static PyObject *
SpectroLib_IsCaptureContinuousSpectrumDone(PyObject *self)
{
	BOOL ret = IsCaptureContinuousSpectrumDone();

	return Py_BuildValue("i", ret ? 1 : 0);
}





static PyObject *
SpectroLib_ExitCaptureContinuousSpectrum(PyObject *self)
{
	ExitCaptureContinuousSpectrum();

	Py_INCREF(Py_None);
	return Py_None;
}



static PyMethodDef SpectroLibMethods[] = {
    {"Initialize",  SpectroLib_Initialize, METH_NOARGS, "Initialize the SpectroLib library."},
    {"GetLastErrorMsg",  SpectroLib_GetLastErrorMsg, METH_NOARGS, "Get the last error message reported by the SpectroLib."},
    {"ReadSerialNumber",  SpectroLib_ReadSerialNumber, METH_NOARGS, "Get the serial number of the connected Spectrometer."},
    {"SetExposureMS",  SpectroLib_SetExposureMS, METH_VARARGS, "Set the exposure time in milliseconds."},
    {"CaptureSingleSpectrum",  SpectroLib_CaptureSingleSpectrum, METH_NOARGS, "Capture a single spectrum."},
    {"CaptureContinuousSpectrum",  SpectroLib_CaptureContinuousSpectrum, METH_VARARGS, "Captures spectrums continuously for the given duration with the given delay between captures."},
    {"IsCaptureContinuousSpectrumDone",  SpectroLib_IsCaptureContinuousSpectrumDone, METH_NOARGS, "Check if a continuous capture is complete."},
    {"ExitCaptureContinuousSpectrum",  SpectroLib_ExitCaptureContinuousSpectrum, METH_NOARGS, "Abort an in-progress continuous capture."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};



PyMODINIT_FUNC
initSpectroLib_module(void)
{
    (void) Py_InitModule("SpectroLib_module", SpectroLibMethods);
}
