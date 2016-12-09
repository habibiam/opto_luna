#-------------------------------------------------
#
# Project created by QtCreator 2011-02-08T11:17:31
#
#-------------------------------------------------

QT       += core gui

TARGET = spi_slave_gui
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
