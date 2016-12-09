#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include "../common/dln_generic.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDevice, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->portPwmEnabled, SIGNAL(stateChanged(int)), SLOT(setPwmPort()));
    connect(ui->channelPwmEnabled, SIGNAL(stateChanged(int)), SLOT(setPwmChannel()));
    connect(ui->setFrequency, SIGNAL(clicked()), SLOT(setFrequency()));
    connect(ui->setDutyCycle, SIGNAL(clicked()), SLOT(setDutyCycle()));
    connect(ui->getFrequency, SIGNAL(clicked()), SLOT(getFrequency()));
    connect(ui->getDutyCycle, SIGNAL(clicked()), SLOT(getDutyCycle()));
    openDevice();
}

MainWindow::~MainWindow()
{
    if (_handle != HDLN_INVALID_HANDLE)
        DlnCloseHandle(_handle);
    delete ui;
}

void MainWindow::openDevice()
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
    if (initPwmPortCombo() && initPwmChannelCombo())
    {
        enableControls(true);
        getConfiguration();
    }
}

void MainWindow::setPwmPort()
{
    uint16_t conflict;
    if(ui->portPwmEnabled->isChecked())
    {
        DLN_RESULT result = DlnPwmEnable(_handle, ui->port->currentIndex(), &conflict);
        if (result == DLN_RES_ALL_CHANNELS_DISABLED)
        {
            QMessageBox::warning(this, tr("DlnPwmEnable() failed"),
                                       tr("To enable PWM for selected Port you should enable Adc at least for one channel!"));
            ui->portPwmEnabled->setChecked(false);
            return;
        }
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPwmEnable() failed"),
                                       tr("DlnPwmEnable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->portPwmEnabled->isChecked())
    {
        DLN_RESULT result = DlnPwmDisable(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPwmDisable() failed"),
                                       tr("DlnPwmDisable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void MainWindow::getPwmPort()
{
    uint8_t enabled;
    DLN_RESULT result = DlnPwmIsEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPwmIsEnabled() failed"),
                            tr("DlnPwmIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_PWM_ENABLED)
    {
       ui->portPwmEnabled->setChecked(true);
       return;
    }
    if(enabled == DLN_PWM_DISABLED)
    {
       ui->portPwmEnabled->setChecked(false);
       return;
    }
}

bool MainWindow::initPwmPortCombo()
{
    ui->port->clear();
    uint8_t count;
    DLN_RESULT result = DlnPwmGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmGetPortCount() failed"),
                             tr("DlnPwmGetPortCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No PWM ports"),
                             tr("Current DLN adapter has no PWM ports"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->port->addItem(QString::number(i));
    ui->port->setCurrentIndex(0);
    return true;
}

void MainWindow::setPwmChannel()
{
    if(ui->channelPwmEnabled->isChecked())
    {
        DLN_RESULT result = DlnPwmChannelEnable(_handle, ui->port->currentIndex(), ui->channel->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPwmChannelEnable() failed"),
                                       tr("DlnPwmChannelEnable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->channelPwmEnabled->isChecked())
    {
        DLN_RESULT result = DlnPwmChannelDisable(_handle, ui->port->currentIndex(), ui->channel->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPwmChannelDisable() failed"),
                                       tr("DlnPwmChannelDisable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void MainWindow::getPwmChannel()
{
    uint8_t enabled;
    DLN_RESULT result = DlnPwmChannelIsEnabled(_handle, ui->port->currentIndex(), ui->channel->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPwmChannelIsEnabled() failed"),
                            tr("DlnPwmChannelIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_PWM_CHANNEL_ENABLED)
    {
       ui->channelPwmEnabled->setChecked(true);
       return;
    }
    if(enabled == DLN_PWM_CHANNEL_DISABLED)
    {
       ui->channelPwmEnabled->setChecked(false);
       return;
    }
}

bool MainWindow::initPwmChannelCombo()
{
    ui->channel->clear();
    uint8_t count;
    DLN_RESULT result = DlnPwmGetChannelCount(_handle, ui->port->currentIndex(), &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmGetChannelCount() failed"),
                             tr("DlnPwmGetChannelCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No PWM channels"),
                             tr("Current DLN adapter has no PWM channels"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->channel->addItem(QString::number(i));
    ui->channel->setCurrentIndex(0);
    return true;
}

void MainWindow::setFrequency()
{
    uint32_t frequency;
    DLN_RESULT result = DlnPwmSetFrequency(_handle, ui->port->currentIndex(), ui->channel->currentIndex(), ui->frequency->text().toUInt(), &frequency);
    if (result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("DlnPwmSetFrequency()"),
                              tr("Frequency was rounded to ")+ QString::number(frequency, 10));
         ui->frequency->setText(QString::number(frequency));
         return;
    }
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmSetFrequency() failed"),
                             tr("DlnPwmSetFrequency() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getFrequency()
{
    uint32_t frequency;
    DLN_RESULT result = DlnPwmGetFrequency(_handle, ui->port->currentIndex(), ui->channel->currentIndex(), &frequency);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmGetFrequency() failed"),
                             tr("DlnPwmGetFrequency() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }

    ui->frequency->setText(QString::number(frequency));
}

void MainWindow::setDutyCycle()
{
    double dutyCycle;
    DLN_RESULT result = DlnPwmSetDutyCycle(_handle, ui->port->currentIndex(), ui->channel->currentIndex(), ui->dutyCycle->text().toDouble(), &dutyCycle);
    if (result == DLN_RES_PWM_INVALID_DUTY_CYCLE)
    {
        QMessageBox::warning(this, tr("DlnPwmSetDutyCycle() failed"),
                             tr("Duty Cycle value should be between 0 and 100"));
        ui->dutyCycle->setFocus();
        return;
    }
    if (result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("DlnPwmSetDutyCycle()"),
                             tr("Duty Cycle was rounded to ")+ QString::number(dutyCycle, 'f'));
        ui->dutyCycle->setText(QString::number(dutyCycle));
        return;
    }
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmSetDutyCycle() failed"),
                             tr("DlnPwmSetDutyCycle() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getDutyCycle()
{
    double dutyCycle;
    DLN_RESULT result = DlnPwmGetDutyCycle(_handle, ui->port->currentIndex(), ui->channel->currentIndex(), &dutyCycle);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPwmGetFrequency() failed"),
                             tr("DlnPwmGetFrequency() function returns 0x")+ QString::number(result, 16).toUpper());
        return;
    }

    ui->dutyCycle->setText(QString::number(dutyCycle));
}

void MainWindow::enableControls(bool enable)
{
    ui->port->setEnabled(enable);
    ui->channel->setEnabled(enable);
    ui->portPwmEnabled->setEnabled(enable);
    ui->channelPwmEnabled->setEnabled(enable);
    ui->channelPwmEnabled->setEnabled(enable);
    ui->frequency->setEnabled(enable);
    ui->dutyCycle->setEnabled(enable);
    ui->setFrequency->setEnabled(enable);
    ui->setDutyCycle->setEnabled(enable);
    ui->getFrequency->setEnabled(enable);
    ui->getDutyCycle->setEnabled(enable);

    ui->port->setEnabled(enable);
    if (enable)
        connect(ui->port, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->port, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));

    ui->channel->setEnabled(enable);

    if (enable)
        connect(ui->channel, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->channel, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));
}

void MainWindow::getConfiguration()
{
    getPwmPort();
    getPwmChannel();
    getFrequency();
    getDutyCycle();  
}

