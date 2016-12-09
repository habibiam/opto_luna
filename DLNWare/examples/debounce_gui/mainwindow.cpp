#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "../common/dln_gpio.h"
#include "../common/dln_generic.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    if (_handle != HDLN_INVALID_HANDLE)
        DlnCloseHandle(_handle);
    delete ui;
}

void MainWindow::changeEvent(QEvent *e)
{
    QMainWindow::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}

void MainWindow::on_buttonSetDebounce_clicked()
{
    DLN_RESULT result;
    result = DlnOpenDevice(0, &_handle);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, tr("Failed to open DLN adapter. Please check connection."),  tr("DLN adapter openning error"));
        DlnDisconnectAll();
    }

    bool ok;

    uint32_t debounce = ui->lineEditInputDebounce->text().toUInt(&ok);

    if (ok == false)
    {
        QMessageBox::warning(NULL, tr("Invalid debouncePeriod"),
                             tr("eventPeriod must be in the range from 0 to 1000000"));
        ui->lineEditInputDebounce->setFocus();
        return;
    }
    result = DlnGpioSetDebounce(_handle, debounce, 0);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, tr("DlnGpioSetDebounce() failed"),
                             tr("DlnGpioSetDebounce() function returns 0x") + QString::number(result, 16).toUpper());
    }

/*    debounce = 0;
    result = DlnGpioGetDebounce(_handle, &debounce);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, tr("DlnGpioGetDebounce() failed"),
                             tr("DlnGpioGetDebounce() function returns 0x") + QString::number(result, 16).toUpper());
    } */
    ui->lineEditRealDebounce->setText(QString::number(debounce));
}
