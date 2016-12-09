#-------------------------------------------------
#
# Project created by QtCreator 2010-06-30T19:14:35
#
#-------------------------------------------------
QT += network
TARGET = get_version
TEMPLATE = app

QMAKE_LFLAGS += -static-libgcc

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
