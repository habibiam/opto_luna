#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln_i2c_slave.h"

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
private slots:
    void openDevice();
    bool initPortCombo();
    bool initSlaveAddressNumCombo();
    void getConfiguration();
    void setEnabled();
    void setAddress();
    void getAddress();
    void loadReply();
    void setEvent();
    void getEvent();
    void setGeneralCall();
private:
    Ui::MainWindow *ui;
    HDLN _handle;
    void enableControls(bool enable);
    void getEnabled();
    void getGeneralCall();
};

#endif // MAINWINDOW_H
