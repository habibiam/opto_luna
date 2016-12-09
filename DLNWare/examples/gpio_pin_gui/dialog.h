#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include "../common/dln_gpio.h"

namespace Ui {
    class Dialog;
}

class Dialog : public QDialog
{
    Q_OBJECT

public:
    explicit Dialog(QWidget *parent = 0);
    ~Dialog();
private slots:
    void setEnabled();
    void getValue();
    void openDevice();
    void setDirection();
    void getDirection();
    void setOutputValue();
    void getOutputValue();
    void setOpenDrain();
    void setPullUp();
    void setPullDown();
    void setDebounce();
    void setEventCfg();
    void getEventCfg();
    void getConfiguration();
private:
    Ui::Dialog *ui;
    HDLN _handle;
    bool initPinCombo();
    void enableControls(bool enable);
    void getEnabled();
    void getOpenDrain();
    void getPullUp();
    void getPullDown();
    void getDebounce();
    void initEventCfgCombo();

};

#endif // DIALOG_H
