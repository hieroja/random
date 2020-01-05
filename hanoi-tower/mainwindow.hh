/* Module: MainWindow
 * ---------------
 *
 * Used to handle button- and keyboard presses. Handles button states and all
 * UI related widgets. Uses GameEngine's methods to make changes to GameArea
 * that includes all disks involved.
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
#ifndef MAINWINDOW_HH
#define MAINWINDOW_HH

#include <gameengine.hh>

#include <QMainWindow>
#include <QButtonGroup>
#include <QTimer>
#include <QTime>
#include <QKeyEvent>
#include <map>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

    explicit MainWindow(GameEngine& engine, GameArea &scene,
                        QWidget* parent = nullptr);

    ~MainWindow();

private slots:

    // Moving the disk with keyboard.
    void keyPressEvent(QKeyEvent* event);

    // Updates the time show on the right upper corner of the window every 1ms.
    void update_timer();

    // Initializes the game. Sets all initial settings and starts timer.
    void start_button_pressed();

    // Updates private variables from_peg_ and to_peg_. Also updates button
    // states accordingly.
    void peg_setting_changed();

    // Calls for GameEngine to move disks, checks if game is over, updates
    // illegal moves and button states.
    void move_button_pressed();

private:

    // Returns elapsed time as string.
    QString get_time_elapsed();

    // Compares current selected move to known illegal moves and returns true
    // if current move is illegal.
    bool current_move_is_illegal();

    // Sets all illegal move buttons to disabled.
    void update_button_states();

    // Checks if game is over and initializes needed methods if it is.
    void if_game_over();

    // Adds current move to move history and shows it in move history widget.
    void update_move_history();

    // Adds the time to highscores if it is smaller than last best and returns
    // true, else returns false.
    bool is_new_record(int amount_of_disks, QString time);

    // Returns tailored message containing wheater the user made new record or not.
    QString get_game_ending_message();

    Ui::MainWindow *ui_;
    GameEngine& engine_;

    QTime* time_; // Used to show time passed.
    QTimer* timer_; // Used to send signal everytime 1ms has passed.

    // Virtual groups for moving buttons.
    QButtonGroup from_button_group_;
    QButtonGroup to_button_group_;

    // Currently selected pegs.
    int from_peg_;
    int to_peg_;

    // Illegal moves marked as from what peg to what peg for example {1,2}
    // would be a move from middle peg to right peg.
    std::vector <std::pair <int,int> > illegal_moves_;

    // Keeps tracks of made moves amount.
    int moves_made_;

    // Calculated as 2^n - 1, where n is amount of disks.
    long long int minimum_amount_of_moves_;

    // Lowest time for each number of disks.
    std::map<int, QString> highscores_;

};

#endif // MAINWINDOW_HH
