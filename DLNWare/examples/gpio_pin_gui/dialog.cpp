#include "dialog.h"
#include "ui_dialog.h"
#include "../common/dln_gpio.h"
#include "../common/dln_generic.h"
#include <QMessageBox>

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDeviceButton, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->isEnabled, SIGNAL(stateChanged(int)), SLOT(setEnabled()));
    connect(ui->getValueButton, SIGNAL(clicked()), SLOT(getValue()));
    connect(ui->setOutputValue, SIGNAL(clicked()), SLOT(setOutputValue()));
    connect(ui->getOutputValue, SIGNAL(clicked()), SLOT(getOutputValue()));
    connect(ui->setDirection, SIGNAL(clicked()), SLOT(setDirection()));
    connect(ui->getDirection, SIGNAL(clicked()), SLOT(getDirection()));
    connect(ui->isOpenDrain, SIGNAL(stateChanged(int)), SLOT(setOpenDrain()));
    connect(ui->isPullUpEnabled, SIGNAL(stateChanged(int)), SLOT(setPullUp()));
    connect(ui->isPullDownEnabled, SIGNAL(stateChanged(int)), SLOT(setPullDown()));
    connect(ui->isDebounceEnabled, SIGNAL(stateChanged(int)), SLOT(setDebounce()));
    connect(ui->setEventCfg, SIGNAL(clicked()), SLOT(setEventCfg()));
    connect(ui->getEventCfg, SIGNAL(clicked()), SLOT(getEventCfg()));
    openDevice();
}

Dialog::~Dialog()
{
    if (_handle != HDLN_INVALID_HANDLE)
        DlnCloseHandle(_handle);
    delete ui;
}

void Dialog::openDevice()
{
    if (_handle != HDLN_INVALID_HANDLE)
    {
        DlnCloseHandle(_handle);
        _handle = HDLN_INVALID_HANDLE;
    }
    DLN_RESULT result = DlnOpenDevice(0, &_handle);
    if (DLN_SUCCEEDED(result))
    {
        if (initPinCombo())
        {
            enableControls(true);
            getConfiguration();
        }
        else
        {
            enableControls(false);
        }
    }
    else
    {
        enableControls(false);
        QMessageBox::warning(this, QObject::tr("DLN adapter openning error"),
                             QObject::tr("Failed to open DLN adapter. Please check connection."));
    }
}

void Dialog::enableControls(bool enable)
{

    ui->pin->setEnabled(enable);
    if (enable)
        connect(ui->pin, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->pin, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));

    ui->value->setEnabled(enable);
    ui->isEnabled->setEnabled(enable);
    ui->setDirection->setEnabled(enable);
    ui->getDirection->setEnabled(enable);
    ui->direction->setEnabled(enable);
    ui->setDirection->setEnabled(enable);
    ui->getDirection->setEnabled(enable);
    ui->outputValue->setEnabled(enable);
    ui->isOpenDrain->setEnabled(enable);
    ui->isPullUpEnabled->setEnabled(enable);
    ui->isDebounceEnabled->setEnabled(enable);
    ui->eventType->setEnabled(enable);
    ui->eventPeriod->setEnabled(enable);
    ui->getValueButton->setEnabled(enable);
    ui->setEventCfg->setEnabled(enable);
    ui->getEventCfg->setEnabled(enable);
    ui->setOutputValue->setEnabled(enable);
    ui->getOutputValue->setEnabled(enable);
    ui->isPullDownEnabled->setEnabled(enable);
}

bool Dialog::initPinCombo()
{
    ui->pin->clear();
    uint16_t pinCount;
    DLN_RESULT result = DlnGpioGetPinCount(_handle, &pinCount);
    if ((DLN_SUCCEEDED(result)) && (pinCount > 0))
    {
        for (uint16_t i = 0; i < pinCount; i++)
            ui->pin->addItem(QString::number(i+1));
        ui->pin->setCurrentIndex(0);
        return true;
    }
    else
    {
        QMessageBox::warning(this, tr("DlnGpioGetPinCount() failed"),
                             tr("DlnGpioGetPinCount() function returns 0x") + QString::number(result, 16).toUpper());
        return false;
    }
}

void Dialog::initEventCfgCombo()
{
    ui->eventType->clear();
    DLN_GPIO_PIN_EVENT_TYPES eventTypes;
    DlnGpioPinGetSupportedEventTypes(_handle, (uint8_t)ui->pin->currentIndex(), &eventTypes);
    for(int i=0; i < eventTypes.count; i++)
    {
        ui->eventType->addItem(DlnGpioPinEventTypeToStringA(eventTypes.eventTypes[i]));
    }
}

void Dialog::getConfiguration()
{
    getEnabled();
    getDirection();
    getValue();
    getOutputValue();
    getOpenDrain();
    getPullUp();
    getDebounce();
    initEventCfgCombo();
    getEventCfg();
    getPullDown();
}

