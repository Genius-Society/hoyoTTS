#pragma once
//#include "HostNetlib.h" 

class Thread_Disconnect : public QThread
{
	Q_OBJECT

protected:

	void run(void);

public:
	Thread_Disconnect(QString);
	~Thread_Disconnect();

signals:

	void FailedList_Dis(int);
	void dSuccess(void);

private: 
	const char *QStrToChar(QString str);
	
	void stopHost(QString); 
	void unshareHost(void);

	HostNetlib hf;
	Sharing sf;

	QString KEY;

};

