#pragma once
#include <QtWidgets>
#include "HostNetlib.h" 


class Timer_Monitor : public QTimer
{

	Q_OBJECT

public:
	Timer_Monitor(int ms);
	~Timer_Monitor();

protected: 

	void timerEvent(QTimerEvent *);

private:

	QStringList getMacList(int);

	int cPeerNum = 0;
	int lPeerNum = 0;

	HostNetlib hf;

signals: 
 
	void UpdMacList(QStringList);
	void FailedList_Monitor(int);
	 
};

