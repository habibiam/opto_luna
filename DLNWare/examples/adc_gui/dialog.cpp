#include "dialog.h"
#include "ui_dialog.h"
#include <QMessageBox>
#include <QDateTime>
#include "../common/dln_generic.h"

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->pushButtonOpenDevice, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->checkBoxEnableAdc, SIGNAL(stateChanged(int)), SLOT(setAdc()));
    connect(ui->pushButtonSetResolution, SIGNAL(clicked()), SLOT(setResolution()));
    connect(ui->pushButtonGetResolution, SIGNAL(clicked()), SLOT(getResolution()));
    connect(ui->pushButtonGetAdcChannelValue, SIGNAL(clicked()), SLOT(getAdcValue()));
    connect(ui->pushButtonGetAdcValues, SIGNAL(clicked()), SLOT(getAdcAllValues()));
    connect(ui->pushButtonSetChannelConfig, SIGNAL(clicked()), SLOT(setChannelCfg()));
    connect(ui->checkBoxChannelEnableAdc, SIGNAL(stateChanged(int)), SLOT(setAdcChannel()));
    connect(ui->pushButtonGetChannelConfig, SIGNAL(clicked()), SLOT(getChannelCfg()));
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
    enableControls(false);
    if (_handle != HDLN_INVALID_HANDLE)
    {
        DlnCloseHandle(_handle);
        _handle = HDLN_INVALID_HANDLE;
    }
    DLN_RESULT result = DlnOpenDevice(0, &_handle);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DLN adapter openning error"),
                             tr("Failed to open DLN-series adapter. DlnOpenDevice() returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if (initAdcPortCombo() && initAdcChannelCombo())
    {
        enableControls(true);
        getConfiguration();
    }
}

void Dialog::enableControls(bool enable)
{
    ui->checkBoxEnableAdc->setEnabled(enable);
    ui->checkBoxChannelEnableAdc->setEnabled(enable);
    ui->comboBoxAdcPort->setEnabled(enable);
    ui->comboBoxAdcResolution->setEnabled(enable);
    ui->pushButtonGetAdcChannelValue->setEnabled(enable);
    ui->pushButtonGetAdcValues->setEnabled(enable);
    ui->pushButtonGetResolution->setEnabled(enable);
    ui->pushButtonSetResolution->setEnabled(enable);
    ui->comboBoxEventType->setEnabled(enable);
    ui->pushButtonSetChannelConfig->setEnabled(enable);
    ui->pushButtonGetChannelConfig->setEnabled(enable);
    ui->lineEditEventPeriod->setEnabled(enable);
    ui->lineEditThresholdHigh->setEnabled(enable);
    ui->lineEditThresholdLow->setEnabled(enable);

    ui->comboBoxAdcPort->setEnabled(enable);
    if (enable)
        connect(ui->comboBoxAdcPort, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->comboBoxAdcPort, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));


    ui->comboBoxAdcChannel->setEnabled(enable);
    if (enable)
        connect(ui->comboBoxAdcChannel, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->comboBoxAdcChannel, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));
}

void Dialog::getConfiguration()
{
    getAdc();
    getAdcChannel();
    getResolution();
    getChannelCfg();
}

