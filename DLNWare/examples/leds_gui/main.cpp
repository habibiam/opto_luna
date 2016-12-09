#include <QtGui/QApplication>
#include <QMessageBox>
#include "mainwindow.h"
#include "../common/dln_generic.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    HDLN handle = HDLN_INVALID_HANDLE;
    DLN_RESULT result = DlnConnect("localhost", DLN_DEFAULT_SERVER_PORT);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, QObject::tr("DLN Server Connection Error"),
                             QObject::tr("Failed to connect to local DLN server."));
        return -1;
    }

    result = DlnOpenDevice(0, &handle);
    if (!DLN_SUCCEEDED(result))
    {
        QMessageBox::warning(NULL, QObject::tr("DLN adapter openning error"),
                             QObject::tr("Failed to open DLN adapter. Please check connection."));
        DlnDisconnectAll();
        return -2;
    }
    MainWindow w(handle);
    w.show();
    int exitCode = a.exec();
    DlnCloseAllHandles();
    DlnDisconnectAll();
    return exitCode;
}
