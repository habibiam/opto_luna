/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 4.8.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QHBoxLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QMainWindow>
#include <QtGui/QPushButton>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QLabel *label;
    QLineEdit *id;
    QHBoxLayout *horizontalLayout_2;
    QPushButton *openDeviceButton;
    QPushButton *getIdButton;
    QPushButton *setIdButton;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(263, 73);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        label = new QLabel(centralWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        id = new QLineEdit(centralWidget);
        id->setObjectName(QString::fromUtf8("id"));

        horizontalLayout->addWidget(id);


        verticalLayout->addLayout(horizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        openDeviceButton = new QPushButton(centralWidget);
        openDeviceButton->setObjectName(QString::fromUtf8("openDeviceButton"));

        horizontalLayout_2->addWidget(openDeviceButton);

        getIdButton = new QPushButton(centralWidget);
        getIdButton->setObjectName(QString::fromUtf8("getIdButton"));

        horizontalLayout_2->addWidget(getIdButton);

        setIdButton = new QPushButton(centralWidget);
        setIdButton->setObjectName(QString::fromUtf8("setIdButton"));

        horizontalLayout_2->addWidget(setIdButton);


        verticalLayout->addLayout(horizontalLayout_2);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Device ID GUI", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("MainWindow", "Current ID:", 0, QApplication::UnicodeUTF8));
        openDeviceButton->setText(QApplication::translate("MainWindow", "Open Device", 0, QApplication::UnicodeUTF8));
        getIdButton->setText(QApplication::translate("MainWindow", "Get ID", 0, QApplication::UnicodeUTF8));
        setIdButton->setText(QApplication::translate("MainWindow", "Set ID", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
