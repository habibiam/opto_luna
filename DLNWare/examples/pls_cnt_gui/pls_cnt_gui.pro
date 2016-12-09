#-------------------------------------------------
#
# Project created by QtCreator 2011-04-19T16:19:34
#
#-------------------------------------------------

QT       += core gui

TARGET = pls_cnt_gui
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
