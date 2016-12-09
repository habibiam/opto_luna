#-------------------------------------------------
#
# Project created by QtCreator 2011-02-09T09:39:40
#
#-------------------------------------------------

QT       += core gui

TARGET = i2c_slave_gui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
