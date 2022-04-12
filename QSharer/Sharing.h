#pragma once
#include <QtWidgets>

class Sharing
{
public:
	Sharing();
	~Sharing();

	int StartSharing(void);
	int StopSharing(void); 

private:

	bool isDest(QString, int);
	bool isSource(QString, int);
	
	BYTE bit(int);
	void InitCon(void);
	void ExitCon(void);

};

