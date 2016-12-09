#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln_spi_slave.h"

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
    void getConfiguration();
    void setEnabled();
    void setSpiSlaveMode();
    void getSpiSlaveMode();
    void setFrameSize();
    void getFrameSize();
    void loadReply();
    void setEventSize();
    void getEventSize();
    void setEventEnable();
    void enqueueReply();
    void setShortage();
    void getShortage();
private:
    Ui::MainWindow *ui;
    HDLN _handle;
    void enableControls(bool enable);
    void getEnabled();
    void getEventEnable();
    void getSupportedFrameSizes();
    void getSupportedCpolValues();
    void getSupportedCphaValues();
};

#endif // MAINWINDOW_H
