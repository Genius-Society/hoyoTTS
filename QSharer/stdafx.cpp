#include "stdafx.h"
 

// const char *QStrToChar(QString str)
// {   
// 	QByteArray ba = str.toLatin1(); 
// 	char *chStr = (char *)malloc(ba.length() + 1);

// 	memset(chStr, 0, ba.length());
// 	memcpy(chStr, ba.data(), ba.length());
// 	chStr[ba.length()] = '\0';

// 	return chStr;
// }

// bool isFormatStr(const char *s)
// {
// 	bool b = true;

// 	while (*s)
// 	{
// 		if (!((*s >= 'A' && *s <= 'Z') || (*s >= 'a' && *s <= 'z') || (*s >= '0' && *s <= '9')))
// 		{
// 			b = false;
// 			break;
// 		} 
// 		s++;
// 	}

// 	return b;
// }

// bool isKEYLength(const char *s)
// {
// 	QString qs = QObject::tr(s); 
// 	int length = qs.length();

// 	return length >= 8 && length <= 13;
// }

// bool isSSIDLength(const char *s)
// {
// 	QString qs = QObject::tr(s);
// 	int length = qs.length();

// 	return length >= 1 && length <= 13;
// }

// BYTE bit(int p)
// {
// 	switch (p)
// 	{
// 	case 1:  return 0x01; break;
// 	case 2:  return 0x02; break;
// 	case 3:  return 0x04; break;
// 	case 4:  return 0x08; break;
// 	case 5:  return 0x10; break;
// 	case 6:  return 0x20; break;
// 	case 7:  return 0x40; break;
// 	case 8:  return 0x80; break;
// 	default: return 0x00; break;
// 	}

// }