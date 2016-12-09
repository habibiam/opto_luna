/********************************************************************************
** Form generated from reading UI file 'dialog.ui'
**
** Created by: Qt User Interface Compiler version 4.8.5
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
    QPushButton *openDeviceButton;
    QGroupBox *groupBoxEventCfg;
    QWidget *layoutWidget;
    QGridLayout *gridLayout;
    QLabel *eventTypeLabel;
    QComboBox *eventType;
    QPushButton *setEventCfg;
    QPushButton *getEventCfg;
    QLabel *eventPeriodLabel;
    QLineEdit *eventPeriod;
    QWidget *layoutWidget1;
    QGridLayout *gridLayout_2;
    QLabel *pinLabel;
    QComboBox *pin;
    QCheckBox *isEnabled;
    QWidget *layoutWidget2;
    QGridLayout *gridLayout_3;
    QLabel *valueLabel;
    QLabel *value;
    QPushButton *getValueButton;
    QLabel *outputValueLabel;
    QComboBox *outputValue;
    QPushButton *setOutputValue;
    QPushButton *getOutputValue;
    QLabel *directionLabel;
    QComboBox *direction;
    QPushButton *setDirection;
    QPushButton *getDirection;
    QLabel *isOpenDrainLabel;
    QCheckBox *isOpenDrain;
    QLabel *isPullUpEnabledLabel;
    QCheckBox *isPullUpEnabled;
    QLabel *isPullDownEnabledLabel;
    QCheckBox *isPullDownEnabled;
    QLabel *isDebounceEnabledLabel;
    QCheckBox *isDebounceEnabled;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QString::fromUtf8("Dialog"));
        Dialog->resize(389, 309);
        openDeviceButton = new QPushButton(Dialog);
        openDeviceButton->setObjectName(QString::fromUtf8("openDeviceButton"));
        openDeviceButton->setGeometry(QRect(300, 10, 75, 23));
        groupBoxEventCfg = new QGroupBox(Dialog);
        groupBoxEventCfg->setObjectName(QString::fromUtf8("groupBoxEventCfg"));
        groupBoxEventCfg->setGeometry(QRect(10, 210, 371, 91));
        layoutWidget = new QWidget(groupBoxEventCfg);
        layoutWidget->setObjectName(QString::fromUtf8("layoutWidget"));
        layoutWidget->setGeometry(QRect(10, 20, 346, 58));
        gridLayout = new QGridLayout(layoutWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        eventTypeLabel = new QLabel(layoutWidget);
        eventTypeLabel->setObjectName(QString::fromUtf8("eventTypeLabel"));

        gridLayout->addWidget(eventTypeLabel, 0, 0, 1, 1);

        eventType = new QComboBox(layoutWidget);
        eventType->setObjectName(QString::fromUtf8("eventType"));

        gridLayout->addWidget(eventType, 0, 1, 1, 1);

        setEventCfg = new QPushButton(layoutWidget);
        setEventCfg->setObjectName(QString::fromUtf8("setEventCfg"));

        gridLayout->addWidget(setEventCfg, 0, 2, 1, 1);

        getEventCfg = new QPushButton(layoutWidget);
        getEventCfg->setObjectName(QString::fromUtf8("getEventCfg"));

        gridLayout->addWidget(getEventCfg, 0, 3, 1, 1);

        eventPeriodLabel = new QLabel(layoutWidget);
        eventPeriodLabel->setObjectName(QString::fromUtf8("eventPeriodLabel"));

        gridLayout->addWidget(eventPeriodLabel, 1, 0, 1, 1);

        eventPeriod = new QLineEdit(layoutWidget);
        eventPeriod->setObjectName(QString::fromUtf8("eventPeriod"));

        gridLayout->addWidget(eventPeriod, 1, 1, 1, 1);

        layoutWidget1 = new QWidget(Dialog);
        layoutWidget1->setObjectName(QString::fromUtf8("layoutWidget1"));
        layoutWidget1->setGeometry(QRect(20, 10, 168, 22));
        gridLayout_2 = new QGridLayout(layoutWidget1);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        pinLabel = new QLabel(layoutWidget1);
        pinLabel->setObjectName(QString::fromUtf8("pinLabel"));

        gridLayout_2->addWidget(pinLabel, 0, 0, 1, 1);

        pin = new QComboBox(layoutWidget1);
        pin->setObjectName(QString::fromUtf8("pin"));

        gridLayout_2->addWidget(pin, 0, 1, 1, 1);

        isEnabled = new QCheckBox(layoutWidget1);
        isEnabled->setObjectName(QString::fromUtf8("isEnabled"));

        gridLayout_2->addWidget(isEnabled, 0, 2, 1, 1);

        layoutWidget2 = new QWidget(Dialog);
        layoutWidget2->setObjectName(QString::fromUtf8("layoutWidget2"));
        layoutWidget2->setGeometry(QRect(20, 41, 351, 159));
        gridLayout_3 = new QGridLayout(layoutWidget2);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        valueLabel = new QLabel(layoutWidget2);
        valueLabel->setObjectName(QString::fromUtf8("valueLabel"));

        gridLayout_3->addWidget(valueLabel, 0, 0, 1, 1);

        value = new QLabel(layoutWidget2);
        value->setObjectName(QString::fromUtf8("value"));

        gridLayout_3->addWidget(value, 0, 1, 1, 1);

        getValueButton = new QPushButton(layoutWidget2);
        getValueButton->setObjectName(QString::fromUtf8("getValueButton"));

        gridLayout_3->addWidget(getValueButton, 0, 2, 1, 1);

        outputValueLabel = new QLabel(layoutWidget2);
        outputValueLabel->setObjectName(QString::fromUtf8("outputValueLabel"));

        gridLayout_3->addWidget(outputValueLabel, 1, 0, 1, 1);

        outputValue = new QComboBox(layoutWidget2);
        outputValue->setObjectName(QString::fromUtf8("outputValue"));

        gridLayout_3->addWidget(outputValue, 1, 1, 1, 1);

        setOutputValue = new QPushButton(layoutWidget2);
        setOutputValue->setObjectName(QString::fromUtf8("setOutputValue"));

        gridLayout_3->addWidget(setOutputValue, 1, 2, 1, 1);

        getOutputValue = new QPushButton(layoutWidget2);
        getOutputValue->setObjectName(QString::fromUtf8("getOutputValue"));

        gridLayout_3->addWidget(getOutputValue, 1, 3, 1, 1);

        directionLabel = new QLabel(layoutWidget2);
        directionLabel->setObjectName(QString::fromUtf8("directionLabel"));

        gridLayout_3->addWidget(directionLabel, 2, 0, 1, 1);

        direction = new QComboBox(layoutWidget2);
        direction->setObjectName(QString::fromUtf8("direction"));

        gridLayout_3->addWidget(direction, 2, 1, 1, 1);

        setDirection = new QPushButton(layoutWidget2);
        setDirection->setObjectName(QString::fromUtf8("setDirection"));

        gridLayout_3->addWidget(setDirection, 2, 2, 1, 1);

        getDirection = new QPushButton(layoutWidget2);
        getDirection->setObjectName(QString::fromUtf8("getDirection"));

        gridLayout_3->addWidget(getDirection, 2, 3, 1, 1);

        isOpenDrainLabel = new QLabel(layoutWidget2);
        isOpenDrainLabel->setObjectName(QString::fromUtf8("isOpenDrainLabel"));

        gridLayout_3->addWidget(isOpenDrainLabel, 3, 0, 1, 1);

        isOpenDrain = new QCheckBox(layoutWidget2);
        isOpenDrain->setObjectName(QString::fromUtf8("isOpenDrain"));

        gridLayout_3->addWidget(isOpenDrain, 3, 1, 1, 1);

        isPullUpEnabledLabel = new QLabel(layoutWidget2);
        isPullUpEnabledLabel->setObjectName(QString::fromUtf8("isPullUpEnabledLabel"));

        gridLayout_3->addWidget(isPullUpEnabledLabel, 4, 0, 1, 1);

        isPullUpEnabled = new QCheckBox(layoutWidget2);
        isPullUpEnabled->setObjectName(QString::fromUtf8("isPullUpEnabled"));

        gridLayout_3->addWidget(isPullUpEnabled, 4, 1, 1, 1);

        isPullDownEnabledLabel = new QLabel(layoutWidget2);
        isPullDownEnabledLabel->setObjectName(QString::fromUtf8("isPullDownEnabledLabel"));

        gridLayout_3->addWidget(isPullDownEnabledLabel, 5, 0, 1, 1);

        isPullDownEnabled = new QCheckBox(layoutWidget2);
        isPullDownEnabled->setObjectName(QString::fromUtf8("isPullDownEnabled"));

        gridLayout_3->addWidget(isPullDownEnabled, 5, 1, 1, 1);

        isDebounceEnabledLabel = new QLabel(layoutWidget2);
        isDebounceEnabledLabel->setObjectName(QString::fromUtf8("isDebounceEnabledLabel"));

        gridLayout_3->addWidget(isDebounceEnabledLabel, 6, 0, 1, 1);

        isDebounceEnabled = new QCheckBox(layoutWidget2);
        isDebounceEnabled->setObjectName(QString::fromUtf8("isDebounceEnabled"));

        gridLayout_3->addWidget(isDebounceEnabled, 6, 1, 1, 1);


        retranslateUi(Dialog);

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QApplication::translate("Dialog", "GPIO Pin GUI", 0, QApplication::UnicodeUTF8));
        openDeviceButton->setText(QApplication::translate("Dialog", "Open Device", 0, QApplication::UnicodeUTF8));
        groupBoxEventCfg->setTitle(QApplication::translate("Dialog", "Event Config:", 0, QApplication::UnicodeUTF8));
        eventTypeLabel->setText(QApplication::translate("Dialog", "eventType:", 0, QApplication::UnicodeUTF8));
        eventType->clear();
        eventType->insertItems(0, QStringList()
         << QApplication::translate("Dialog", "None", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Change", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Level 1", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Level 0", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "Always", 0, QApplication::UnicodeUTF8)
        );
        setEventCfg->setText(QApplication::translate("Dialog", "Set", 0, QApplication::UnicodeUTF8));
        getEventCfg->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        eventPeriodLabel->setText(QApplication::translate("Dialog", "eventPeriod:", 0, QApplication::UnicodeUTF8));
        pinLabel->setText(QApplication::translate("Dialog", "Pin:", 0, QApplication::UnicodeUTF8));
        isEnabled->setText(QApplication::translate("Dialog", "Enabled", 0, QApplication::UnicodeUTF8));
        valueLabel->setText(QApplication::translate("Dialog", "value:", 0, QApplication::UnicodeUTF8));
        value->setText(QApplication::translate("Dialog", "-", 0, QApplication::UnicodeUTF8));
        getValueButton->setText(QApplication::translate("Dialog", "Get Value", 0, QApplication::UnicodeUTF8));
        outputValueLabel->setText(QApplication::translate("Dialog", "outputValue:", 0, QApplication::UnicodeUTF8));
        outputValue->clear();
        outputValue->insertItems(0, QStringList()
         << QApplication::translate("Dialog", "0", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "1", 0, QApplication::UnicodeUTF8)
        );
        setOutputValue->setText(QApplication::translate("Dialog", "Set", 0, QApplication::UnicodeUTF8));
        getOutputValue->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        directionLabel->setText(QApplication::translate("Dialog", "Direction:", 0, QApplication::UnicodeUTF8));
        direction->clear();
        direction->insertItems(0, QStringList()
         << QApplication::translate("Dialog", "0", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Dialog", "1", 0, QApplication::UnicodeUTF8)
        );
        setDirection->setText(QApplication::translate("Dialog", "Set", 0, QApplication::UnicodeUTF8));
        getDirection->setText(QApplication::translate("Dialog", "Get", 0, QApplication::UnicodeUTF8));
        isOpenDrainLabel->setText(QApplication::translate("Dialog", "isOpenDrain:", 0, QApplication::UnicodeUTF8));
        isOpenDrain->setText(QString());
        isPullUpEnabledLabel->setText(QApplication::translate("Dialog", "isPullUpEnabled:", 0, QApplication::UnicodeUTF8));
        isPullUpEnabled->setText(QString());
        isPullDownEnabledLabel->setText(QApplication::translate("Dialog", "isPullDownEnabled:", 0, QApplication::UnicodeUTF8));
        isPullDownEnabled->setText(QString());
        isDebounceEnabledLabel->setText(QApplication::translate("Dialog", "isDebounceEnabled:", 0, QApplication::UnicodeUTF8));
        isDebounceEnabled->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DIALOG_H
