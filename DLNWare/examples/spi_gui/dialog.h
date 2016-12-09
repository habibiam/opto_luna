#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include "../common/dln_spi_master.h"

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
    void readWrite();
    void setFrequency();
    void getFrequency();
    void setDelayBetweenSS();
    void getDelayBetweenSS();
    void setSpiMasterMode();
    void getSpiMasterMode();
    void spiMasterPortConfig();
    void setDelayAfterSS();
    void getDelayAfterSS();
    void setFrameSize();
    void getFrameSize();
    void setDelayBetweenFrames();
    void getDelayBetweenFrames();
    void setSSPin();
    void getSSPin();
    void setSSBetweenFrames();
    void readWriteEx();
    void read();
    void write();
    void readEx();
    void writeEx();
    void setSS0Enabled();
    void setSS1Enabled();
    void setSS2Enabled();
    void setSS3Enabled();
    void setSS4Enabled();

private:
    Ui::Dialog *ui;
    HDLN _handle;
    bool initPortCombo();
    void initDecodeCombo(bool enable);
    void enableControls(bool enable);
    bool spiMasterIsEnabled();
    void getSSBetweenFrames();
    void initSS();
    uint8_t getPort();
    void isSSEnabled();
};

#endif // DIALOG_H
