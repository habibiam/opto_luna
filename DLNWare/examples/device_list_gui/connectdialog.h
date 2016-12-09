#ifndef CONNECTDIALOG_H
#define CONNECTDIALOG_H

#include <QDialog>

namespace Ui {
    class ConnectDialog;
}

class ConnectDialog : public QDialog {
    Q_OBJECT
public:
    ConnectDialog(QWidget *parent = 0);
    ~ConnectDialog();
    QString host();
    QString port();
signals:
    void connected();

protected:
    void changeEvent(QEvent *e);

private:
    Ui::ConnectDialog *ui;
};

#endif // CONNECTDIALOG_H
