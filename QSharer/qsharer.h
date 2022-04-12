#ifndef QSHARER_H
#define QSHARER_H
#pragma once
#include <QtWidgets>
#include "HostNetlib.h" 
#include "oui.h"


class QSharer : public QMainWindow
{
	Q_OBJECT

public:
	QSharer(QWidget *parent = 0);
	~QSharer();

	QWidget *centralWidget;
	QTabWidget *tabWidget;
	QWidget *HotspotTab;
	QLineEdit *WifiNameEdit;
	QLabel *ClientLabel;
	QLabel *PassLabel;
	QPushButton *CreateButton;
	QLabel *ClientNumLabel;
	QLabel *WifiNameLabel;
	QLineEdit *PassEdit;
	QPushButton *DisconnectButton;
	QCheckBox *HideCheck;
	QWidget *DeviceTab;
	QTableView *listView;

	QTimer *Monitor;

private:
	//Ui::QSharerClass ui;

	HostNetlib hf;
	oui ouf;

	void setupUi(QMainWindow *);
	void retranslateUi(QMainWindow *);
	void customizeUi(QMainWindow *);

public slots: 

    void createStart(void);
	void createFailed(int);
	void createFinished(int); 

	void discStart(void);
	void discFailed(int);
	void discFinished(void);

	void HidePass(bool);

	void UpdClients(QStringList);
	void PassMinLength(QString);

};

#endif // QSHARER_H
