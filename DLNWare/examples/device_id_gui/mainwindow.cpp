#include <QMessageBox>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "../common/dln_generic.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDeviceButton, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->getIdButton, SIGNAL(clicked()), SLOT(getId()));
    connect(ui->setIdButton, SIGNAL(clicked()), SLOT(setId()));
    openDevice();
}

MainWindow::~MainWindow()
{
    if (handle != HDLN_INVALID_HANDLE)
        closeDevice();
    delete ui;
}


void MainWindow::openDevice()
{
    if (handle != HDLN_INVALID_HANDLE)
        closeDevice();
    DLN_RESULT result = DlnOpenDevice(0, &handle);
    if (DLN_SUCCEEDED(result))
    {
        getId();
        ui->id->setEnabled(true);
        ui->getIdButton->setEnabled(true);
        ui->setIdButton->setEnabled(true);
    }
    else
    {
        if (result == DLN_RES_HARDWARE_NOT_FOUND)
            QMessageBox::warning(this, tr("Device Open Error"), tr("No device is connected"));
        else
            QMessageBox::warning(this, tr("Device Open Error"), tr("DlnOpenDevice() returns 0x") + QString::number(result, 16));
        ui->id->setText("");
        ui->id->setEnabled(false);
        ui->getIdButton->setEnabled(false);
        ui->setIdButton->setEnabled(false);
    }
}

void MainWindow::closeDevice()
{
    DlnCloseHandle(handle);
    handle = HDLN_INVALID_HANDLE;
}

void MainWindow::getId()
{
    uint32_t id;
    DLN_RESULT result = DlnGetDeviceId(handle, &id);
    if (DLN_SUCCEEDED(result))
        ui->id->setText(QString::number(id));
    else
        QMessageBox::warning(this, tr("Get Device ID Failed"), tr("DlnGetDeviceId() returns 0x") + QString::number(result, 16));
}

void MainWindow::setId()
{
    bool ok;
    uint32_t id = ui->id->text().toULong(&ok);
    if (ok)
    {
        DLN_RESULT result = DlnSetDeviceId(handle, id);
        if (!DLN_SUCCEEDED(result))
            QMessageBox::warning(this, tr("Set Device ID Failed"), tr("DlnSetDeviceId() returns 0x") + QString::number(result, 16));
    }
    else
    {
        QMessageBox::warning(this, tr("Invalid Device ID"),
                             tr("Device ID must be in the range from 0 to 4294967295"));
        ui->id->setFocus();
    }

}
