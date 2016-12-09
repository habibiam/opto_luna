#include "connectdialog.h"
#include "ui_connectdialog.h"
#include "../common/dln_generic.h"

ConnectDialog::ConnectDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ConnectDialog)
{
    ui->setupUi(this);
    ui->port->setValidator(new QIntValidator(0, 0xFFFF, this));
    ui->host->setText(tr("localhost"));
    ui->port->setText(QString::number(DLN_DEFAULT_SERVER_PORT));
}

ConnectDialog::~ConnectDialog()
{
    delete ui;
}

void ConnectDialog::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}

QString ConnectDialog::host()
{
    return ui->host->text();
}

QString ConnectDialog::port()
{
    return ui->port->text();
}

