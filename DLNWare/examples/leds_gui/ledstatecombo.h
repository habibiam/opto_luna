#ifndef LEDSTATECOMBO_H
#define LEDSTATECOMBO_H

#include <QComboBox>
#include "../common/dln_led.h"

class LedStateCombo : public QComboBox
{
    Q_OBJECT
public:
    LedStateCombo(uint8_t ledNumber, DLN_LED_STATE currentState);

signals:
    void ledStateChanged(uint8_t ledNumber, DLN_LED_STATE newState);

private slots:
    void selectionChanged(int index);
private:
    uint8_t _ledNumber;

};

#endif // LEDSTATECOMBO_H
