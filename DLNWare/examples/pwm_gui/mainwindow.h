#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln_pwm.h"

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
    void setPwmPort();
    void setPwmChannel();
    void getPwmChannel();
    void setFrequency();
    void setDutyCycle();
    void getFrequency();
    void getDutyCycle();

private:
    Ui::MainWindow *ui;
    HDLN _handle;
    void enableControls(bool enable);
    bool initPwmPortCombo();
    bool initPwmChannelCombo();
    void getPwmPort();
};

#endif // MAINWINDOW_H
