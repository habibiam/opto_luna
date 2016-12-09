#include "dialog.h"
#include "ui_dialog.h"
#include <QMessageBox>
#include <QByteArray>
#include "../common/dln_generic.h"
#include "../common/dln_spi_master.h"

Dialog::Dialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog),
    _handle(HDLN_INVALID_HANDLE)
{
    ui->setupUi(this);
    connect(ui->openDeviceButton, SIGNAL(clicked()), SLOT(openDevice()));
    connect(ui->readWriteButton, SIGNAL(clicked()), SLOT(readWrite()));
    connect(ui->setFrequencyPushButton, SIGNAL(clicked()), SLOT(setFrequency()));
    connect(ui->getFrequencyPushButton, SIGNAL(clicked()), SLOT(getFrequency()));
    connect(ui->enabledCheckBox, SIGNAL(stateChanged(int)), SLOT(spiMasterPortConfig()));
    connect(ui->setModePushButton, SIGNAL(clicked()), SLOT(setSpiMasterMode()));
    connect(ui->getModePushButton, SIGNAL(clicked()), SLOT(getSpiMasterMode()));
    connect(ui->setDelayBetweenSSPushButton, SIGNAL(clicked()), SLOT(setDelayBetweenSS()));
    connect(ui->getDelayBetweenSSPushButton, SIGNAL(clicked()), SLOT(getDelayBetweenSS()));
    connect(ui->setDelayAfterSSPushButton, SIGNAL(clicked()), SLOT(setDelayAfterSS()));
    connect(ui->getDelayAfterSSPushButton, SIGNAL(clicked()), SLOT(getDelayAfterSS()));
    connect(ui->setFrameSizePushButton, SIGNAL(clicked()), SLOT(setFrameSize()));
    connect(ui->getFrameSizePushButton, SIGNAL(clicked()), SLOT(getFrameSize()));
    connect(ui->setDelayBetweenFramesPushButton, SIGNAL(clicked()), SLOT(setDelayBetweenFrames()));
    connect(ui->getDelayBetweenFramesPushButton, SIGNAL(clicked()), SLOT(getDelayBetweenFrames()));
    connect(ui->setSSPinPushButton, SIGNAL(clicked()), SLOT(setSSPin()));
    connect(ui->getSSPinPushButton, SIGNAL(clicked()), SLOT(getSSPin()));
    connect(ui->ssBetweenFramesCheckBox, SIGNAL(stateChanged(int)), SLOT(setSSBetweenFrames()));
    connect(ui->writeButton, SIGNAL(clicked()), SLOT(write()));
    connect(ui->readButton, SIGNAL(clicked()), SLOT(read()));
    connect(ui->writeExButton, SIGNAL(clicked()), SLOT(writeEx()));
    connect(ui->readExButton, SIGNAL(clicked()), SLOT(readEx()));
    connect(ui->readWriteExButton, SIGNAL(clicked()), SLOT(readWriteEx()));
    connect(ui->ss0Enabled, SIGNAL(stateChanged(int)), SLOT(setSS0Enabled()));
    connect(ui->ss1Enabled, SIGNAL(stateChanged(int)), SLOT(setSS1Enabled()));
    connect(ui->ss2Enabled, SIGNAL(stateChanged(int)), SLOT(setSS2Enabled()));
    connect(ui->ss3Enabled, SIGNAL(stateChanged(int)), SLOT(setSS3Enabled()));
    connect(ui->ss4Enabled, SIGNAL(stateChanged(int)), SLOT(setSS4Enabled()));

    openDevice();
}

Dialog::~Dialog()
{
    if (_handle != HDLN_INVALID_HANDLE)
        DlnCloseHandle(_handle);
    delete ui;
}

