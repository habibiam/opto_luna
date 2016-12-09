#include <QMessageBox>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "../common/dln_adc.h"
#include "../common/dln_gpio.h"

const QEvent::Type DlnEvent = QEvent::Type(QEvent::User + 1);

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QFontMetrics fm = fontMetrics();
    int charWidth = fm.averageCharWidth();
    ui->eventList->setColumnWidth(0, 10 * charWidth);
    ui->eventList->setColumnWidth(1, 10 * charWidth);
    ui->eventList->setColumnWidth(2, 10 * charWidth);
    ui->eventList->setColumnWidth(3, 50 * charWidth);
    connect(ui->actionClear, SIGNAL(triggered()), SLOT(clearList()));
    ui->actionAutoscroll->setChecked(true);

    DLN_NOTIFICATION notification;
    notification.type = DLN_NOTIFICATION_TYPE_CALLBACK;
    notification.callback.function = dlnCallback;
    notification.callback.context = this;
    DlnRegisterNotification(HDLN_ALL_DEVICES, notification);
    OpenAllDevices();
}

MainWindow::~MainWindow()
{
    DlnUnregisterNotification(HDLN_ALL_DEVICES);
    DlnCloseAllHandles();
    delete ui;
}

void MainWindow::dlnCallback(HDLN handle, void *context)
{
    QApplication::postEvent((QObject*)context, new QEvent(DlnEvent));
}

void MainWindow::customEvent(QEvent *event)
{
    if (event->type() == DlnEvent)
    {
        unsigned char buffer[DLN_MAX_MSG_SIZE];
        while (DLN_SUCCEEDED(DlnGetMessage(HDLN_ALL_DEVICES, buffer, DLN_MAX_MSG_SIZE)))
        {
            DLN_MSG_HEADER *header = (DLN_MSG_HEADER*) buffer;

            // DLN_DEVICE_ADDED_EV event doesn't contain device handle - device is not opened yet.
            // To show device ID and SN in the events list, we open the device and change the handle
            // in the DLN_DEVICE_ADDED_EV with the new one.
            // This way the DLN_DEVICE_ADDED_EV can be processed as any other event.
            if (header->msgId == DLN_MSG_ID_DEVICE_ADDED_EV)
                header->handle = OpenDevice((DLN_DEVICE_ADDED_EV*)header);

            // Add event details to the events list
            int newRow = ui->eventList->rowCount();
            ui->eventList->insertRow(newRow);
            ui->eventList->setItem(newRow, 0, new QTableWidgetItem(getDeviceSn(header->handle)));
            ui->eventList->setItem(newRow, 1, new QTableWidgetItem(getDeviceId(header->handle)));
            ui->eventList->setItem(newRow, 2, new QTableWidgetItem(getModuleName(header->msgId)));
            ui->eventList->setItem(newRow, 3, new QTableWidgetItem(getEventName(header->msgId)));
            ui->eventList->setItem(newRow, 4, new QTableWidgetItem(getMessageData(buffer)));
            if (ui->actionAutoscroll->isChecked())
                ui->eventList->setCurrentCell(newRow, 0);

            // After we added the DLN_DEVICE_REMOVED_EV to the events list, we can close
            // the device handle and release resources associated with current device.
            if (header->msgId == DLN_MSG_ID_DEVICE_REMOVED_EV)
                CloseDevice(header->handle);
        }
    }
}

HDLN MainWindow::OpenDevice(DLN_DEVICE_ADDED_EV *deviceAddedEvent)
{
    HDLN handle;
    DLN_RESULT result = DlnOpenDeviceBySn(deviceAddedEvent->sn, &handle);
    if (DLN_SUCCEEDED(result))
    {
        DeviceDetails details;
        details.id = deviceAddedEvent->id;
        details.sn = deviceAddedEvent->sn;
        _deviceDetails[handle] = details;
        return handle;
    }
    else
    {
        return HDLN_INVALID_HANDLE;
    }
}

