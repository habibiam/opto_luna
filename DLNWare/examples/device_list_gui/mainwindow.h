#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QEvent>
#include "../common/dln_generic.h"

namespace Ui {
    class MainWindow;
}

class ConnectDialog;


class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();

protected:
    void changeEvent(QEvent *e);
private slots:
    void connectServer();
    void disconnectSelected();
    void disconnectAll();
    void updateDeviceList();
    void serverSelectionChanged();
private:
    Ui::MainWindow *ui;
    ConnectDialog *connectDialog;
    void disconnectServer(QString host, uint16_t port);
    void showConnectionError(DLN_RESULT result);
    void showDisconnectionError(DLN_RESULT result, QString host, uint16_t port);
    QString getDeviceType(DLN_VERSION version);
    void customEvent(QEvent * event);
    static void dlnCallback(HDLN handle, void *context);
};

#endif // MAINWINDOW_H
