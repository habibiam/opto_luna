#include <QtGui/QApplication>
#include <QMessageBox>
#include "mainwindow.h"
#include "../common/dln_generic.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    int exitCode = -1;
    DLN_RESULT result = DlnConnect("localhost", DLN_DEFAULT_SERVER_PORT);
    if (DLN_SUCCEEDED(result))
    {
        MainWindow w;
        w.show();
        exitCode = a.exec();
        DlnDisconnectAll();

    }
    else
    {
        QMessageBox::warning(NULL, QObject::tr("DLN Server Connection Error"),
                             QObject::tr("Failed to connect to local DLN server"));
    }
    return exitCode;
}
