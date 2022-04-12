#pragma once
#include <QStyledItemDelegate>

class QCommonDelegate : public QStyledItemDelegate
{

	Q_OBJECT

public:
	QCommonDelegate(QObject *parent);
	~QCommonDelegate();

private:

	void paint(QPainter *painter,
		const QStyleOptionViewItem &option, const QModelIndex &index) const;

};

