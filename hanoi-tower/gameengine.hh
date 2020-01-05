/* Module: GameEngine
 * ---------------
 *
 * Creates, stores and moves disks on given GameArea (QGraphicsScene). Is
 * also used to check when game is over and what moves are currently illegal.
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
#ifndef GAMEENGINE_HH
#define GAMEENGINE_HH

#include "gamearea.hh"

#include <QObject>
#include <vector>

class GameEngine : public QObject
{
    Q_OBJECT

public:

    explicit GameEngine(GameArea& game_area, QObject *parent = nullptr);

    // Creates all of the disks and draws them on the left peg.
    void initialize(int disk_amount);

    // Moves a disk from given peg to destination peg.
    void move_disk(int from_peg, int to_peg);

    // Returns every illegal move with current disk positions.
    std::vector <std::pair <int,int> > get_illegal_moves();

    // Checks if all of the disks are in the last peg.
    bool is_game_over();

    // Removes all disks from GameArea (scene) and local vector.
    void empty_area();

    // Returns random RGB color.
    QColor random_color();

private:

    // Used to calculate initial disk properties from global constans.
    std::vector<int> get_disk_properties(int disk_amount);

    // Checks if given peg is empty.
    bool is_peg_empty(int peg);

    // Adds given illegal move to given vector if the vector doesn't allready
    // have the move.
    void add_to_vector(std::vector<std::pair<int,int> >& vector, std::pair<int,int> move);

    // The area where all pegs and disks will be drawn.
    GameArea& game_area_;
    // Contains 3 vectors that each represent a peg and each of those vectors
    // contain the disks that are in the peg.
    std::vector< std::vector<Disk*> > disks_;

};

#endif // GAMEENGINE_HH