void Dialog::setEnabled()
{
    if (ui->isEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinEnable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinEnable() failed"),
                                 tr("DlnGpioPinEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(!ui->isEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinDisable(_handle, (uint8_t)ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinDisable() failed"),
                                 tr("DlnGpioPinDisable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getEnabled()
{
    uint8_t enabled;
    DLN_RESULT result = DlnGpioPinIsEnabled(_handle, ui->pin->currentIndex(), &enabled);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinEnable() failed"),
                             tr("DlnGpioPinEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    if(enabled == DLN_GPIO_ENABLED)
    {
       ui->isEnabled->setChecked(true);
       return;
    }
    if(enabled == DLN_GPIO_DISABLED)
    {
       ui->isEnabled->setChecked(false);
       return;
    }
}


void Dialog::setDirection()
{
    DLN_RESULT result = DlnGpioPinSetDirection(_handle, ui->pin->currentIndex(), ui->direction->currentIndex());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinSetDirection() failed"),
                             tr("DlnGpioPinSetDirection() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getDirection()
{
    uint8_t direction;
    DLN_RESULT result = DlnGpioPinGetDirection(_handle, ui->pin->currentIndex(), &direction);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinGetDirection() failed"),
                             tr("DlnGpioPinGetDirection() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
    ui->direction->setCurrentIndex(direction ? 1 : 0);
}

void Dialog::getValue()
{
    uint8_t value;
    uint16_t pin = (uint16_t)ui->pin->currentIndex();
    DLN_RESULT result = /*(ui->direction->currentIndex()) ? DlnGpioPinGetOutVal(_handle, pin, &value) :  */DlnGpioPinGetVal(_handle, pin, &value);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinGet(Out)Val() failed"),
                             tr("DlnGpioPinGet(Out)Val() function returns 0x") + QString::number(result, 16).toUpper());
    }
    ui->value->setText(QString::number(value));

}

void Dialog::setOutputValue()
{
    DLN_RESULT result = DlnGpioPinSetOutVal(_handle, ui->pin->currentIndex(), ui->outputValue->currentIndex()) ;
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioSetPinOutVal() failed"),
                             tr("DlnGpioSetPinOutVal() function returns 0x") + QString::number(result, 16).toUpper());
    }
}

void Dialog::getOutputValue()
{
    uint8_t value;
    DLN_RESULT result = DlnGpioPinGetOutVal(_handle, ui->pin->currentIndex(), &value) ;
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioGetPinOutVal() failed"),
                             tr("DlnGpioGetPinOutVal() function returns 0x") + QString::number(result, 16).toUpper());
    }
    ui->outputValue->setCurrentIndex(value ? 1 : 0);
}

void Dialog::setOpenDrain()
{
    if (ui->isOpenDrain->isChecked())
    {
        DLN_RESULT result = DlnGpioPinOpendrainEnable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinOpendrainEnable() failed"),
                                 tr("DlnGpioPinOpendrainEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(!ui->isOpenDrain->isChecked())
    {
        DLN_RESULT result = DlnGpioPinOpendrainDisable(_handle, (uint8_t)ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinOpendrainDisable() failed"),
                                 tr("DlnGpioPinOpendrainDisable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void::Dialog::getOpenDrain()
{
    uint8_t enabled;
    DLN_RESULT result = DlnGpioPinOpendrainIsEnabled(_handle, ui->pin->currentIndex(), &enabled);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinOpendrainIsEnabled() failed"),
                             tr("DlnGpioPinOpendrainIsEnabled() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->isOpenDrain->setChecked(enabled);
}

void Dialog::setPullUp()
{
    if (ui->isPullUpEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinPullupEnable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinPullupEnable() failed"),
                                 tr("DlnGpioPinPullupEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(!ui->isPullUpEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinPullupDisable(_handle, (uint8_t)ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinPullupDisable() failed"),
                                 tr("DlnGpioPinPullupDisable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void::Dialog::getPullUp()
{
    uint8_t enabled;
    DLN_RESULT result = DlnGpioPinPullupIsEnabled(_handle, ui->pin->currentIndex(), &enabled);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinPullupIsEnabled() failed"),
                             tr("DlnGpioPinPullupIsEnabled() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->isPullUpEnabled->setChecked(enabled);
}

void Dialog::setPullDown()
{
    if (ui->isPullDownEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinPulldownEnable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinPulldownEnable() failed"),
                                 tr("DlnGpioPinPulldownEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(!ui->isPullDownEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinPulldownDisable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinPullupDisable() failed"),
                                 tr("DlnGpioPinPullupDisable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void::Dialog::getPullDown()
{
    uint8_t enabled;
    DLN_RESULT result = DlnGpioPinPulldownIsEnabled(_handle, ui->pin->currentIndex(), &enabled);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinPulldownIsEnabled() failed"),
                             tr("DlnGpioPinPulldownIsEnabled() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->isPullDownEnabled->setChecked(enabled);
}

void Dialog::setDebounce()
{
    if (ui->isDebounceEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinDebounceEnable(_handle, ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinDebounceEnable() failed"),
                                 tr("DlnGpioPinDebounceEnable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(!ui->isDebounceEnabled->isChecked())
    {
        DLN_RESULT result = DlnGpioPinDebounceDisable(_handle, (uint8_t)ui->pin->currentIndex());
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("DlnGpioPinDebounceDisable() failed"),
                                 tr("DlnGpioPinDebounceDisable() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void::Dialog::getDebounce()
{
    uint8_t enabled;
    DLN_RESULT result = DlnGpioPinDebounceIsEnabled(_handle, ui->pin->currentIndex(), &enabled);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinDebounceIsEnabled() failed"),
                             tr("DlnGpioPinDebounceIsEnabled() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->isDebounceEnabled->setChecked(enabled);
}

void::Dialog::setEventCfg()
{
    DLN_RESULT result = DlnGpioPinSetEventCfg(_handle, ui->pin->currentIndex(), ui->eventType->currentIndex(), ui->eventPeriod->text().toUShort()) ;
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinSetEventCfg() failed"),
                             tr("DlnGpioPinSetEventCfg() function returns 0x") + QString::number(result, 16).toUpper());
    }
}

void::Dialog::getEventCfg()
{
    uint8_t eventType;
    uint16_t eventPeriod;
    DLN_RESULT result = DlnGpioPinGetEventCfg(_handle, ui->pin->currentIndex(), &eventType, &eventPeriod);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnGpioPinGetEventCfg() failed"),
                             tr("DlnGpioPinGetEventCfg() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->eventType->setCurrentIndex(eventType);
    ui->eventPeriod->setText(QString::number(eventPeriod));
}
