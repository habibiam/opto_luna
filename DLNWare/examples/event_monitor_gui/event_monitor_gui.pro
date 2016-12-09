#-------------------------------------------------
#
# Project created by QtCreator 2010-07-31T19:20:39
#
#-------------------------------------------------

QT       += core gui

TARGET = event_monitor_gui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a

RESOURCES += \
    images.qrc
