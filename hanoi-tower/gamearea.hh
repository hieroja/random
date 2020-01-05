/* Module: GameArea
 * ---------------
 *
 * Acts as MainWindows graphicscene. Is used to add, draw, move and remove given
 * disks.
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
#ifndef GAMEAREA_HH
#define GAMEAREA_HH

#include "disk.hh"
#include <QGraphicsScene>

// Scene dimensions are made 4 pixels smaller than graphicsview so that everything
// fits without needing to use scroll bars.
const int SCENE_WIDTH = 620 - 4;
const int SCENE_HEIGHT = 290 - 4;

// Peg sizes.
const int PEG_WIDTH = 2;
const int PEG_HEIGHT = 283;

// Each peg's drawing x-coordinate.
const int LEFT_PEG_X = SCENE_WIDTH/5 - (PEG_WIDTH + 2)/2;
const int CENTER_PEG_X = SCENE_WIDTH/2 - (PEG_WIDTH + 2)/2;
const int RIGHT_PEG_X = SCENE_WIDTH - SCENE_WIDTH/5 - (PEG_WIDTH + 2)/2;

// Disk size limits and standard values.
const int STANDARD_BIGGEST_DISK_WIDTH = 80;
const int STANDARD_DISK_HEIGHT = 20;
const int STANDARD_DISK_SIZE_DIFFERENCE = 2*5;

// Maximum disk width is calculated so that in the extreme case where minimum
// size difference is only 2 (1 pixel per side) there is at least 20 pixels
// between the biggest and second biggest disk.
const int MAXIMUM_DISK_WIDTH = ((CENTER_PEG_X - LEFT_PEG_X)/2 - 20) * 2;

const int MINIMUM_DISK_HEIGHT = 4;

// Minimum disk width is calculated so that the smallest disk is still 2 pixels
// wider than the peg.
const int MINIMUM_DISK_WIDTH = PEG_WIDTH + 2;


class GameArea : public QGraphicsScene
{

public:

    GameArea(QObject* parent = nullptr);

    // Draws given disk on scene.
    void draw_disk(Disk* disk_to_be_drawn);

    // Updates given disk's position on scene.
    void move_disk_on_scene(Disk* disk_ptr);

private:

    // Convers peg number into x-coordinate.
    int peg_to_x(int peg, int disk_width);

    // Converts disk's height position into x-coordinate.
    int position_to_y(int disk_position, int disk_height);

};

#endif // GAMEAREA_HH
