#-------------------------------------------------
#
# Project created by QtCreator 2011-01-17T16:28:05
#
#-------------------------------------------------

QT       += core gui

TARGET   =  adc_gui
TEMPLATE =  app


SOURCES  += main.cpp\
            dialog.cpp

HEADERS  += dialog.h

FORMS    += dialog.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
