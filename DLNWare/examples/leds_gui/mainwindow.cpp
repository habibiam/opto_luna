#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ledstatecombo.h"
#include <QMessageBox>

MainWindow::MainWindow(HDLN handle, QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    _handle(handle)
{
    ui->setupUi(this);
    uint8_t ledCount;
    DLN_RESULT result = DlnLedGetCount(_handle, &ledCount);
    if (DLN_SUCCEEDED(result))
    {
        for (uint8_t i = 0; i < ledCount; i++)
            addLed(i);
    }
    else
    {
        QMessageBox::warning(this, tr("DlnLedGetCount() failed"),
                             tr("DlnLedGetCount() function returns 0x") + QString::number(result, 16));
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::addLed(uint8_t ledNumber)
{
    DLN_LED_STATE state;
    DLN_RESULT result = DlnLedGetState(_handle, ledNumber, &state);
    if (DLN_SUCCEEDED(result))
    {
        LedStateCombo *combo = new LedStateCombo(ledNumber, state);
        connect(combo, SIGNAL(ledStateChanged(uint8_t,DLN_LED_STATE)), SLOT(ledStateChanged(uint8_t,DLN_LED_STATE)));
        ui->ledsList->insertRow(ledNumber);
        ui->ledsList->setVerticalHeaderItem(ledNumber, new
                                            QTableWidgetItem(tr("User LED ") + QString::number(ledNumber) + tr(":")));
        ui->ledsList->setCellWidget(ledNumber, 0, combo);
    }
    else
    {
        QMessageBox::warning(this, tr("DlnLedGetState() failed"),
                             tr("DlnLedGetState() function returns 0x") + QString::number(result, 16));
    }
}

void MainWindow::ledStateChanged(uint8_t ledNumber, DLN_LED_STATE newState)
{
    DLN_RESULT result = DlnLedSetState(_handle, ledNumber, newState);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(this, tr("DlnLedSetState() failed"),
                             tr("DlnLedSetState() function returns 0x") + QString::number(result, 16));
    }
}