void MainWindow::CloseDevice(HDLN handle)
{
    DlnCloseHandle(handle);
    _deviceDetails.remove(handle);
}

void MainWindow::OpenAllDevices()
{
    uint32_t deviceCount;
    DLN_RESULT result = DlnGetDeviceCount(&deviceCount);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, QObject::tr("DlnGetDeviceCount() failed"),
                             QObject::tr("DlnGetDeviceCount() returns 0x") + QString::number(result, 16));
        return;
    }
    for (uint32_t i = 0; i < deviceCount; i++)
    {
        HDLN handle;
        DeviceDetails details;
        result = DlnOpenDevice(0, &handle);
        if (!DLN_SUCCEEDED(result))
            continue;
        DlnGetDeviceId(handle, &details.id);
        DlnGetDeviceSn(handle, &details.sn);
        _deviceDetails[handle] = details;
    }
}

QString MainWindow::getDeviceId(HDLN handle)
{
    switch (handle)
    {
    case HDLN_ALL_DEVICES:
        return tr("-");
    case HDLN_INVALID_HANDLE:
        return tr("Invalid");
    default:
        return QString::number(_deviceDetails[handle].id);
    }
}

QString MainWindow::getDeviceSn(HDLN handle)
{
    switch (handle)
    {
    case HDLN_ALL_DEVICES:
        return tr("-");
    case HDLN_INVALID_HANDLE:
        return tr("Invalid");
    default:
        return QString::number(_deviceDetails[handle].sn);
    }
}


QString MainWindow::getModuleName(uint16_t msgId)
{
    uint8_t module = DLN_GET_MSG_MODULE(msgId);
    switch (module)
    {
    case DLN_MODULE_GENERIC:
        return tr("Generic");
    case DLN_MODULE_GPIO:
        return tr("GPIO");
    case DLN_MODULE_SPI_MASTER:
        return tr("SPI Master");
    case DLN_MODULE_I2C_MASTER:
        return tr("I2C Master");
    case DLN_MODULE_I2S:
        return tr("I2S");
    case DLN_MODULE_PWM:
        return tr("PWM");
    case DLN_MODULE_FREQ:
        return tr("FREQ");
    case DLN_MODULE_ADC:
        return tr("ADC");
    case DLN_MODULE_LED:
        return tr("LED");
    default:
        return QString("%1").arg(module, 2, 16, QChar('0')).toUpper();
    }
}

QString MainWindow::getEventName(uint16_t msgId)
{
    switch (msgId)
    {
    case DLN_MSG_ID_CONNECTION_LOST_EV:
        return tr("DLN_MSG_ID_CONNECTION_LOST_EV");
    case DLN_MSG_ID_DEVICE_REMOVED_EV:
        return tr("DLN_MSG_ID_DEVICE_REMOVED_EV");
    case DLN_MSG_ID_DEVICE_ADDED_EV:
        return tr("DLN_MSG_ID_DEVICE_ADDED_EV");
    case DLN_MSG_ID_ADC_CONDITION_MET_EV:
        return tr("DLN_MSG_ID_ADC_CONDITION_MET_EV");
    case DLN_MSG_ID_GPIO_CONDITION_MET_EV:
        return tr("DLN_MSG_ID_GPIO_CONDITION_MET_EV");
    default:
        return QString("%1").arg(msgId, 4, 16, QChar('0')).toUpper();
    }
}

QString MainWindow::getMessageData(unsigned char *buffer)
{
    DLN_MSG_HEADER *header = (DLN_MSG_HEADER*) buffer;
    QString hex;
    for (uint16_t i = sizeof(DLN_MSG_HEADER); i < header->size; i++)
        hex += QString("%1").arg(buffer[i], 2, 16, QChar('0')).toUpper() + " ";
    return hex;
}

void MainWindow::clearList()
{
    ui->eventList->setRowCount(0);
}
