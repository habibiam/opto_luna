#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln_pls_cnt.h"

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
    void getConfiguration();
    void setEnabled();
    void setSuspended();
    void resetCounter();
    void getResolution();
    void getValue();
    void setMode();
    void getMode();
    void setEventCfg();
    void getEventCfg();
private:
    Ui::MainWindow *ui;
    HDLN _handle;
    void enableControls(bool enable);
    bool initPlsCntPortCombo();
    void getEnabled();
    void getSuspended();
};

#endif // MAINWINDOW_H
