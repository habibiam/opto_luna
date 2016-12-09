#-------------------------------------------------
#
# Project created by QtCreator 2010-07-30T12:58:58
#
#-------------------------------------------------

QT       += core gui

TARGET = leds_gui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    ledstatecombo.cpp

HEADERS  += mainwindow.h \
    ledstatecombo.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
