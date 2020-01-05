#include "disk.hh"

Disk::Disk(int peg, int position,
           int width, int height, QColor initial_color):
    peg_(peg),
    position_(position),
    width_(width),
    height_(height),
    color_(initial_color)
{}

void Disk::paint(QPainter* painter, const QStyleOptionGraphicsItem* option,
                 QWidget* widget)
{

    QRectF rect = boundingRect();
    QBrush brush(color_);

    // Creating graphics.
    painter->fillRect(rect, brush);
    painter->drawRect(rect);

    // These has to be used.
    if ( option || widget ) {}
}

QRectF Disk::boundingRect() const
{
    return QRectF(0,0, width_, height_);
}

void Disk::change_disk_location(int peg, int position)
{
    peg_ = peg;
    position_ = position;
}

void Disk::change_color(QColor new_color)
{
    color_ = new_color;
}

int Disk::get_peg() const
{
    return peg_;
}

int Disk::get_position() const
{
    return position_;
}

int Disk::get_width() const
{
    return width_;
}

int Disk::get_height() const
{
    return height_;
}
