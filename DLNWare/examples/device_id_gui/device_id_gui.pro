#-------------------------------------------------
#
# Project created by QtCreator 2010-07-17T15:19:26
#
#-------------------------------------------------

QT       += core gui

TARGET = device_id_gui
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