void Dialog::openDevice()
{
    enableControls(false);
    if (_handle != HDLN_INVALID_HANDLE)
    {
        DlnCloseHandle(_handle);
        _handle = HDLN_INVALID_HANDLE;
    }
    DLN_RESULT result = DlnOpenDevice(0, &_handle);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DLN adapter openning error"),
                             tr("Failed to open DLN-series adapter. DlnOpenDevice() returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if (initPortCombo())
    {
        enableControls(true);
        getConfiguration();
    }
}

bool Dialog::initPortCombo()
{
    ui->port->clear();
    uint8_t count;
    DLN_RESULT result = DlnSpiMasterGetPortCount(_handle, &count);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetPortCount() failed"),
                             tr("DlnSpiGetPortCount() function returns 0x") + QString::number(result, 16).toUpper());
        return false;
    }
    if (count == 0)
    {
        QMessageBox::warning(this, tr("No SPI ports"),
                             tr("Current DLN adapter has no SPI ports"));
        return false;
    }
    for (uint8_t i = 0; i < count; i++)
        ui->port->addItem(QString::number(i));
    ui->port->setCurrentIndex(0);
    return true;
}

uint8_t Dialog::getPort()
{
    return ui->port->currentIndex();
}


void Dialog::setFrequency()
{
    uint32_t actualFrequency;
    DLN_RESULT result = DlnSpiMasterSetFrequency(_handle, getPort(),ui->frequencyLineEdit->text().toUInt(), &actualFrequency);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetFrequency() failed"),
                             tr("DlnSpiMasterSetFrequency() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("Set Frequency"),
                             tr("Frequency value was rounded to ") + QString::number(actualFrequency));
    }
    ui->frequencyLineEdit->setText(QString::number(actualFrequency));
}

void Dialog::getFrequency()
{
    uint32_t actualFrequency;
    DLN_RESULT result = DlnSpiMasterGetFrequency(_handle, getPort(), &actualFrequency);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetFrequency() failed"),
                             tr("DlnSpiMasterGetFrequency() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->frequencyLineEdit->setText(QString::number(actualFrequency));
}

void Dialog::setDelayBetweenSS()
{
    uint32_t actualDelayBetweenSS;
    DLN_RESULT result = DlnSpiMasterSetDelayBetweenSS(_handle, getPort(), ui->delayBetweenSSLineEdit->text().toUInt(), &actualDelayBetweenSS);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetDelayBetweenSS() failed"),
                             tr("DlnSpiMasterSetDelayBetweenSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("Set Delay Between SS"),
                             tr("Delay value was rounded to ") + QString::number(actualDelayBetweenSS));
    }
    ui->delayBetweenSSLineEdit->setText(QString::number(actualDelayBetweenSS));
}

void Dialog::getDelayBetweenSS()
{
    uint32_t delayBetweenSS;
    DLN_RESULT result = DlnSpiMasterGetDelayBetweenSS(_handle, getPort(), &delayBetweenSS);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetDelayBetweenSS() failed"),
                             tr("DlnSpiMasterSetDelayBetweenSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->delayBetweenSSLineEdit->setText(QString::number(delayBetweenSS));
}

void Dialog::setDelayAfterSS()
{
    uint32_t actualDelayAfterSS;
    DLN_RESULT result = DlnSpiMasterSetDelayAfterSS(_handle, getPort(), ui->delayAfterSSLineEdit->text().toUInt(), &actualDelayAfterSS);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetDelayAfterSS() failed"),
                             tr("DlnSpiMasterSetDelayAfterSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("Set Delay After SS"),
                             tr("Delay value was rounded to ") + QString::number(actualDelayAfterSS));
    }
    ui->delayAfterSSLineEdit->setText(QString::number(actualDelayAfterSS));
}

