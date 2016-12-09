/********************************************************************************
** Form generated from reading UI file 'dialog.ui'
**
** Created by: Qt User Interface Compiler version 4.8.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DIALOG_H
#define UI_DIALOG_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QCheckBox>
#include <QtGui/QComboBox>
#include <QtGui/QDialog>
#include <QtGui/QGridLayout>
#include <QtGui/QGroupBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QGroupBox *groupBoxAdcChannelConfig;
    QWidget *layoutWidget;
    QGridLayout *gridLayout_3;
    QGridLayout *gridLayout;
    QLabel *labelEventType;
    QComboBox *comboBoxEventType;
    QLabel *labelEventPeriod;
    QLineEdit *lineEditEventPeriod;
    QLabel *labelThresLow;
    QLineEdit *lineEditThresholdLow;
    QLabel *labelThresHigh;
    QLineEdit *lineEditThresholdHigh;
    QPushButton *pushButtonSetChannelConfig;
    QPushButton *pushButtonGetChannelConfig;
    QWidget *layoutWidget1;
    QGridLayout *gridLayout_2;
    QLabel *labelAdcPort;
    QComboBox *comboBoxAdcPort;
    QCheckBox *checkBoxEnableAdc;
    QPushButton *pushButtonOpenDevice;
    QLabel *labelAdcChannel;
    QComboBox *comboBoxAdcChannel;
    QCheckBox *checkBoxChannelEnableAdc;
    QLabel *labelAdcValue;
    QLineEdit *AdcValue;
    QPushButton *pushButtonGetAdcChannelValue;
    QLabel *labelAdcValues;
    QLineEdit *AdcValues;
    QPushButton *pushButtonGetAdcValues;
    QLabel *labelResolution;
    QComboBox *comboBoxAdcResolution;
    QPushButton *pushButtonSetResolution;
    QPushButton *pushButtonGetResolution;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QString::fromUtf8("Dialog"));
        Dialog->resize(417, 299);
        groupBoxAdcChannelConfig = new QGroupBox(Dialog);
        groupBoxAdcChannelConfig->setObjectName(QString::fromUtf8("groupBoxAdcChannelConfig"));
        groupBoxAdcChannelConfig->setGeometry(QRect(10, 160, 401, 131));
        layoutWidget = new QWidget(groupBoxAdcChannelConfig);
        layoutWidget->setObjectName(QString::fromUtf8("layoutWidget"));
        layoutWidget->setGeometry(QRect(10, 20, 385, 102));
        gridLayout_3 = new QGridLayout(layoutWidget);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        labelEventType = new QLabel(layoutWidget);
        labelEventType->setObjectName(QString::fromUtf8("labelEventType"));

        gridLayout->addWidget(labelEventType, 0, 0, 1, 1);

        comboBoxEventType = new QComboBox(layoutWidget);
        comboBoxEventType->setObjectName(QString::fromUtf8("comboBoxEventType"));

        gridLayout->addWidget(comboBoxEventType, 0, 1, 1, 1);

        labelEventPeriod = new QLabel(layoutWidget);
        labelEventPeriod->setObjectName(QString::fromUtf8("labelEventPeriod"));

        gridLayout->addWidget(labelEventPeriod, 1, 0, 1, 1);

        lineEditEventPeriod = new QLineEdit(layoutWidget);
        lineEditEventPeriod->setObjectName(QString::fromUtf8("lineEditEventPeriod"));

        gridLayout->addWidget(lineEditEventPeriod, 1, 1, 1, 1);

        labelThresLow = new QLabel(layoutWidget);
        labelThresLow->setObjectName(QString::fromUtf8("labelThresLow"));

        gridLayout->addWidget(labelThresLow, 2, 0, 1, 1);

        lineEditThresholdLow = new QLineEdit(layoutWidget);
        lineEditThresholdLow->setObjectName(QString::fromUtf8("lineEditThresholdLow"));

        gridLayout->addWidget(lineEditThresholdLow, 2, 1, 1, 1);

        labelThresHigh = new QLabel(layoutWidget);
        labelThresHigh->setObjectName(QString::fromUtf8("labelThresHigh"));

        gridLayout->addWidget(labelThresHigh, 3, 0, 1, 1);

        lineEditThresholdHigh = new QLineEdit(layoutWidget);
        lineEditThresholdHigh->setObjectName(QString::fromUtf8("lineEditThresholdHigh"));

        gridLayout->addWidget(lineEditThresholdHigh, 3, 1, 1, 1);


        gridLayout_3->addLayout(gridLayout, 0, 0, 1, 1);

        pushButtonSetChannelConfig = new QPushButton(layoutWidget);
        pushButtonSetChannelConfig->setObjectName(QString::fromUtf8("pushButtonSetChannelConfig"));

        gridLayout_3->addWidget(pushButtonSetChannelConfig, 0, 1, 1, 1);

        pushButtonGetChannelConfig = new QPushButton(layoutWidget);
        pushButtonGetChannelConfig->setObjectName(QString::fromUtf8("pushButtonGetChannelConfig"));

        gridLayout_3->addWidget(pushButtonGetChannelConfig, 0, 2, 1, 1);

        layoutWidget1 = new QWidget(Dialog);
        layoutWidget1->setObjectName(QString::fromUtf8("layoutWidget1"));
        layoutWidget1->setGeometry(QRect(10, 10, 391, 138));
        gridLayout_2 = new QGridLayout(layoutWidget1);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        labelAdcPort = new QLabel(layoutWidget1);
        labelAdcPort->setObjectName(QString::fromUtf8("labelAdcPort"));

        gridLayout_2->addWidget(labelAdcPort, 0, 0, 1, 1);

        comboBoxAdcPort = new QComboBox(layoutWidget1);
        comboBoxAdcPort->setObjectName(QString::fromUtf8("comboBoxAdcPort"));

        gridLayout_2->addWidget(comboBoxAdcPort, 0, 1, 1, 1);

        checkBoxEnableAdc = new QCheckBox(layoutWidget1);
        checkBoxEnableAdc->setObjectName(QString::fromUtf8("checkBoxEnableAdc"));

        gridLayout_2->addWidget(checkBoxEnableAdc, 0, 2, 1, 1);

        pushButtonOpenDevice = new QPushButton(layoutWidget1);
        pushButtonOpenDevice->setObjectName(QString::fromUtf8("pushButtonOpenDevice"));

        gridLayout_2->addWidget(pushButtonOpenDevice, 0, 4, 1, 1);

        labelAdcChannel = new QLabel(layoutWidget1);
        labelAdcChannel->setObjectName(QString::fromUtf8("labelAdcChannel"));

        gridLayout_2->addWidget(labelAdcChannel, 1, 0, 1, 1);

        comboBoxAdcChannel = new QComboBox(layoutWidget1);
        comboBoxAdcChannel->setObjectName(QString::fromUtf8("comboBoxAdcChannel"));

        gridLayout_2->addWidget(comboBoxAdcChannel, 1, 1, 1, 1);

        checkBoxChannelEnableAdc = new QCheckBox(layoutWidget1);
        checkBoxChannelEnableAdc->setObjectName(QString::fromUtf8("checkBoxChannelEnableAdc"));

        gridLayout_2->addWidget(checkBoxChannelEnableAdc, 1, 2, 1, 1);

        labelAdcValue = new QLabel(layoutWidget1);
        labelAdcValue->setObjectName(QString::fromUtf8("labelAdcValue"));

        gridLayout_2->addWidget(labelAdcValue, 2, 0, 1, 1);

        AdcValue = new QLineEdit(layoutWidget1);
        AdcValue->setObjectName(QString::fromUtf8("AdcValue"));
        AdcValue->setEnabled(false);

        gridLayout_2->addWidget(AdcValue, 2, 1, 1, 2);

        pushButtonGetAdcChannelValue = new QPushButton(layoutWidget1);
        pushButtonGetAdcChannelValue->setObjectName(QString::fromUtf8("pushButtonGetAdcChannelValue"));

        gridLayout_2->addWidget(pushButtonGetAdcChannelValue, 2, 4, 1, 1);

        labelAdcValues = new QLabel(layoutWidget1);
        labelAdcValues->setObjectName(QString::fromUtf8("labelAdcValues"));

        gridLayout_2->addWidget(labelAdcValues, 3, 0, 1, 1);

        AdcValues = new QLineEdit(layoutWidget1);
        AdcValues->setObjectName(QString::fromUtf8("AdcValues"));
        AdcValues->setEnabled(false);

        gridLayout_2->addWidget(AdcValues, 3, 1, 1, 2);

        pushButtonGetAdcValues = new QPushButton(layoutWidget1);
        pushButtonGetAdcValues->setObjectName(QString::fromUtf8("pushButtonGetAdcValues"));

        gridLayout_2->addWidget(pushButtonGetAdcValues, 3, 4, 1, 1);

        labelResolution = new QLabel(layoutWidget1);
        labelResolution->setObjectName(QString::fromUtf8("labelResolution"));

        gridLayout_2->addWidget(labelResolution, 4, 0, 1, 1);

        comboBoxAdcResolution = new QComboBox(layoutWidget1);
        comboBoxAdcResolution->setObjectName(QString::fromUtf8("comboBoxAdcResolution"));

        gridLayout_2->addWidget(comboBoxAdcResolution, 4, 1, 1, 1);

        pushButtonSetResolution = new QPushButton(layoutWidget1);
        pushButtonSetResolution->setObjectName(QString::fromUtf8("pushButtonSetResolution"));

        gridLayout_2->addWidget(pushButtonSetResolution, 4, 3, 1, 1);

        pushButtonGetResolution = new QPushButton(layoutWidget1);
        pushButtonGetResolution->setObjectName(QString::fromUtf8("pushButtonGetResolution"));

        gridLayout_2->addWidget(pushButtonGetResolution, 4, 4, 1, 1);


        retranslateUi(Dialog);

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QApplication::translate("Dialog", "Adc Gui", 0, QApplication::UnicodeUTF8));
        groupBoxAdcChannelConfig->setTitle(QApplication::translate("Dialog", "ADC Channel Configuration", 0, QApplication::UnicodeUTF8));
        labelEventType->setText(QApplication::translate("Dialog", "Event Type:", 0, QApplication::UnicodeUTF8));
        comboBoxEventType->clear();
        comboBoxEventType->insertItems(0, QStringList()
         << QApplication::translate("Dialog", "None", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Below", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Above", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Outside", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Inside", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Always", 0, QApplication::UnicodeUTF8)
        );
        labelEventPeriod->setText(QApplication::translate("Dialog", "Event Period:", 0, QApplication::UnicodeUTF8));
        lineEditEventPeriod->setText(QApplication::translate("Dialog", "0", 0, QApplication::UnicodeUTF8));
        labelThresLow->setText(QApplication::translate("Dialog", "Threshold Low:", 0, QApplication::UnicodeUTF8));
        lineEditThresholdLow->setText(QApplication::translate("Dialog", "0", 0, QApplication::UnicodeUTF8));
        labelThresHigh->setText(QApplication::translate("Dialog", "Threshold High:", 0, QApplication::UnicodeUTF8));
        lineEditThresholdHigh->setText(QApplication::translate("Dialog", "0", 0, QApplication::UnicodeUTF8));
        pushButtonSetChannelConfig->setText(QApplication::translate("Dialog", "Set", 0, QApplication::UnicodeUTF8));
        pushButtonGetChannelConfig->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        labelAdcPort->setText(QApplication::translate("Dialog", "ADC Port:", 0, QApplication::UnicodeUTF8));
        checkBoxEnableAdc->setText(QApplication::translate("Dialog", "Enabled", 0, QApplication::UnicodeUTF8));
        pushButtonOpenDevice->setText(QApplication::translate("Dialog", "Open Device", 0, QApplication::UnicodeUTF8));
        labelAdcChannel->setText(QApplication::translate("Dialog", "ADC Channel:", 0, QApplication::UnicodeUTF8));
        checkBoxChannelEnableAdc->setText(QApplication::translate("Dialog", "Enabled", 0, QApplication::UnicodeUTF8));
        labelAdcValue->setText(QApplication::translate("Dialog", "ADC Value:", 0, QApplication::UnicodeUTF8));
        pushButtonGetAdcChannelValue->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        labelAdcValues->setText(QApplication::translate("Dialog", "ADC Values:", 0, QApplication::UnicodeUTF8));
        pushButtonGetAdcValues->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        labelResolution->setText(QApplication::translate("Dialog", "Resolution:", 0, QApplication::UnicodeUTF8));
        comboBoxAdcResolution->clear();
        comboBoxAdcResolution->insertItems(0, QStringList()
         << QApplication::translate("Dialog", "8", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "10", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "12", 0, QApplication::UnicodeUTF8)
        );
        pushButtonSetResolution->setText(QApplication::translate("Dialog", "Set", 0, QApplication::UnicodeUTF8));
        pushButtonGetResolution->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DIALOG_H
