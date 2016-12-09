#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include "../common/dln_generic.h"
#include "../common/dln_i2c_slave.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDevice, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->checkBoxEnabled, SIGNAL(stateChanged(int)), SLOT(setEnabled()));
    connect(ui->setAddress, SIGNAL(clicked()), SLOT(setAddress()));
    connect(ui->getAddress, SIGNAL(clicked()), SLOT(getAddress()));
    connect(ui->loadReply, SIGNAL(clicked()), SLOT(loadReply()));
    connect(ui->setEvent, SIGNAL(clicked()), SLOT(setEvent()));
    connect(ui->getEvent, SIGNAL(clicked()), SLOT(getEvent()));
    connect(ui->generalCall, SIGNAL(stateChanged(int)), SLOT(setGeneralCall()));
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
    if (initPortCombo())
    {
        enableControls(true);
        getConfiguration();
    }
}

bool MainWindow::initPortCombo()
{
    ui->port->clear();
    uint8_t count;
    DLN_RESULT result = DlnI2cSlaveGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnI2cSlaveGetPortCount() failed"),
                             tr("DlnI2cSlaveGetPortCount() function returns 0x") + QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No SPI ports"),
                             tr("Current DLN adapter has no SPI ports"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->port->addItem(QString::number(i));
    ui->port->setCurrentIndex(0);
    return true;
}

bool MainWindow::initSlaveAddressNumCombo()
{
    ui->slaveAddressNumber->clear();
    uint8_t count;
    DLN_RESULT result = DlnI2cSlaveGetAddressCount(_handle, ui->port->currentIndex(), &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnI2cSlaveGetAddressCount() failed"),
                             tr("DlnI2cSlaveGetAddressCount() function returns 0x") + QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No Slave Addresses"),
                             tr("Current DLN adapter has no slave addresses"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
    {
        ui->slaveAddressNumber->addItem(QString::number(i));
        ui->slaveAddressNumberEvent->addItem(QString::number(i));
    }
    ui->slaveAddressNumber->setCurrentIndex(0);
    ui->slaveAddressNumberEvent->setCurrentIndex(0);
    return true;
}

void MainWindow::setEnabled()
{
    uint16_t conflict;
    if(ui->checkBoxEnabled->isChecked())
    {
        DLN_RESULT result = DlnI2cSlaveEnable(_handle, ui->port->currentIndex(), &conflict);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnI2cSlaveEnable() failed"),
                                tr("DlnI2cSlaveEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
    if(!ui->checkBoxEnabled->isChecked())
    {
        DLN_RESULT result = DlnI2cSlaveDisable(_handle, ui->port->currentIndex(), 0);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnI2cSlaveDisable() failed"),
                                tr("DlnI2cSlaveDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void MainWindow::getEnabled()
{
    uint8_t enabled;
    DLN_RESULT result = DlnI2cSlaveIsEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnI2cSlaveIsEnabled() failed"),
                            tr("DlnI2cSlaveIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_I2C_SLAVE_ENABLED)
    {
       ui->checkBoxEnabled->setChecked(true);
       return;
    }
    if(enabled == DLN_I2C_SLAVE_DISABLED)
    {
       ui->checkBoxEnabled->setChecked(false);
       return;
    }
}

void MainWindow::setAddress()
{
    DLN_RESULT result = DlnI2cSlaveSetAddress(_handle, ui->port->currentIndex(), ui->slaveAddressNumber->currentIndex(), ui->address->text().toUInt(0, 16));
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnI2cSlaveSetAddress() failed"),
                             tr("DlnI2cSlaveSetAddress() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getAddress()
{
    uint8_t address;

    DLN_RESULT result = DlnI2cSlaveGetAddress(_handle, ui->port->currentIndex(), ui->slaveAddressNumber->currentIndex(), &address);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnI2cSlaveGetAddress() failed"),
                             tr("DlnI2cSlaveGetAddress() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->address->setText(QString::number(address, 16).toUpper());
}

void MainWindow::setGeneralCall()
{
    if(ui->generalCall->isChecked())
    {
        DLN_RESULT result = DlnI2cSlaveGeneralCallEnable(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnI2cSlaveGeneralCallEnable() failed"),
                                tr("DlnI2cSlaveGeneralCallEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
    if(!ui->generalCall->isChecked())
    {
        DLN_RESULT result = DlnI2cSlaveGeneralCallDisable(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnI2cSlaveGeneralCallDisable() failed"),
                                tr("DlnI2cSlaveGeneralCallDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void MainWindow::getGeneralCall()
{
    uint8_t enabled;
    DLN_RESULT result = DlnI2cSlaveGeneralCallIsEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnI2cSlaveGeneralCallIsEnabled() failed"),
                            tr("DlnI2cSlaveGeneralCallIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_I2C_SLAVE_GENERAL_CALL_ENABLED)
    {
       ui->generalCall->setChecked(true);
       return;
    }
    if(enabled == DLN_I2C_SLAVE_GENERAL_CALL_DISABLED)
    {
       ui->generalCall->setChecked(false);
       return;
    }
}

void  MainWindow::loadReply()
{
    QByteArray buffer = QByteArray::fromHex(ui->reply->toPlainText().toAscii());

    if (buffer.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }

    DLN_RESULT result = DlnI2cSlaveLoadReply(_handle, ui->port->currentIndex(), buffer.size(), (uint8_t*)buffer.data());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnI2cSlaveLoadReply() failed"),
                            tr("DlnI2cSlaveLoadReply() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void  MainWindow::setEvent()
{
    DLN_RESULT result = DlnI2cSlaveSetEvent(_handle, ui->port->currentIndex(), ui->slaveAddressNumberEvent->currentIndex(), ui->eventType->currentIndex());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveSetEvent() failed"),
                             tr("DlnSpiSlaveSetEvent() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void  MainWindow::getEvent()
{
    uint8_t eventType;

    DLN_RESULT result = DlnI2cSlaveGetEvent(_handle, ui->port->currentIndex(), ui->slaveAddressNumberEvent->currentIndex(), &eventType);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetEvent() failed"),
                             tr("DlnSpiSlaveGetEvent() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->eventType->setCurrentIndex(eventType);
}

void MainWindow::getConfiguration()
{
    getEnabled();
    initSlaveAddressNumCombo();
    getAddress();
    getEvent();
    getGeneralCall();
}

void MainWindow::enableControls(bool enable)
{
    ui->port->setEnabled(enable);
    if (enable)
        connect(ui->port, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->port, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));

    ui->checkBoxEnabled->setEnabled(enable);
    ui->eventType->setEnabled(enable);
    ui->getEvent->setEnabled(enable);
    ui->loadReply->setEnabled(enable);
    ui->reply->setEnabled(enable);
    ui->setEvent->setEnabled(enable);
    ui->address->setEnabled(enable);
    ui->slaveAddressNumberEvent->setEnabled(enable);
    ui->getAddress->setEnabled(enable);
    ui->setAddress->setEnabled(enable);
    ui->generalCall->setEnabled(enable);
}

