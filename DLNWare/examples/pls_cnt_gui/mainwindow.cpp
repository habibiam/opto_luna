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
    connect(ui->enabled, SIGNAL(clicked()), SLOT(setEnabled()));
    connect(ui->suspended, SIGNAL(clicked()), SLOT(setSuspended()));
    connect(ui->reset, SIGNAL(clicked()), SLOT(resetCounter()));
    connect(ui->getValue, SIGNAL(clicked()), SLOT(getValue()));
    connect(ui->setMode, SIGNAL(clicked()), SLOT(setMode()));
    connect(ui->getMode, SIGNAL(clicked()), SLOT(getMode()));
    connect(ui->setEventCfg, SIGNAL(clicked()), SLOT(setEventCfg()));
    connect(ui->getEventCfg, SIGNAL(clicked()), SLOT(getEventCfg()));
    connect(ui->getResolution, SIGNAL(clicked()), SLOT(getResolution()));
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
    if (initPlsCntPortCombo())
    {
        enableControls(true);
        getConfiguration();
    }
}

bool MainWindow::initPlsCntPortCombo()
{
    ui->port->clear();
    uint8_t count;
    DLN_RESULT result = DlnPlsCntGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPlsCntGetPortCount() failed"),
                             tr("DlnPlsCntGetPortCount() function returns 0x")+ QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No pulse counter ports"),
                             tr("Current DLN adapter has no pulse counter ports"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->port->addItem(QString::number(i));
    ui->port->setCurrentIndex(0);
    return true;
}

void MainWindow::enableControls(bool enable)
{
    ui->port->setEnabled(enable);
    ui->enabled->setEnabled(enable);
    ui->suspended->setEnabled(enable);
    ui->timer->setEnabled(enable);
    ui->counter->setEnabled(enable);
    ui->reset->setEnabled(enable);
    ui->mode->setEnabled(enable);
    ui->limit->setEnabled(enable);
    ui->setMode->setEnabled(enable);
    ui->getMode->setEnabled(enable);
    ui->eventMatch->setEnabled(enable);
    ui->eventOverflow->setEnabled(enable);
    ui->eventRepeat->setEnabled(enable);
    ui->repeatInterval->setEnabled(enable);
    ui->setEventCfg->setEnabled(enable);
    ui->getEventCfg->setEnabled(enable);
    ui->getValue->setEnabled(enable);
    ui->getResolution->setEnabled(enable);

    ui->port->setEnabled(enable);
    if (enable)
        connect(ui->port, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    else
        disconnect(ui->port, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));
}

void MainWindow::getConfiguration()
{
    getEnabled();
    getSuspended();
    getMode();
    getEventCfg();
}

void MainWindow::setEnabled()
{
    uint16_t conflict;
    if(ui->enabled->isChecked())
    {
        DLN_RESULT result = DlnPlsCntEnable(_handle, ui->port->currentIndex(), &conflict);
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPlsCntEnable() failed"),
                                       tr("DlnPlsCntEnable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->enabled->isChecked())
    {
        DLN_RESULT result = DlnPlsCntDisable(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPlsCntDisable() failed"),
                                       tr("DlnPlsCntDisable() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void MainWindow::getEnabled()
{
    uint8_t enabled;
    DLN_RESULT result = DlnPlsCntIsEnabled(_handle, ui->port->currentIndex(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntIsEnabled() failed"),
                            tr("DlnPlsCntIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    if(enabled == DLN_PLS_CNT_ENABLED)
    {
       ui->enabled->setChecked(true);
       return;
    }
    if(enabled == DLN_PLS_CNT_DISABLED)
    {
       ui->enabled->setChecked(false);
       return;
    }
}

void MainWindow::setSuspended()
{
    if(ui->suspended->isChecked())
    {
        DLN_RESULT result = DlnPlsCntSuspend(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPlsCntSuspend() failed"),
                                       tr("DlnPlsCntSuspend() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(!ui->suspended->isChecked())
    {
        DLN_RESULT result = DlnPlsCntResume(_handle, ui->port->currentIndex());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnPlsCntResume() failed"),
                                       tr("DlnPlsCntResume() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
}

void MainWindow::getSuspended()
{
    uint8_t suspended;
    DLN_RESULT result = DlnPlsCntIsSuspended(_handle, ui->port->currentIndex(), &suspended);
    if (DLN_FAILED(result))
    {
        if(result == DLN_RES_COMMAND_NOT_SUPPORTED)
        {
            ui->suspended->setEnabled(false);
            return;
        }
        else
        {
            QMessageBox::warning(this, tr("DlnPlsCntIsSuspended() failed"),
                            tr("DlnPlsCntIsSuspended() function returns 0x")+ QString::number(result, 16).toUpper());
            return;
        }
    }
    if(suspended == DLN_PLS_CNT_SUSPENDED)
    {
       ui->suspended->setChecked(true);
       return;
    }
    if(!suspended == DLN_PLS_CNT_SUSPENDED)
    {
       ui->suspended->setChecked(false);
       return;
    }
}

void MainWindow::getResolution()
{
    uint8_t resolution;
    DLN_RESULT result = DlnPlsCntGetResolution(_handle, ui->port->currentIndex(), &resolution);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntGetResolution() failed"),
                            tr("DlnPlsCntGetResolution() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    ui->resolution->setText(QString::number(resolution));
}

void MainWindow::resetCounter()
{
    DLN_RESULT result = DlnPlsCntReset(_handle, ui->port->currentIndex(), ui->timer->isChecked(), ui->counter->isChecked());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntReset() failed"),
                            tr("DlnPlsCntReset() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void MainWindow::getValue()
{
    uint32_t timerValue, counterValue;
    DLN_RESULT result = DlnPlsCntGetValue(_handle, ui->port->currentIndex(), &timerValue, &counterValue);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntGetValue() failed"),
                            tr("DlnPlsCntGetValue() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    ui->timerValue->setText(QString::number(timerValue));
    ui->counterValue->setText(QString::number(counterValue));
}

void MainWindow::setMode()
{
    DLN_RESULT result = DlnPlsCntSetMode(_handle, ui->port->currentIndex(), ui->mode->currentIndex(), ui->limit->text().toUInt());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntSetMode() failed"),
                            tr("DlnPlsCntSetMode() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void MainWindow::getMode()
{
    uint8_t mode;
    uint32_t limit;
    DLN_RESULT result = DlnPlsCntGetMode(_handle, ui->port->currentIndex(), &mode, &limit);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntGetMode() failed"),
                            tr("DlnPlsCntGetMode() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
    ui->mode->setCurrentIndex(mode);
    ui->limit->setText(QString::number(limit));
}

void MainWindow::setEventCfg()
{
    uint8_t eventType = 0;

    if(ui->eventOverflow->isChecked())
        eventType |= DLN_PLS_CNT_EVENT_OVERFLOW;

    if(ui->eventMatch->isChecked())
        eventType |= DLN_PLS_CNT_EVENT_MATCH;

    if(ui->eventRepeat->isChecked())
        eventType |= DLN_PLS_CNT_EVENT_REPEAT;

    DLN_RESULT result = DlnPlsCntSetEventCfg(_handle, ui->port->currentIndex(), eventType, ui->repeatInterval->text().toUInt());
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnPlsCntSetEventCfg() failed"),
                            tr("DlnPlsCntSetEventCfg() function returns 0x")+ QString::number(result, 16).toUpper());
       return;
    }
}

void MainWindow::getEventCfg()
{
    uint8_t eventType;
    uint32_t repeatInterval;
    DLN_RESULT result = DlnPlsCntGetEventCfg(_handle, ui->port->currentIndex(), &eventType, &repeatInterval);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnPlsCntGetEventCfg() failed"),
                             tr("DlnPlsCntGetEventCfg() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    if (eventType & DLN_PLS_CNT_EVENT_OVERFLOW)
        ui->eventOverflow->setChecked(true);
    else
        ui->eventOverflow->setChecked(false);

    if (eventType & DLN_PLS_CNT_EVENT_MATCH)
        ui->eventMatch->setChecked(true);
    else
        ui->eventMatch->setChecked(false);

    if (eventType & DLN_PLS_CNT_EVENT_REPEAT)
        ui->eventRepeat->setChecked(true);
    else
        ui->eventRepeat->setChecked(false);

    ui->repeatInterval->setText(QString::number(repeatInterval));
}
