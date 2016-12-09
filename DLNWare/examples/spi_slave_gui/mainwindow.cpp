#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include "../common/dln_generic.h"
#include "../common/dln_spi_slave.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDevice, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->checkBoxEnabled, SIGNAL(stateChanged(int)), SLOT(setEnabled()));
    connect(ui->setMode, SIGNAL(clicked()), SLOT(setSpiSlaveMode()));
    connect(ui->getMode, SIGNAL(clicked()), SLOT(getSpiSlaveMode()));
    connect(ui->setFrameSize, SIGNAL(clicked()), SLOT(setFrameSize()));
    connect(ui->getFrameSize, SIGNAL(clicked()), SLOT(getFrameSize()));
    connect(ui->loadReply, SIGNAL(clicked()), SLOT(loadReply()));
    connect(ui->setEventSize, SIGNAL(clicked()), SLOT(setEventSize()));
    connect(ui->getEventSize, SIGNAL(clicked()), SLOT(getEventSize()));
    connect(ui->enableEvent, SIGNAL(stateChanged(int)), SLOT(setEventEnable()));
    connect(ui->enqueueReply, SIGNAL(clicked()), SLOT(enqueueReply()));
    connect(ui->setShortage, SIGNAL(clicked()), SLOT(setShortage()));
    connect(ui->getShortage, SIGNAL(clicked()), SLOT(getShortage()));
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
    DLN_RESULT result = DlnSpiSlaveGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetPortCount() failed"),
                             tr("DlnSpiSlaveGetPortCount() function returns 0x") + QString::number(result, 16).toUpper());
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

