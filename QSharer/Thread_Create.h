#pragma once
//#include "HostNetlib.h" 

class Thread_Create : public QThread
{
	Q_OBJECT

public:
	Thread_Create(QString, QString);
	~Thread_Create();

signals:
	void FailedList_Create(int);
	void cSuccess(int);

protected:

	void run(void);

private: 
	const char *QStrToChar(QString str);
	
	void initHost(void);
	void stopPrevHost(void);
	void setHost(QString, QString);
	void startHost(void);
	void unsharePrevHost(void);
	void shareHost(void);

	HostNetlib hf;
	Sharing sf;

	QString SSID;
	QString KEY; 

};

