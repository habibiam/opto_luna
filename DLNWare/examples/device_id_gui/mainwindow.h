#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../common/dln.h"

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
    void getId();
    void setId();

private:
    Ui::MainWindow *ui;
    void closeDevice();
    HDLN handle;

};

#endif // MAINWINDOW_H
