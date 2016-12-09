#include <QMessageBox>
#include "mainwindow.h"
#include "ui_mainwindow.h"

/*!
  Constructor connects getVersionButton clicked signal to getVersion slot
  */
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->getVersionButton, SIGNAL(clicked()), this, SLOT(getVersion()));
}

MainWindow::~MainWindow()
{
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

/*!
  Shows version information at the dialog.
  \param version - version information retrieved with DLN_GetVersion() function.
  */
void MainWindow::showVersion(DLN_VERSION version)
{
    switch (version.hardwareType)
    {
    case DLN_HW_TYPE_DLN1:
        ui->hardwareType->setText(tr("DLN-1"));
        break;
    case DLN_HW_TYPE_DLN2:
        ui->hardwareType->setText(tr("DLN-2"));
        break;
    case DLN_HW_TYPE_DLN4M:
        ui->hardwareType->setText(tr("DLN-4M"));
        break;
    case DLN_HW_TYPE_DLN4S:
        ui->hardwareType->setText(tr("DLN-4S"));
        break;
    default:
        ui->hardwareType->setText(QString::number(version.hardwareType));
        break;
    }
    ui->hardwareVersion->setText(QString::number(version.hardwareVersion));
    ui->firmwareVersion->setText(QString::number(version.firmwareVersion));
    ui->serverVersion->setText(QString::number(version.serverVersion));
    ui->libraryVersion->setText(QString::number(version.libraryVersion));
}

/*!
  Connects to local server, opens first device and retrieves version information for this device.
  Uses showVersion() function to display the version information.
  */
void MainWindow::getVersion()
{
    /*!
      Current expample connects to dln_srv that runs on the same PC.
      If you want to connect to another server specify its IP or url in serverHost variable.
      */
    const char* serverHost = "localhost";
    /*!
      In current example we assume that server uses the default server port.
      You can change the server port, changing the serverPort variable.
      */
    uint16_t serverPort = DLN_DEFAULT_SERVER_PORT;

    //! connect to dln_srv
    DLN_RESULT result = DlnConnect(serverHost, serverPort);
    if (DLN_SUCCEEDED(result))
    {
        HDLN handle;
        //! open first available device
        result = DlnOpenDevice(0, &handle);
        if (DLN_SUCCEEDED(result))
        {
            DLN_VERSION version;
            //! retrieve version information
            result = DlnGetVersion(handle, &version);
            if (DLN_SUCCEEDED(result))
            {
                showVersion(version);
            }
            else
            {
                QMessageBox::warning(this, tr("Get Version Error"),
                                     tr("DlnGetVersion() failed"));
            }
            //! close device handle returned by DLN_OpenDevice() function
            DlnCloseHandle(handle);
        }
        else
        {
            QMessageBox::warning(this, tr("Device Open Error"),
                                 tr("Failed to open device"));
        }
        //! disconnect from dln_srv
        DlnDisconnect(serverHost, serverPort);
    }
    else
    {
        QMessageBox::warning(this, tr("Connection Error"),
                             tr("Failed to connect to local DLN server"));
    }

}
