#pragma once
#include <QtWidgets>

class Sharing
{
public:
	Sharing(); // QString);
	~Sharing();
	QStringList LoadSrc(void);
	int StartSharing(QString);
	int StopSharing(void);

private:
	bool isDest(QString, int);
	bool isSource(QString, int);
	BYTE bit(int);
	void InitCon(void);
	void ExitCon(void);
};
