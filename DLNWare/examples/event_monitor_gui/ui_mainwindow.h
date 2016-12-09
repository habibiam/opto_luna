/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 4.8.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QLocale>
#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QTableWidget>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionClear;
    QAction *actionAutoscroll;
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QTableWidget *eventList;
    QMenuBar *menuBar;
    QToolBar *toolBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(833, 402);
        MainWindow->setLocale(QLocale(QLocale::English, QLocale::UnitedStates));
        actionClear = new QAction(MainWindow);
        actionClear->setObjectName(QString::fromUtf8("actionClear"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/new/prefix1/images/clear.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionClear->setIcon(icon);
        actionAutoscroll = new QAction(MainWindow);
        actionAutoscroll->setObjectName(QString::fromUtf8("actionAutoscroll"));
        actionAutoscroll->setCheckable(true);
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/new/prefix1/images/autoscroll.png"), QSize(), QIcon::Selected, QIcon::On);
        actionAutoscroll->setIcon(icon1);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        eventList = new QTableWidget(centralWidget);
        if (eventList->columnCount() < 5)
            eventList->setColumnCount(5);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        eventList->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        eventList->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        eventList->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        eventList->setHorizontalHeaderItem(3, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        eventList->setHorizontalHeaderItem(4, __qtablewidgetitem4);
        eventList->setObjectName(QString::fromUtf8("eventList"));
        eventList->setEnabled(true);
        eventList->setFocusPolicy(Qt::NoFocus);
        eventList->setEditTriggers(QAbstractItemView::NoEditTriggers);
        eventList->setAlternatingRowColors(true);
        eventList->setSelectionMode(QAbstractItemView::NoSelection);
        eventList->setSelectionBehavior(QAbstractItemView::SelectRows);
        eventList->horizontalHeader()->setVisible(false);
        eventList->horizontalHeader()->setStretchLastSection(true);
        eventList->verticalHeader()->setStretchLastSection(false);

        gridLayout->addWidget(eventList, 0, 0, 1, 1);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 833, 21));
        MainWindow->setMenuBar(menuBar);
        toolBar = new QToolBar(MainWindow);
        toolBar->setObjectName(QString::fromUtf8("toolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, toolBar);

        toolBar->addAction(actionClear);
        toolBar->addAction(actionAutoscroll);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Event Monitor GUI", 0, QApplication::UnicodeUTF8));
        actionClear->setText(QApplication::translate("MainWindow", "Clear", 0, QApplication::UnicodeUTF8));
#ifndef QT_NO_TOOLTIP
        actionClear->setToolTip(QApplication::translate("MainWindow", "Clear the events log", 0, QApplication::UnicodeUTF8));
#endif // QT_NO_TOOLTIP
        actionAutoscroll->setText(QApplication::translate("MainWindow", "Autoscroll", 0, QApplication::UnicodeUTF8));
#ifndef QT_NO_TOOLTIP
        actionAutoscroll->setToolTip(QApplication::translate("MainWindow", "Scroll the events log when a new event arrives", 0, QApplication::UnicodeUTF8));
#endif // QT_NO_TOOLTIP
        QTableWidgetItem *___qtablewidgetitem = eventList->horizontalHeaderItem(0);
        ___qtablewidgetitem->setText(QApplication::translate("MainWindow", "SN", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem1 = eventList->horizontalHeaderItem(1);
        ___qtablewidgetitem1->setText(QApplication::translate("MainWindow", "ID", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem2 = eventList->horizontalHeaderItem(2);
        ___qtablewidgetitem2->setText(QApplication::translate("MainWindow", "Module", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem3 = eventList->horizontalHeaderItem(3);
        ___qtablewidgetitem3->setText(QApplication::translate("MainWindow", "Event", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem4 = eventList->horizontalHeaderItem(4);
        ___qtablewidgetitem4->setText(QApplication::translate("MainWindow", "Data", 0, QApplication::UnicodeUTF8));
        toolBar->setWindowTitle(QApplication::translate("MainWindow", "toolBar", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
