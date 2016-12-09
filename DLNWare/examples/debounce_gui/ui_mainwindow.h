/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created: Thu 2. Dec 10:50:42 2010
**      by: Qt User Interface Compiler version 4.6.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QPushButton>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QPushButton *buttonSetDebounce;
    QLineEdit *lineEditInputDebounce;
    QLineEdit *lineEditRealDebounce;
    QLabel *label;
    QLabel *labelRealDebounce;
    QMenuBar *menuBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(238, 133);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        buttonSetDebounce = new QPushButton(centralWidget);
        buttonSetDebounce->setObjectName(QString::fromUtf8("buttonSetDebounce"));
        buttonSetDebounce->setGeometry(QRect(150, 30, 81, 23));
        lineEditInputDebounce = new QLineEdit(centralWidget);
        lineEditInputDebounce->setObjectName(QString::fromUtf8("lineEditInputDebounce"));
        lineEditInputDebounce->setGeometry(QRect(10, 30, 131, 20));
        lineEditRealDebounce = new QLineEdit(centralWidget);
        lineEditRealDebounce->setObjectName(QString::fromUtf8("lineEditRealDebounce"));
        lineEditRealDebounce->setEnabled(false);
        lineEditRealDebounce->setGeometry(QRect(10, 80, 131, 20));
        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(10, 10, 121, 16));
        label->setFocusPolicy(Qt::NoFocus);
        labelRealDebounce = new QLabel(centralWidget);
        labelRealDebounce->setObjectName(QString::fromUtf8("labelRealDebounce"));
        labelRealDebounce->setGeometry(QRect(10, 60, 121, 16));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 238, 21));
        MainWindow->setMenuBar(menuBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0, QApplication::UnicodeUTF8));
        buttonSetDebounce->setText(QApplication::translate("MainWindow", "Set Debounce", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Input Debounce Interval: </span></p></body></html>", 0, QApplication::UnicodeUTF8));
        labelRealDebounce->setText(QApplication::translate("MainWindow", "Real Debounce Interval:", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
