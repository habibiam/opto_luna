# -------------------------------------------------
# Project created by QtCreator 2010-07-05T10:25:08
# -------------------------------------------------
TARGET = device_list_gui
TEMPLATE = app
SOURCES += main.cpp \
    mainwindow.cpp \
    connectdialog.cpp
HEADERS += mainwindow.h \
    connectdialog.h
FORMS += mainwindow.ui \
    connectdialog.ui
QMAKE_LFLAGS += -static-libgcc
LIBS += /usr/local/lib/libdln.a

