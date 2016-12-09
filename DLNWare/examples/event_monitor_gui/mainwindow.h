#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMap>
#include "../common/dln_generic.h"

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

    void customEvent(QEvent *event);

    static void dlnCallback(HDLN handle, void *context);
    struct DeviceDetails
    {
        uint32_t id;
        uint32_t sn;
    };

    QMap<HDLN, DeviceDetails> _deviceDetails;
    QString getDeviceId(HDLN handle);
    QString getDeviceSn(HDLN handle);
    QString getModuleName(uint16_t msgId);
    QString getEventName(uint16_t msgId);
    QString getMessageData(unsigned char *buffer);

    HDLN OpenDevice(DLN_DEVICE_ADDED_EV *deviceAddedEvent);
    void CloseDevice(HDLN handle);
    void OpenAllDevices();
private slots:
    void clearList();

};

#endif // MAINWINDOW_H
