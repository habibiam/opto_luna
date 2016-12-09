#-------------------------------------------------
#
# Project created by QtCreator 2011-02-22T14:13:48
#
#-------------------------------------------------

QT       += core gui

TARGET = pwm_gui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
