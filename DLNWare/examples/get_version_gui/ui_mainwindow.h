/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 4.8.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QLocale>
#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHBoxLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QMainWindow>
#include <QtGui/QPushButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QPushButton *getVersionButton;
    QSpacerItem *horizontalSpacer_2;
    QGridLayout *gridLayout;
    QLabel *hardwareTypeLabel;
    QLineEdit *hardwareType;
    QLabel *hardwareVersionLabel;
    QLineEdit *hardwareVersion;
    QLabel *firmwareVersionLabel;
    QLineEdit *firmwareVersion;
    QLabel *serverVersionLabel;
    QLineEdit *serverVersion;
    QLabel *libraryVersionLabel;
    QLineEdit *libraryVersion;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(355, 175);
        MainWindow->setLocale(QLocale(QLocale::English, QLocale::UnitedStates));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        verticalLayout = new QVBoxLayout(centralWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        getVersionButton = new QPushButton(centralWidget);
        getVersionButton->setObjectName(QString::fromUtf8("getVersionButton"));

        horizontalLayout->addWidget(getVersionButton);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer_2);


        verticalLayout->addLayout(horizontalLayout);

        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        hardwareTypeLabel = new QLabel(centralWidget);
        hardwareTypeLabel->setObjectName(QString::fromUtf8("hardwareTypeLabel"));
        hardwareTypeLabel->setScaledContents(false);

        gridLayout->addWidget(hardwareTypeLabel, 0, 0, 1, 1);

        hardwareType = new QLineEdit(centralWidget);
        hardwareType->setObjectName(QString::fromUtf8("hardwareType"));
        hardwareType->setEnabled(true);
        hardwareType->setReadOnly(true);

        gridLayout->addWidget(hardwareType, 0, 1, 1, 1);

        hardwareVersionLabel = new QLabel(centralWidget);
        hardwareVersionLabel->setObjectName(QString::fromUtf8("hardwareVersionLabel"));

        gridLayout->addWidget(hardwareVersionLabel, 1, 0, 1, 1);

        hardwareVersion = new QLineEdit(centralWidget);
        hardwareVersion->setObjectName(QString::fromUtf8("hardwareVersion"));
        hardwareVersion->setReadOnly(true);

        gridLayout->addWidget(hardwareVersion, 1, 1, 1, 1);

        firmwareVersionLabel = new QLabel(centralWidget);
        firmwareVersionLabel->setObjectName(QString::fromUtf8("firmwareVersionLabel"));

        gridLayout->addWidget(firmwareVersionLabel, 2, 0, 1, 1);

        firmwareVersion = new QLineEdit(centralWidget);
        firmwareVersion->setObjectName(QString::fromUtf8("firmwareVersion"));
        firmwareVersion->setReadOnly(true);

        gridLayout->addWidget(firmwareVersion, 2, 1, 1, 1);

        serverVersionLabel = new QLabel(centralWidget);
        serverVersionLabel->setObjectName(QString::fromUtf8("serverVersionLabel"));

        gridLayout->addWidget(serverVersionLabel, 3, 0, 1, 1);

        serverVersion = new QLineEdit(centralWidget);
        serverVersion->setObjectName(QString::fromUtf8("serverVersion"));
        serverVersion->setReadOnly(true);

        gridLayout->addWidget(serverVersion, 3, 1, 1, 1);

        libraryVersionLabel = new QLabel(centralWidget);
        libraryVersionLabel->setObjectName(QString::fromUtf8("libraryVersionLabel"));

        gridLayout->addWidget(libraryVersionLabel, 4, 0, 1, 1);

        libraryVersion = new QLineEdit(centralWidget);
        libraryVersion->setObjectName(QString::fromUtf8("libraryVersion"));
        libraryVersion->setReadOnly(true);

        gridLayout->addWidget(libraryVersion, 4, 1, 1, 1);


        verticalLayout->addLayout(gridLayout);

        MainWindow->setCentralWidget(centralWidget);
        QWidget::setTabOrder(getVersionButton, hardwareType);
        QWidget::setTabOrder(hardwareType, hardwareVersion);
        QWidget::setTabOrder(hardwareVersion, firmwareVersion);
        QWidget::setTabOrder(firmwareVersion, serverVersion);
        QWidget::setTabOrder(serverVersion, libraryVersion);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Diolan Get Version Demo", 0, QApplication::UnicodeUTF8));
        getVersionButton->setText(QApplication::translate("MainWindow", "Get Version", 0, QApplication::UnicodeUTF8));
        hardwareTypeLabel->setText(QApplication::translate("MainWindow", "Hardware type:", 0, QApplication::UnicodeUTF8));
        hardwareVersionLabel->setText(QApplication::translate("MainWindow", "Hardware version:", 0, QApplication::UnicodeUTF8));
        firmwareVersionLabel->setText(QApplication::translate("MainWindow", "Firmware version:", 0, QApplication::UnicodeUTF8));
        serverVersionLabel->setText(QApplication::translate("MainWindow", "Server version", 0, QApplication::UnicodeUTF8));
        libraryVersionLabel->setText(QApplication::translate("MainWindow", "Library version:", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
