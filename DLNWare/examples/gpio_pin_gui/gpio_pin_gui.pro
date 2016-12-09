#-------------------------------------------------
#
# Project created by QtCreator 2010-10-10T14:20:28
#
#-------------------------------------------------

QT       += core gui

TARGET = gpio_pin_gui
TEMPLATE = app


SOURCES += main.cpp\
        dialog.cpp

HEADERS  += dialog.h

FORMS    += dialog.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