void Dialog::getDelayAfterSS()
{
    uint32_t delayAfterSS;
    DLN_RESULT result = DlnSpiMasterGetDelayAfterSS(_handle, getPort(), &delayAfterSS);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetDelayAfterSS() failed"),
                             tr("DlnSpiMasterGetDelayAfterSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->delayAfterSSLineEdit->setText(QString::number(delayAfterSS));
}

void Dialog::setFrameSize()
{
    DLN_RESULT result = DlnSpiMasterSetFrameSize(_handle, getPort(), ui->frameSizeComboBox->currentText().toUInt());
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetFrameSize() failed"),
                             tr("DlnSpiMasterSetFrameSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getFrameSize()
{
    uint8_t frameSize;
    DLN_RESULT result = DlnSpiMasterGetFrameSize(_handle, getPort(), &frameSize);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetFrameSize() failed"),
                             tr("DlnSpiMasterGetFrameSize() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    int index = ui->frameSizeComboBox->findText(QString::number(frameSize));
    ui->frameSizeComboBox->setCurrentIndex(index);
}

void Dialog::setDelayBetweenFrames()
{
    uint32_t actualDelayBetweenFrames;
    DLN_RESULT result = DlnSpiMasterSetDelayBetweenFrames(_handle, getPort(), ui->delayBetweenFramesLineEdit->text().toUInt(), &actualDelayBetweenFrames);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetDelayBetweenFrames() failed"),
                             tr("DlnSpiMasterSetDelayBetweenFrames() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    if(result == DLN_RES_VALUE_ROUNDED)
    {
        QMessageBox::warning(this, tr("Set Delay Between Frames"),
                             tr("Delay value was rounded to ") + QString::number(actualDelayBetweenFrames));
    }
    ui->delayBetweenFramesLineEdit->setText(QString::number(actualDelayBetweenFrames));
}

void Dialog::getDelayBetweenFrames()
{
    uint32_t delayBetweenFrames;
    DLN_RESULT result = DlnSpiMasterGetDelayBetweenFrames(_handle, getPort(), &delayBetweenFrames);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetDelayBetweenFrames() failed"),
                             tr("DlnSpiMasterGetDelayBetweenFrames() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->delayBetweenFramesLineEdit->setText(QString::number(delayBetweenFrames));
}

void Dialog::setSpiMasterMode()
{
    uint8_t mode = 0;

    if(ui->cphaComboBox->currentText().toUInt() == 1)
        mode |= DLN_SPI_MASTER_CPHA_1;

    if(ui->cpolComboBox->currentText().toUInt() == 1)
        mode |= DLN_SPI_MASTER_CPOL_1;

    DLN_RESULT result = DlnSpiMasterSetMode(_handle, getPort(), mode);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetMode() failed"),
                             tr("DlnSpiMasterSetMode() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::getSpiMasterMode()
{
    uint8_t mode;
    DLN_RESULT result = DlnSpiMasterGetMode(_handle, getPort(), &mode);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetMode() failed"),
                             tr("DlnSpiMasterGetMode() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    if ((mode & DLN_SPI_MASTER_CPHA_BIT) == DLN_SPI_MASTER_CPHA_1)
        ui->cphaComboBox->setCurrentIndex(1);
    else
        ui->cphaComboBox->setCurrentIndex(0);

    if ((mode & DLN_SPI_MASTER_CPOL_BIT) == DLN_SPI_MASTER_CPOL_1)
        ui->cpolComboBox->setCurrentIndex(1);
    else
        ui->cpolComboBox->setCurrentIndex(0);
}

void Dialog::setSSPin()
{
    uint8_t ss = 0xFF;

    if(ui->ss0->isChecked())
        ss &= ~(1 << 0);
    if(ui->ss1->isChecked())
        ss &= ~(1 << 1);
    if(ui->ss2->isChecked())
        ss &= ~(1 << 2);
    if(ui->ss3->isChecked())
        ss &= ~(1 << 3);
    if(ui->ss4->isChecked())
        ss &= ~(1 << 4);

    DLN_RESULT result = DlnSpiMasterSetSS(_handle, getPort(), ss);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterSetSS() failed"),
                             tr("DlnSpiMasterSetSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::setSS0Enabled()
{
    DLN_RESULT result;

    if(ui->ss0Enabled->isChecked())
    {
        result = DlnSpiMasterSSEnable(_handle, getPort(), 0);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

    if(!ui->ss0Enabled->isChecked())
    {
        result = DlnSpiMasterSSDisable(_handle, getPort(), 0);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void Dialog::setSS1Enabled()
{
    DLN_RESULT result;

    if(ui->ss1Enabled->isChecked())
    {
        result = DlnSpiMasterSSEnable(_handle, getPort(), 1);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

    if(!ui->ss1Enabled->isChecked())
    {
        result = DlnSpiMasterSSDisable(_handle, getPort(), 1);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSDisable() failed"),
                                tr("DlnSpiMasterSSDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }

    }
}


void Dialog::setSS2Enabled()
{
    DLN_RESULT result;

    if(ui->ss2Enabled->isChecked())
    {
        result = DlnSpiMasterSSEnable(_handle, getPort(), 2);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

    if(!ui->ss2Enabled->isChecked())
    {
        result = DlnSpiMasterSSDisable(_handle, getPort(), 2);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSDisable() failed"),
                                tr("DlnSpiMasterSSDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

}

void Dialog::setSS3Enabled()
{
    DLN_RESULT result;

    if(ui->ss3Enabled->isChecked())
    {
        result = DlnSpiMasterSSEnable(_handle, getPort(), 3);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

    if(!ui->ss3Enabled->isChecked())
    {
        result = DlnSpiMasterSSDisable(_handle, getPort(), 3);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSDisable() failed"),
                                tr("DlnSpiMasterSSDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

}

void Dialog::setSS4Enabled()
{
    DLN_RESULT result;

    if(ui->ss4Enabled->isChecked())
    {
        result = DlnSpiMasterSSEnable(_handle, getPort(), 4);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSEnable() failed"),
                                tr("DlnSpiMasterSSEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

    if(!ui->ss4Enabled->isChecked())
    {
        result = DlnSpiMasterSSDisable(_handle, getPort(), 4);
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterSSDisable() failed"),
                                tr("DlnSpiMasterSSDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }

}

void Dialog::isSSEnabled()
{
    uint8_t enabled;
    DlnSpiMasterSSIsEnabled(_handle, getPort(), 0, &enabled);
    ui->ss0Enabled->setChecked(enabled);
    DlnSpiMasterSSIsEnabled(_handle, getPort(), 1, &enabled);
    ui->ss1Enabled->setChecked(enabled);
    DlnSpiMasterSSIsEnabled(_handle, getPort(), 2, &enabled);
    ui->ss2Enabled->setChecked(enabled);
    DlnSpiMasterSSIsEnabled(_handle, getPort(), 3, &enabled);
    ui->ss3Enabled->setChecked(enabled);
    DlnSpiMasterSSIsEnabled(_handle, getPort(), 4, &enabled);
    ui->ss4Enabled->setChecked(enabled);
}

void Dialog::initSS()
{
    uint16_t count;
    DlnSpiMasterGetSSCount(_handle, getPort(), &count);

    ui->ss0->setEnabled(false);
    ui->ss1->setEnabled(false);
    ui->ss2->setEnabled(false);
    ui->ss3->setEnabled(false);
    ui->ss4->setEnabled(false);

    ui->ss0Enabled->setEnabled(false);
    ui->ss1Enabled->setEnabled(false);
    ui->ss2Enabled->setEnabled(false);
    ui->ss3Enabled->setEnabled(false);
    ui->ss4Enabled->setEnabled(false);

    switch(count)
    {
    case 0:
            ui->setSSPinPushButton->setEnabled(false);
            ui->getSSPinPushButton->setEnabled(false);
            return;
    case 1:
            ui->ss0->setEnabled(true);
            if(!spiMasterIsEnabled())
                ui->ss0Enabled->setEnabled(true);
            return;
    case 2:
            ui->ss0->setEnabled(true);
            ui->ss1->setEnabled(true);
            if(!spiMasterIsEnabled())
            {
                ui->ss0Enabled->setEnabled(true);
                ui->ss1Enabled->setEnabled(true);
            }
            return;
    case 3:
            ui->ss0->setEnabled(true);
            ui->ss1->setEnabled(true);
            ui->ss2->setEnabled(true);
            if(!spiMasterIsEnabled())
            {
                ui->ss0Enabled->setEnabled(true);
                ui->ss1Enabled->setEnabled(true);
                ui->ss2Enabled->setEnabled(true);
            }
            return;
    case 4:
            ui->ss0->setEnabled(true);
            ui->ss1->setEnabled(true);
            ui->ss2->setEnabled(true);
            ui->ss3->setEnabled(true);
            if(!spiMasterIsEnabled())
            {
                ui->ss0Enabled->setEnabled(true);
                ui->ss1Enabled->setEnabled(true);
                ui->ss2Enabled->setEnabled(true);
                ui->ss3Enabled->setEnabled(true);
            }
            return;
    case 5:
            ui->ss0->setEnabled(true);
            ui->ss1->setEnabled(true);
            ui->ss2->setEnabled(true);
            ui->ss3->setEnabled(true);
            ui->ss4->setEnabled(true);
            if(!spiMasterIsEnabled())
            {
                ui->ss0Enabled->setEnabled(true);
                ui->ss1Enabled->setEnabled(true);
                ui->ss2Enabled->setEnabled(true);
                ui->ss3Enabled->setEnabled(true);
                ui->ss4Enabled->setEnabled(true);
            }
            return;
    }
}

void Dialog::getSSPin()
{
    uint8_t ss;

    DLN_RESULT result = DlnSpiMasterGetSS(_handle, getPort(), &ss);
    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterGetSS() failed"),
                             tr("DlnSpiMasterGetSS() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->ss0->setChecked((ss & (1 << 0)) == 0);
    ui->ss1->setChecked((ss & (1 << 1)) == 0);
    ui->ss2->setChecked((ss & (1 << 2)) == 0);
    ui->ss3->setChecked((ss & (1 << 3)) == 0);
    ui->ss4->setChecked((ss & (1 << 4)) == 0);
}

void Dialog::setSSBetweenFrames()
{
    if(ui->ssBetweenFramesCheckBox->isChecked())
    {
        DLN_RESULT result = DlnSpiMasterSSBetweenFramesEnable(_handle, getPort());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnSpiMasterSSBetweenFramesEnable() failed"),
                                       tr("DlnSpiMasterSSBetweenFramesEnable() function returns 0x") + QString::number(result, 16).toUpper());
            return;
        }

    }
    if(!ui->ssBetweenFramesCheckBox->isChecked())
    {
        DLN_RESULT result = DlnSpiMasterSSBetweenFramesDisable(_handle, getPort());
        if (DLN_FAILED(result))
        {
            QMessageBox::warning(this, tr("DlnSpiMasterSSBetweenFramesDisable() failed"),
                                       tr("DlnSpiMasterSSBetweenFramesDisable() function returns 0x") + QString::number(result, 16).toUpper());
            return;
        }
    }
}

void Dialog::getSSBetweenFrames()
{
    uint8_t ssBetweenFramesEnabled;
    DLN_RESULT result = DlnSpiMasterSSBetweenFramesIsEnabled(_handle, getPort(), &ssBetweenFramesEnabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiMasterSSBetweenFramesIsEnabled() failed"),
                            tr("DlnSpiMasterSSBetweenFramesIsEnabled() function returns 0x") + QString::number(result, 16).toUpper());
       return;
    }
    if(ssBetweenFramesEnabled == DLN_SPI_MASTER_SS_BETWEEN_FRAMES_ENABLED)
    {
       ui->ssBetweenFramesCheckBox->setChecked(true);
       return;
    }
    if(ssBetweenFramesEnabled == DLN_SPI_MASTER_SS_BETWEEN_FRAMES_DISABLED)
    {
       ui->ssBetweenFramesCheckBox->setChecked(false);
       return;
    }
}

void Dialog::getConfiguration()
{
    initSS();
    spiMasterIsEnabled();
    getFrequency();
    getDelayBetweenSS();
    getSpiMasterMode();
    getDelayAfterSS();
    getFrameSize();
    getDelayBetweenFrames();
    getSSPin();
    isSSEnabled();
}

bool Dialog::spiMasterIsEnabled()
{
    uint8_t enabled;
    DLN_RESULT result = DlnSpiMasterIsEnabled(_handle, getPort(), &enabled);
    if (DLN_FAILED(result))
    {
       QMessageBox::warning(this, tr("DlnSpiMasterIsEnabled() failed"),
                            tr("DlnSpiMasterIsEnabled() function returns 0x")+ QString::number(result, 16).toUpper());
       return false;
    }
    if(enabled == DLN_SPI_MASTER_ENABLED)
    {
       ui->enabledCheckBox->setChecked(true);
       return true;
    }
    if(enabled == DLN_SPI_MASTER_DISABLED)
    {
       ui->enabledCheckBox->setChecked(false);
       return false;
    }

    return false;
}

void Dialog::spiMasterPortConfig()
{
    uint16_t conflict;
    if(ui->enabledCheckBox->isChecked())
    {
        DLN_RESULT result = DlnSpiMasterEnable(_handle, getPort(), &conflict);
        initSS();
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterEnable() failed"),
                                tr("DlnSpiMasterEnable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
    if(!ui->enabledCheckBox->isChecked())
    {
        DLN_RESULT result = DlnSpiMasterDisable(_handle, getPort(), 0);
        initSS();
        if (DLN_FAILED(result))
        {
           QMessageBox::warning(this, tr("DlnSpiMasterDisable() failed"),
                                tr("DlnSpiMasterDisable() function returns 0x")+ QString::number(result, 16).toUpper());
           return;
        }
    }
}

void Dialog::readWrite()
{

    // to simplify the demo application we don't check input data for validity
    // invalid characters are skipped, enabling the decoding process to continue with subsequent characters.
    QByteArray writeData = QByteArray::fromHex(ui->writeData->toPlainText().toAscii());

    uint8_t frameSize;
    DlnSpiMasterGetFrameSize(_handle, getPort(), &frameSize);

    if(frameSize > 8)
    {
        QByteArray invertedData;
        int j = writeData.size()-1;
        for(int i = 0; i < writeData.size(); i++)
            invertedData[i] = writeData[j--];
        writeData = invertedData;
    }

    if (writeData.size() > 256)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("This application doesn't support writting of more than 256 bytes."));
        return;
    }
    if (writeData.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }

    QByteArray readData(writeData.size(), 0);


    DLN_RESULT result = DlnSpiMasterReadWrite(_handle, getPort(), writeData.size(),
                                              (uint8_t*)writeData.data(), (uint8_t*)readData.data());

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterReadWrite() failed"),
                             tr("DlnSpiMasterReadWrite() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->readData->setPlainText(readData.toHex());
}

void Dialog::read()
{
    QByteArray readData(ui->readSize->text().toInt(), 0);

    DLN_RESULT result = DlnSpiMasterRead(_handle, getPort(), readData.size(), (uint8_t*)readData.data());

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterRead() failed"),
                             tr("DlnSpiMasterRead() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
    ui->readData->setPlainText(readData.toHex());
}

void Dialog::write()
{
    QByteArray writeData = QByteArray::fromHex(ui->writeData->toPlainText().toAscii());

    uint8_t frameSize;
    DlnSpiMasterGetFrameSize(_handle, getPort(), &frameSize);

    if(frameSize > 8)
    {
        QByteArray invertedData;
        int j = writeData.size()-1;
        for(int i = 0; i < writeData.size(); i++)
            invertedData[i] = writeData[j--];
        writeData = invertedData;
    }

    if (writeData.size() > 256)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("This application doesn't support writting of more than 256 bytes."));
        return;
    }

    if (writeData.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }

    DLN_RESULT result = DlnSpiMasterWrite(_handle, getPort(), writeData.size(), (uint8_t*)writeData.data());

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterWrite() failed"),
                             tr("DlnSpiMasterWrite() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::readWriteEx()
{
    // to simplify the demo application we don't check input data for validity
    // invalid characters are skipped, enabling the decoding process to continue with subsequent characters.
    QByteArray writeData = QByteArray::fromHex(ui->writeData->toPlainText().toAscii());

    uint8_t frameSize;
    DlnSpiMasterGetFrameSize(_handle, getPort(), &frameSize);

    if(frameSize > 8)
    {
        QByteArray invertedData;
        int j = writeData.size()-1;
        for(int i = 0; i < writeData.size(); i++)
            invertedData[i] = writeData[j--];
        writeData = invertedData;
    }

    if (writeData.size() > 256)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("This application doesn't support writting of more than 256 bytes."));
        return;
    }
    if (writeData.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }


    uint8_t attribute = 0;
    if (ui->leaveSSlow->checkState()) attribute |= DLN_SPI_MASTER_ATTR_LEAVE_SS_LOW;

    QByteArray readData(writeData.size(), 0);
    DLN_RESULT result = DlnSpiMasterReadWriteEx(_handle, getPort(), writeData.size(),
                                         (uint8_t*)writeData.data(), (uint8_t*)readData.data(), attribute);

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterReadWriteEx() failed"),
                                 tr("DlnSpiMasterReadWriteEx() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

    ui->readData->setPlainText(readData.toHex());
}

void Dialog::readEx()
{
    uint8_t attribute = 0;
    if (ui->leaveSSlow->checkState()) attribute |= DLN_SPI_MASTER_ATTR_LEAVE_SS_LOW;

    QByteArray readData(ui->readSize->text().toInt(), 0);

    DLN_RESULT result = DlnSpiMasterReadEx(_handle, getPort(), readData.size(),
                                             (uint8_t*)readData.data(), attribute);

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterReadEx() failed"),
                             tr("DlnSpiMasterReadEx() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }

}

void Dialog::writeEx()
{
    QByteArray writeData = QByteArray::fromHex(ui->writeData->toPlainText().toAscii());

    uint8_t frameSize;
    DlnSpiMasterGetFrameSize(_handle, getPort(), &frameSize);

    if(frameSize > 8)
    {
        QByteArray invertedData;
        int j = writeData.size()-1;
        for(int i = 0; i < writeData.size(); i++)
            invertedData[i] = writeData[j--];
        writeData = invertedData;
    }

    if (writeData.size() > 256)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("This application doesn't support writting of more than 256 bytes."));
        return;
    }
    if (writeData.size() == 0)
    {
        QMessageBox::warning(this, tr("Invalid write data"),
                             tr("Please provide data to write."));
        return;
    }

    uint8_t attribute = 0;
    if (ui->leaveSSlow->checkState()) attribute |= DLN_SPI_MASTER_ATTR_LEAVE_SS_LOW;

    DLN_RESULT result = DlnSpiMasterWriteEx(_handle, getPort(), writeData.size(),
                                             (uint8_t*)writeData.data(), attribute);

    if (DLN_FAILED(result))
    {
        QMessageBox::warning(this, tr("DlnSpiMasterWriteEx() failed"),
                             tr("DlnSpiMasterWriteEx() function returns 0x") + QString::number(result, 16).toUpper());
        return;
    }
}

void Dialog::enableControls(bool enable)
{
    ui->cphaComboBox->setEnabled(enable);
    ui->cpolComboBox->setEnabled(enable);
    ui->delayAfterSSLineEdit->setEnabled(enable);
    ui->delayBetweenFramesLineEdit->setEnabled(enable);
    ui->delayBetweenSSLineEdit->setEnabled(enable);
    ui->enabledCheckBox->setEnabled(enable);
    ui->frameSizeComboBox->setEnabled(enable);
    ui->frequencyLineEdit->setEnabled(enable);
    ui->getDelayAfterSSPushButton->setEnabled(enable);
    ui->getDelayBetweenFramesPushButton->setEnabled(enable);
    ui->getDelayBetweenSSPushButton->setEnabled(enable);
    ui->getFrameSizePushButton->setEnabled(enable);
    ui->getFrequencyPushButton->setEnabled(enable);
    ui->getModePushButton->setEnabled(enable);
    ui->getSSPinPushButton->setEnabled(enable);
    ui->ssBetweenFramesCheckBox->setEnabled(enable);
    ui->leaveSSlow->setEnabled(enable);
    ui->setDelayAfterSSPushButton->setEnabled(enable);
    ui->setDelayBetweenFramesPushButton->setEnabled(enable);
    ui->setFrameSizePushButton->setEnabled(enable);
    ui->setFrequencyPushButton->setEnabled(enable);
    ui->setModePushButton->setEnabled(enable);
    ui->setSSPinPushButton->setEnabled(enable);
    ui->setDelayBetweenSSPushButton->setEnabled(enable);
    ui->readButton->setEnabled(enable);
    ui->writeButton->setEnabled(enable);
    ui->readWriteButton->setEnabled(enable);
    ui->writeExButton->setEnabled(enable);
    ui->readExButton->setEnabled(enable);
    ui->readWriteExButton->setEnabled(enable);
    ui->readSize->setEnabled(enable);

    ui->port->setEnabled(enable);
    if (enable)
    {
        connect(ui->port, SIGNAL(currentIndexChanged(int)), SLOT(getConfiguration()));
    }
    else
    {
        disconnect(ui->port, SIGNAL(currentIndexChanged(int)), this, SLOT(getConfiguration()));
    }
}
