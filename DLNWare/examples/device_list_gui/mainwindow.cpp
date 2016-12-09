#include <QMessageBox>
#include <QDebug>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "connectdialog.h"
#include "../common/dln.h"

const QEvent::Type DlnEvent = QEvent::Type(QEvent::User + 1);

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    connectDialog(new ConnectDialog(this))
{
    ui->setupUi(this);
    connect(ui->connectButton, SIGNAL(clicked()), this, SLOT(connectServer()));
    connect(ui->disconnectSelectedButton, SIGNAL(clicked()), this, SLOT(disconnectSelected()));
    connect(ui->disconnectAllButton, SIGNAL(clicked()), this, SLOT(disconnectAll()));
    connect(ui->updateDeviceListButton, SIGNAL(clicked()), this, SLOT(updateDeviceList()));
    connect(ui->serverList, SIGNAL(itemSelectionChanged()), this, SLOT(serverSelectionChanged()));
    DLN_NOTIFICATION notification;
    notification.type = DLN_NOTIFICATION_TYPE_CALLBACK;
    notification.callback.function = dlnCallback;
    notification.callback.context = this;
    DlnRegisterNotification(HDLN_ALL_DEVICES, notification);

}

MainWindow::~MainWindow()
{
    DlnUnregisterNotification(HDLN_ALL_DEVICES);
    DlnCloseAllHandles();
    DlnDisconnectAll();
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

void MainWindow::showConnectionError(DLN_RESULT result)
{
    QString errorText;
    switch (result)
    {
    case DLN_RES_HOST_LOOKUP_FAILED:
        errorText = tr("Cannot locate the specified host.");
        break;
    case DLN_RES_CONNECTION_FAILED:
        errorText = tr("Cannon connect to the specified DLN server.");
        break;
    case DLN_RES_HOST_NAME_TOO_LONG:
        errorText = tr("Host name length should not exceed ") + QString::number(DLN_MAX_HOST_LENGTH) + tr("characters.");
        break;
    case DLN_RES_ALREADY_CONNECTED:
        errorText = tr("You are already connected to the specified DLN server");
        break;
    default:
        errorText = tr("Connection failed, DlnConnect() returns 0x") + QString::number(result, 16) + tr(".");
        break;
    }
    QMessageBox::warning(this, tr("Connection Error"), errorText);
}

void MainWindow::showDisconnectionError(DLN_RESULT result, QString host, uint16_t port)
{
    QString errorText;
    switch (result)
    {
    case DLN_RES_NOT_CONNECTED:
        errorText = tr("We are already disconnected from server ") + host + tr(":") + QString::number(port) + tr(".");
        break;
    default:
        errorText = tr("DlnDisconnect(") + host + tr(", ") + QString::number(port) + tr(") returns 0x") + QString::number(result, 16) + tr(".");
        break;
    }
    QMessageBox::warning(this, tr("Disconnection Error"), errorText);
}

void MainWindow::connectServer()
{
    if (QDialog::Accepted == connectDialog->exec())
    {
        QString hostString = connectDialog->host();
        QString portString = connectDialog->port();
        uint16_t port = portString.toUShort();
        DLN_RESULT result = DlnConnect(hostString.toAscii().data(), port);
        if (DLN_SUCCEEDED(result))
        {
            int newRow = ui->serverList->rowCount();
            ui->serverList->insertRow(newRow);
            ui->serverList->setItem(newRow, 0, new QTableWidgetItem(hostString));
            ui->serverList->setItem(newRow, 1, new QTableWidgetItem(portString));
            ui->disconnectAllButton->setEnabled(true);
            ui->updateDeviceListButton->setEnabled(true);
            updateDeviceList();
        }
        else
        {
            showConnectionError(result);
        }
    }
}

void MainWindow::disconnectServer(QString host, uint16_t port)
{
    for (int i = 0; i < ui->serverList->rowCount(); i++)
    {
        if ((host == ui->serverList->item(i, 0)->text()) &&
            (port == ui->serverList->item(i, 1)->text().toUShort()))
        {
            ui->serverList->removeRow(i);
            break;
        }
    }
    DlnDisconnect(host.toAscii().data(), port);
    updateDeviceList();
    if (ui->serverList->rowCount() == 0)
    {
        ui->updateDeviceListButton->setEnabled(false);
        ui->disconnectAllButton->setEnabled(false);
        ui->disconnectSelectedButton->setEnabled(false);
    }
}

void MainWindow::disconnectSelected()
{
    for (int i = ui->serverList->rowCount() - 1; i >= 0; i--)
    {
        if (ui->serverList->item(i, 0)->isSelected())
        {
            QString host = ui->serverList->item(i, 0)->text();
            uint16_t port = ui->serverList->item(i, 1)->text().toUShort();
            //= portString.toUShort();
            DLN_RESULT result = DlnDisconnect(host.toAscii().data(), port);
            if (!DLN_SUCCEEDED(result))
                showDisconnectionError(result, host, port);
            ui->serverList->removeRow(i);

        }
    }
    updateDeviceList();
    if (ui->serverList->rowCount() == 0)
    {
        ui->updateDeviceListButton->setEnabled(false);
        ui->disconnectAllButton->setEnabled(false);
        ui->disconnectSelectedButton->setEnabled(false);
    }
}

void MainWindow::disconnectAll()
{
    DlnDisconnectAll();
    ui->serverList->setRowCount(0);;
    ui->disconnectAllButton->setEnabled(false);
    ui->disconnectSelectedButton->setEnabled(false);
    ui->deviceList->setRowCount(0);
    ui->updateDeviceListButton->setEnabled(false);
}

QString MainWindow::getDeviceType(DLN_VERSION version)
{
    switch (version.hardwareType)
    {
    case DLN_HW_TYPE_DLN1:
        return tr("DLN-1");
    case DLN_HW_TYPE_DLN2:
        return tr("DLN-2");
    case DLN_HW_TYPE_DLN4M:
        return tr("DLN-4M");
    case DLN_HW_TYPE_DLN4S:
        return tr("DLN-4S");
    default:
        return QString::number(version.hardwareType);
    }
}

void MainWindow::updateDeviceList()
{
    ui->deviceList->setRowCount(0);
    DlnCloseAllHandles();
    uint32_t deviceCount;
    DLN_RESULT result = DlnGetDeviceCount(&deviceCount);
    if (DLN_SUCCEEDED(result))
    {
        for (uint32_t i = 0; i < deviceCount; i++)
        {
            HDLN handle;
            result = DlnOpenDevice(i, &handle);
            if (DLN_SUCCEEDED(result))
            {
                DLN_VERSION version;
                uint32_t sn, id;
                DlnGetVersion(handle, &version);
                DlnGetDeviceSn(handle, &sn);
                DlnGetDeviceId(handle, &id);
                ui->deviceList->insertRow(i);
                ui->deviceList->setItem(i, 0, new QTableWidgetItem(getDeviceType(version)));
                ui->deviceList->setItem(i, 1, new QTableWidgetItem(QString::number(sn)));
                ui->deviceList->setItem(i, 2, new QTableWidgetItem(QString::number(id)));
                ui->deviceList->setItem(i, 3, new QTableWidgetItem("0x" + QString::number(version.hardwareVersion, 16)));
                ui->deviceList->setItem(i, 4, new QTableWidgetItem("0x" + QString::number(version.firmwareVersion, 16)));
                ui->deviceList->setItem(i, 5, new QTableWidgetItem("0x" + QString::number(version.serverVersion, 16)));
                ui->deviceList->setItem(i, 6, new QTableWidgetItem("0x" + QString::number(version.libraryVersion, 16)));
            }
        }
    }

}

void MainWindow::serverSelectionChanged()
{
    if (ui->serverList->selectedItems().isEmpty())
        ui->disconnectSelectedButton->setEnabled(false);
    else
        ui->disconnectSelectedButton->setEnabled(true);

}


void MainWindow::customEvent(QEvent *event)
{
    if (event->type() == DlnEvent)
    {
        unsigned char buffer[DLN_MAX_MSG_SIZE];
        while (DLN_SUCCEEDED(DlnGetMessage(HDLN_ALL_DEVICES, buffer, DLN_MAX_MSG_SIZE)))
        {
            DLN_MSG_HEADER *header = (DLN_MSG_HEADER*) buffer;
            switch (header->msgId)
            {
            case DLN_MSG_ID_DEVICE_ADDED_EV:
            case DLN_MSG_ID_DEVICE_REMOVED_EV:
                updateDeviceList();
                break;
            case DLN_MSG_ID_CONNECTION_LOST_EV:
                DLN_CONNECTION_LOST_EV *connectionLostEv = (DLN_CONNECTION_LOST_EV*)buffer;
                Q_ASSERT(connectionLostEv->header.size == sizeof(DLN_CONNECTION_LOST_EV));
                qDebug("host = %s, port = %d", connectionLostEv->host, connectionLostEv->port);
                disconnectServer(connectionLostEv->host, connectionLostEv->port);
                updateDeviceList();
                break;
            }
        }
    }
    else
    {
        QMainWindow::customEvent(event);
    }
}

void MainWindow::dlnCallback(HDLN handle, void *context)
{
    handle = handle;
    QApplication::postEvent((QObject*)context, new QEvent(DlnEvent));
}
