#-------------------------------------------------
#
# Project created by QtCreator 2010-11-18T11:42:42
#
#-------------------------------------------------

TARGET = debounce_gui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp

HEADERS  += mainwindow.h

FORMS    += mainwindow.ui

QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a
