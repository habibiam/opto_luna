#-------------------------------------------------
#
# Project created by QtCreator 2010-11-07T13:07:12
#
#-------------------------------------------------

QT       += core gui

TARGET = spi_gui
TEMPLATE = app

CONFIG += static

SOURCES += main.cpp\
        dialog.cpp

HEADERS  += dialog.h

FORMS    += \
    dialog.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a

