#-------------------------------------------------
#
# Project created by QtCreator 2011-01-05T16:46:19
#
#-------------------------------------------------

QT       += core gui

TARGET = i2c_master_gui
TEMPLATE = app

QMAKE_LFLAGS += -static-libgcc

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