void MainWindow::setEnabled()
{
    uint16_t conflict;
    if(ui->checkBoxEnabled->isChecked())
    {
        DLN_RESULT result = DlnSpiSlaveEnable(_handle, ui->port->currentIndex(), &conflict);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiSlaveEnable() failed"),
                                tr("DlnSpiSlaveEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
    if(!ui->checkBoxEnabled->isChecked())
    {
        DLN_RESULT result = DlnSpiSlaveDisable(_handle, ui->port->currentIndex(), 0);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiSlaveDisable() failed"),
                                tr("DlnSpiSlaveDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void MainWindow::getEnabled()
{
    uint8_t enabled;
    DLN_RESULT result = DlnSpiSlaveIsEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiSlaveIsEnabled() failed"),
                            tr("DlnSpiSlaveIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_SPI_SLAVE_ENABLED)
    {
       ui->checkBoxEnabled->setChecked(true);
       return;
    }
    if(enabled == DLN_SPI_SLAVE_DISABLED)
    {
       ui->checkBoxEnabled->setChecked(false);
       return;
    }
}

void::MainWindow::getSupportedCpolValues()
{
    ui->cpol->clear();
    DLN_SPI_SLAVE_CPOL_VALUES supportedCpolValues;
    DLN_RESULT result = DlnSpiSlaveGetSupportedCpolValues(_handle, ui->port->currentIndex(), &supportedCpolValues);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetSupportedCpolValues() failed"),
                             tr("DlnSpiSlaveGetSupportedCpolValues() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    for (uint8_t i = 0; i < supportedCpolValues.count; i++)
        ui->cpol->addItem(QString::number(supportedCpolValues.values[i]));
    ui->cpol->setCurrentIndex(0);
}

void::MainWindow::getSupportedCphaValues()
{
    ui->cpha->clear();
    DLN_SPI_SLAVE_CPHA_VALUES supportedCphaValues;
    DLN_RESULT result = DlnSpiSlaveGetSupportedCphaValues(_handle, ui->port->currentIndex(), &supportedCphaValues);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetSupportedCphaValues() failed"),
                             tr("DlnSpiSlaveGetSupportedCphaValues() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    for (uint8_t i = 0; i < supportedCphaValues.count; i++)
        ui->cpha->addItem(QString::number(supportedCphaValues.values[i]));
    ui->cpha->setCurrentIndex(0);
}


void MainWindow::setSpiSlaveMode()
{
    uint8_t mode = 0;

    if(ui->cpha->currentText().toUInt() == 1)
        mode |= DLN_SPI_SLAVE_CPHA_1;

    if(ui->cpol->currentText().toUInt() == 1)
        mode |= DLN_SPI_SLAVE_CPOL_1;

    DLN_RESULT result = DlnSpiSlaveSetMode(_handle, ui->port->currentIndex(), mode);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveSetMode() failed"),
                             tr("DlnSpiSlaveSetMode() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getSpiSlaveMode()
{
    uint8_t mode;
    DLN_RESULT result = DlnSpiSlaveGetMode(_handle, ui->port->currentIndex(), &mode);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetMode() failed"),
                             tr("DlnSpiSlaveGetMode() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    if ((mode & DLN_SPI_SLAVE_CPHA_BIT) == DLN_SPI_SLAVE_CPHA_1)
        ui->cpha->setCurrentIndex(1);
    else
        ui->cpha->setCurrentIndex(0);

    if ((mode & DLN_SPI_SLAVE_CPOL_BIT) == DLN_SPI_SLAVE_CPOL_1)
        ui->cpol->setCurrentIndex(1);
    else
        ui->cpol->setCurrentIndex(0);
}

void MainWindow::getSupportedFrameSizes()
{
    ui->frameSize->clear();
    DLN_SPI_SLAVE_FRAME_SIZES supportedSizes;
    DLN_RESULT result = DlnSpiSlaveGetSupportedFrameSizes(_handle, ui->port->currentIndex(), &supportedSizes);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetSupportedFrameSizes() failed"),
                             tr("DlnSpiSlaveGetSupportedFrameSizes() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    for (uint8_t i = 0; i < supportedSizes.count; i++)
        ui->frameSize->addItem(QString::number(supportedSizes.frameSizes[i]));
    ui->frameSize->setCurrentIndex(0);
}

void MainWindow::setFrameSize()
{
    DLN_RESULT result = DlnSpiSlaveSetFrameSize(_handle, ui->port->currentIndex(), ui->frameSize->currentText().toUInt());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveSetFrameSize() failed"),
                             tr("DlnSpiSlaveSetFrameSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getFrameSize()
{
    uint8_t frameSize;

    DLN_RESULT result = DlnSpiSlaveGetFrameSize(_handle, ui->port->currentIndex(), &frameSize);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetFrameSize() failed"),
                             tr("DlnSpiSlaveGetFrameSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    int index = ui->frameSize->findText(QString::number(frameSize));
    ui->frameSize->setCurrentIndex(index);
}

void MainWindow::setShortage()
{
    DLN_RESULT result = DlnSpiSlaveSetReplyShortageAction(_handle, ui->port->currentIndex(), ui->action->currentIndex());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveSetReplyShortageAction() failed"),
                             tr("DlnSpiSlaveSetReplyShortageAction() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void MainWindow::getShortage()
{
    uint8_t action;

    DLN_RESULT result = DlnSpiSlaveGetReplyShortageAction(_handle, ui->port->currentIndex(), &action);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetReplyShortageAction() failed"),
                             tr("DlnSpiSlaveGetReplyShortageAction() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->action->setCurrentIndex(action);
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

    DLN_RESULT result = DlnSpiSlaveLoadReply(_handle, ui->port->currentIndex(), buffer.size(), (uint8_t*)buffer.data());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiSlaveLoadReply() failed"),
                            tr("DlnSpiSlaveLoadReply() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void  MainWindow::enqueueReply()
{
    QByteArray buffer = QByteArray::fromHex(ui->reply->toPlainText().toAscii());

    if (buffer.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }

    DLN_RESULT result = DlnSpiSlaveEnqueueReply(_handle, ui->port->currentIndex(), buffer.size(), (uint8_t*)buffer.data());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiSlaveEnqueueReply() failed"),
                            tr("DlnSpiSlaveEnqueueReply() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void  MainWindow::setEventSize()
{
    DLN_RESULT result = DlnSpiSlaveSetEventSize(_handle, ui->port->currentIndex(), ui->eventSize->text().toUInt());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveSetEventSize() failed"),
                             tr("DlnSpiSlaveSetEventSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void  MainWindow::getEventSize()
{
    uint16_t eventSize;

    DLN_RESULT result = DlnSpiSlaveGetEventSize(_handle, ui->port->currentIndex(), &eventSize);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiSlaveGetEventSize() failed"),
                             tr("DlnSpiSlaveGetEventSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->eventSize->setText(QString::number(eventSize));
}

void MainWindow::setEventEnable()
{
    if(ui->enableEvent->isChecked())
    {
        DLN_RESULT result = DlnSpiSlaveEnableEvent(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiSlaveEnableEvent() failed"),
                                tr("DlnSpiSlaveEnableEvent() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
    if(!ui->enableEvent->isChecked())
    {
        DLN_RESULT result = DlnSpiSlaveDisableEvent(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiSlaveDisableEvent() failed"),
                                tr("DlnSpiSlaveDisableEvent() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void MainWindow::getEventEnable()
{
    uint8_t enabled;
    DLN_RESULT result = DlnSpiSlaveIsEventEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiSlaveIsEventEnabled() failed"),
                            tr("DlnSpiSlaveIsEventEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_SPI_SLAVE_EVENT_ENABLED)
    {
       ui->enableEvent->setChecked(true);
    }
    else
    {
       ui->enableEvent->setChecked(false);
    }
/*
    result = DlnSpiSlaveIsSSRiseEventEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiSlaveIsSSRiseEventEnabled() failed"),
                            tr("DlnSpiSlaveIsSSRiseEventEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_SPI_SLAVE_EVENT_ENABLED)
    {
       ui->enableSSRiseEvent->setChecked(true);
    }
    else
    {
       ui->enableSSRiseEvent->setChecked(false);
    }
*/
}

void MainWindow::getConfiguration()
{
    getEnabled();
    getSpiSlaveMode();
    getSupportedFrameSizes();
    getSupportedCpolValues();
    getSupportedCphaValues();
    getFrameSize();
    getEventSize();
    getEventEnable();
}

void MainWindow::enableControls(bool enable)
{
    ui->port->setEnabled(enable);
    if (enable)
        connect(ui->port, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->port, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));

    ui->checkBoxEnabled->setEnabled(enable);
    ui->cpha->setEnabled(enable);
    ui->cpol->setEnabled(enable);
    ui->eventSize->setEnabled(enable);
    ui->frameSize->setEnabled(enable);
    ui->getEventSize->setEnabled(enable);
    ui->getFrameSize->setEnabled(enable);
    ui->getMode->setEnabled(enable);
    ui->loadReply->setEnabled(enable);
    ui->reply->setEnabled(enable);
    ui->setEventSize->setEnabled(enable);
    ui->setFrameSize->setEnabled(enable);
    ui->setMode->setEnabled(enable);
    ui->enableEvent->setEnabled(enable);
    ui->enqueueReply->setEnabled(enable);
    ui->setShortage->setEnabled(enable);
    ui->getShortage->setEnabled(enable);
    ui->action->setEnabled(enable);
}
