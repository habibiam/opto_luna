#include "ledstatecombo.h"

LedStateCombo::LedStateCombo(uint8_t ledNumber, DLN_LED_STATE currentState)
    : QComboBox(0), _ledNumber(ledNumber)
{
    setInsertPolicy(QComboBox::NoInsert);
    addItem(tr("DLN_LED_STATE_OFF"), DLN_LED_STATE_OFF);
    addItem(tr("DLN_LED_STATE_ON"), DLN_LED_STATE_ON);
    addItem(tr("DLN_LED_STATE_SLOW_BLINK"), DLN_LED_STATE_SLOW_BLINK);
    addItem(tr("DLN_LED_STATE_FAST_BLINK"), DLN_LED_STATE_FAST_BLINK);
    addItem(tr("DLN_LED_STATE_DOUBLE_BLINK"), DLN_LED_STATE_DOUBLE_BLINK);
    addItem(tr("DLN_LED_STATE_TRIPLE_BLINK"), DLN_LED_STATE_TRIPLE_BLINK);
    setCurrentIndex(currentState);
    connect(this, SIGNAL(currentIndexChanged(int)), SLOT(selectionChanged(int)));
}

void LedStateCombo::selectionChanged(int index)
{
    emit ledStateChanged(_ledNumber, DLN_LED_STATE(index));
}

