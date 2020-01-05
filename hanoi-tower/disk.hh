/* Module: Disk
 * ---------------
 *
 * Represents one disk on GameArea. Holds information about disk's position,
 * size and color.
 *
 * ---------------
 *
 * Author: Jere Liimatainen
 * Email:jere.liimatainen@tuni.fi
 * Student number: 285309
 *
 * ---------------
 * TIE-0220x S2019
 * */
#ifndef DISK_HH
#define DISK_HH

#include <QWidget>
#include<QGraphicsItem>
#include <QPainter>

class Disk : public QGraphicsItem
{

public:

    Disk(int peg, int position,
         int width, int height, QColor initial_color);

    // Used to Create graphical representation.
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget = nullptr) override;

    // Necessary method for QGraphicsItem, also defines the graphics of the disk.
    // Returns rectangele that surrounds the object.
    QRectF boundingRect() const override;

    // Changes disk's position to given position.
    void change_disk_location(int peg, int position);

    void change_color(QColor new_color);

    // Self explaing get functions.
    int get_peg() const;
    int get_position() const;
    int get_width() const;
    int get_height() const;

private:

    int peg_; // The peg the disk is located in. 0, 1 or 3.
    int position_; // Position in given peg starting from 0.
    int width_;
    int height_;
    QColor color_;

};

#endif // DISK_HH