bool Dialog::initAdcPortCombo()
{
    ui->comboBoxAdcPort->clear();
    uint8_t count;
    DLN_RESULT result = DlnAdcGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetPortCount() failed"),
                             tr("DlnAdcGetPortCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No ADC ports"),
                             tr("Current DLN adapter has no ADC ports"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->comboBoxAdcPort->addItem(QString::number(i));
    ui->comboBoxAdcPort->setCurrentIndex(0);
    return true;
}

void Dialog::setAdc()
{
    uint16_t conflict;
    if(ui->checkBoxEnableAdc->isChecked())
    {
        DLN_RESULT result = DlnAdcEnable(_handle, ui->comboBoxAdcPort->currentIndex(), &conflict);
        if (result == DLN_RES_ALL_CHANNELS_DISABLED)
        {
            ui->checkBoxEnableAdc->setChecked(false);
            QMessageBox::warning(this, tr("DlnAdcEnable() failed"),
                                       tr("To enable ADC for selected Port you should enable Adc at least for one channel"));

            return;
        }
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnAdcEnable() failed"),
                                       tr("DlnAdcEnable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->checkBoxEnableAdc->isChecked())
    {
        DLN_RESULT result = DlnAdcDisable(_handle, ui->comboBoxAdcPort->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnAdcDisable() failed"),
                                       tr("DlnAdcDisable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void Dialog::getAdc()
{
    uint8_t enabled;
    DLN_RESULT result = DlnAdcIsEnabled(_handle, ui->comboBoxAdcPort->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnAdcIsEnabled() failed"),
                            tr("DlnAdcIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_ADC_ENABLED)
    {
       ui->checkBoxEnableAdc->setChecked(true);
       return;
    }
    if(enabled == DLN_ADC_DISABLED)
    {
       ui->checkBoxEnableAdc->setChecked(false);
       return;
    }
}

bool Dialog::initAdcChannelCombo()
{
    uint8_t count;
    DLN_RESULT result = DlnAdcGetChannelCount(_handle, ui->comboBoxAdcPort->currentIndex(), &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetChannelCount() failed"),
                             tr("DlnAdcGetChannelCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return false;
    }

    ui->comboBoxAdcChannel->clear();
    for (uint8_t i = 0; i < count; i++)
        ui->comboBoxAdcChannel->addItem(QString::number(i));
    ui->comboBoxAdcChannel->setCurrentIndex(0);
    return true;
}

void Dialog::setAdcChannel()
{
    if(ui->checkBoxChannelEnableAdc->isChecked())
    {
        DLN_RESULT result = DlnAdcChannelEnable(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnAdcChannelEnable() failed"),
                                       tr("DlnAdcChannelEnable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->checkBoxChannelEnableAdc->isChecked())
    {
        DLN_RESULT result = DlnAdcChannelDisable(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnAdcChannelDisable() failed"),
                                       tr("DlnAdcChannelDisable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void Dialog::getAdcChannel()
{
    uint8_t enabled = 0;
    DLN_RESULT result = DlnAdcChannelIsEnabled(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnAdcChannelIsEnabled() failed"),
                            tr("DlnAdcChannelIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_ADC_CHANNEL_ENABLED)
    {
       ui->checkBoxChannelEnableAdc->setChecked(true);
       return;
    }
    if(enabled == DLN_ADC_CHANNEL_DISABLED)
    {
       ui->checkBoxChannelEnableAdc->setChecked(false);
       return;
    }
}

void Dialog::setResolution()
{
    DLN_RESULT result = DlnAdcSetResolution(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcResolution->currentText().toInt());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcSetResolution() failed"),
                             tr("DlnAdcSetResolution() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getResolution()
{
    uint8_t resolution;
    DLN_RESULT result = DlnAdcGetResolution(_handle, ui->comboBoxAdcPort->currentIndex(), &resolution);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetResolution() failed"),
                             tr("DlnAdcGetResolution() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }

    int index = ui->comboBoxAdcResolution->findText(QString::number(resolution));
    ui->comboBoxAdcResolution->setCurrentIndex(index);
}

void Dialog::getAdcValue()
{
    uint16_t value;
    DLN_RESULT result = DlnAdcGetValue(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex(), &value);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetValue() failed"),
                             tr("DlnAdcGetValue() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }

    ui->AdcValue->setText(QString::number(value, 16));
}

void Dialog::getAdcAllValues()
{
    uint16_t values[DLN_ADC_CHANNEL_COUNT_MAX], channelMask;
    uint8_t count;

    DLN_RESULT result = DlnAdcGetAllValues(_handle, ui->comboBoxAdcPort->currentIndex(), &channelMask, (uint16_t*)values);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetAllValues() failed"),
                             tr("DlnAdcGetAllValues() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
    result = DlnAdcGetChannelCount(_handle, ui->comboBoxAdcPort->currentIndex(), &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcGetChannelCount() failed"),
                             tr("DlnAdcGetChannelCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
    QString valuesStr;
    for (uint8_t i = 0; i < count; i++)
        valuesStr += QString::number(values[i], 16) + " ";

    ui->AdcValues->setText(valuesStr);
}

void Dialog::setChannelCfg()
{
    bool ok;
    uint16_t eventPeriod = ui->lineEditEventPeriod->text().toUShort(&ok);
    if ((ok == false) || eventPeriod > 0x7FFF)
    {
        QMessageBox::warning(this, tr("Invalid Repeat Value"),
                             tr("Repeat Value must be in the range from 0 to 32767"));
        ui->lineEditEventPeriod->setFocus();
        return;
    }
    uint16_t thresholdLow = ui->lineEditThresholdLow->text().toUShort(&ok);
    if ((ok == false) || thresholdLow > 0x7FFF)
    {
        QMessageBox::warning(this, tr("Invalid Threshold Low Value"),
                             tr("Threshold Low Value must be in the range from 0 to 32767"));
        ui->lineEditThresholdLow->setFocus();
        return;
    }
    uint16_t thresholdHigh = ui->lineEditThresholdHigh->text().toUShort(&ok);
    if ((ok == false) || thresholdHigh > 0x7FFF)
    {
        QMessageBox::warning(this, tr("Invalid Threshold High Value"),
                             tr("Threshold High Value must be in the range from 0 to 32767"));
        ui->lineEditThresholdHigh->setFocus();
        return;
    }
    DLN_RESULT result = DlnAdcChannelSetCfg(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex(), ui->comboBoxEventType->currentIndex(), eventPeriod, thresholdLow, thresholdHigh);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcChannelSetCfg() failed"),
                             tr("DlnAdcSetChannelCfg() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getChannelCfg()
{
    uint16_t eventPeriod, thresholdLow, thresholdHigh;
    uint8_t eventType;

    DLN_RESULT result = DlnAdcChannelGetCfg(_handle, ui->comboBoxAdcPort->currentIndex(), ui->comboBoxAdcChannel->currentIndex(), &eventType, &eventPeriod, &thresholdLow, &thresholdHigh);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnAdcChannelGetCfg() failed"),
                             tr("DlnAdcGetChannelCfg() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }

    ui->comboBoxEventType->setCurrentIndex(eventType);
    ui->lineEditEventPeriod->setText(QString::number(eventPeriod));
    ui->lineEditThresholdLow->setText(QString::number(thresholdLow));
    ui->lineEditThresholdHigh->setText(QString::number(thresholdHigh));
}
