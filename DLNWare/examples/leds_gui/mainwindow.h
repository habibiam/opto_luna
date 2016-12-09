#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln_led.h"

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(HDLN handle, QWidget *parent = 0);
    ~MainWindow();
private slots:
    void ledStateChanged(uint8_t ledNumber, DLN_LED_STATE newState);

private:
    Ui::MainWindow *ui;
    void addLed(uint8_t ledNumber);
    HDLN _handle;
};

#endif // MAINWINDOW_H
