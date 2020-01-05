#include "gamearea.hh"

GameArea::GameArea(QObject* parent):
    QGraphicsScene(parent)
{
    // Setting scene size.
    setSceneRect(0, 0,
                 SCENE_WIDTH,
                 SCENE_HEIGHT);

    // Peg colors.
    QColor left_peg_color(255, 51, 51);
    QColor center_peg_color(51, 255, 51);
    QColor right_peg_color(51, 51, 255);

    // Peg brushes
    QBrush left_peg_brush(left_peg_color);
    QBrush center_peg_brush(center_peg_color);
    QBrush right_peg_brush(right_peg_color);

    // Peg pens
    QPen left_peg_pen(left_peg_color);
    QPen center_peg_pen(center_peg_color);
    QPen right_peg_pen(right_peg_color);


    // Drawing pegs.

    // Left peg
    addRect(LEFT_PEG_X,
            SCENE_HEIGHT - PEG_HEIGHT - 1,
            PEG_WIDTH, PEG_HEIGHT, left_peg_pen, left_peg_brush);

    // Center peg
    addRect(CENTER_PEG_X,
            SCENE_HEIGHT - PEG_HEIGHT - 1,
            PEG_WIDTH, PEG_HEIGHT, center_peg_pen, center_peg_brush);

    // Right peg
    addRect(RIGHT_PEG_X,
            SCENE_HEIGHT - PEG_HEIGHT - 1,
            PEG_WIDTH, PEG_HEIGHT, right_peg_pen, right_peg_brush);

}

void GameArea::draw_disk(Disk* disk_to_be_drawn)
{
    // At first, the disk is at scene position (0,0) so it has to be moved to
    // its decided coordinates.
    move_disk_on_scene(disk_to_be_drawn);
    // Showing the disk on scene.
    addItem(disk_to_be_drawn);
}

void GameArea::move_disk_on_scene(Disk* disk_ptr)
{

    int x_coordinate = peg_to_x(disk_ptr->get_peg(),
                                disk_ptr->get_width());

    int y_coordinate = position_to_y(disk_ptr->get_position(),
                                     disk_ptr->get_height());

    disk_ptr->setPos(x_coordinate, y_coordinate);
}

int GameArea::peg_to_x(int peg, int disk_width)
{
    int peg_coordinate;

    // Selecting right peg's coordinates.
    if ( peg == 0 ) {
        peg_coordinate = LEFT_PEG_X;

    } else if ( peg == 1 ) {
        peg_coordinate = CENTER_PEG_X;

    } else {
        peg_coordinate = RIGHT_PEG_X;
    }

    // Making the actual starting coordinate so that the disk will be in the
    // center of the peg.
    return peg_coordinate - disk_width/2 + 1;
}

int GameArea::position_to_y(int disk_position, int disk_height)
{
    return SCENE_HEIGHT - (1 + disk_position) * disk_height - 1;
}
