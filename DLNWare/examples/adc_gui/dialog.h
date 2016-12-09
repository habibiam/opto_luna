#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include "../common/dln_adc.h"

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
    void openDevice();
    void getConfiguration();
    void setAdc();
    void setResolution();
    void getResolution();
    void getAdcValue();
    void getAdcAllValues();
    void setChannelCfg();
    void getChannelCfg();
    void setAdcChannel();
    void getAdcChannel();
private:
    Ui::Dialog *ui;
    HDLN _handle;
    void enableControls(bool enable);
    bool initAdcPortCombo();
    void getAdc();
    bool initAdcChannelCombo();
};

#endif // DIALOG_H
