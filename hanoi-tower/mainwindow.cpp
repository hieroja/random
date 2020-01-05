#include "mainwindow.hh"
#include "ui_mainwindow.h"

#include <QMessageBox>
#include <math.h>

MainWindow::MainWindow(GameEngine& engine, GameArea& scene, QWidget *parent):
    QMainWindow(parent),
    ui_(new Ui::MainWindow),
    engine_(engine),
    time_(new QTime),
    timer_(new QTimer),
    moves_made_(0)
{
    // Initial scne setting and maximum amount of disks settings.
    ui_->setupUi(this);
    ui_->graphicsView->setScene(&scene);

    // Absolute max amount is desided by the smaller maximum amout desided by
    // width or height.
    const int absolute_max_amount_of_disks =
            std::min(PEG_HEIGHT/MINIMUM_DISK_HEIGHT,
                     (MAXIMUM_DISK_WIDTH-MINIMUM_DISK_WIDTH)/2);

    ui_->spinBoxDiskAmount->setRange(1, absolute_max_amount_of_disks);

    QString disk_amount_text = "Amount of disks (max " +
                               QString::number(absolute_max_amount_of_disks) + ")";
    ui_->labelDiskAmount->setText(disk_amount_text);

    // Adding all from- and to pegs to groups.
    from_button_group_.addButton(ui_->fromLeftPeg, 0);
    from_button_group_.addButton(ui_->fromCenterPeg, 1);
    from_button_group_.addButton(ui_->fromRightPeg, 2);
    from_button_group_.setExclusive(true);

    to_button_group_.addButton(ui_->toLeftPeg, 0);
    to_button_group_.addButton(ui_->toCenterPeg, 1);
    to_button_group_.addButton(ui_->toRightPeg, 2);
    to_button_group_.setExclusive(true);

    // Signal-slot connections

    connect(timer_, SIGNAL(timeout()), this, SLOT(update_timer()));

    connect(ui_->pushButtonStart, &QPushButton::pressed,
            this, &MainWindow::start_button_pressed);
    connect(ui_->pushButtonMove, &QPushButton::pressed,
            this, &MainWindow::move_button_pressed);

    for ( int i = 0 ; i < 3 ; ++i ) {
        connect(from_button_group_.button(i), &QRadioButton::clicked,
                this, &MainWindow::peg_setting_changed);

        connect(to_button_group_.button(i), &QRadioButton::clicked,
                this, &MainWindow::peg_setting_changed);

    }

    // Disabling moving buttons before game is initialized.
    ui_->groupBoxFromPeg->setDisabled(true);
    ui_->groupBoxToPeg->setDisabled(true);
    ui_->pushButtonMove->setDisabled(true);


}

MainWindow::~MainWindow()
{

    delete ui_;
    ui_ = nullptr;

    delete time_;
    time_ = nullptr;

    delete timer_;
    timer_ = nullptr;

}

void MainWindow::keyPressEvent(QKeyEvent* event)
{
    if( event->key() == Qt::Key_Space && ui_->pushButtonMove->isEnabled()) {
        move_button_pressed();
        return;
    }

    if( event->key() == Qt::Key_1 && from_button_group_.button(0)->isEnabled()) {
        from_button_group_.button(0)->setChecked(true);
        peg_setting_changed();
        return;
    }

    if( event->key() == Qt::Key_2 && from_button_group_.button(1)->isEnabled()) {
        from_button_group_.button(1)->setChecked(true);
        peg_setting_changed();
        return;
    }

    if( event->key() == Qt::Key_3 && from_button_group_.button(2)->isEnabled()) {
        from_button_group_.button(2)->setChecked(true);
        peg_setting_changed();
        return;
    }

    if( event->key() == Qt::Key_8 && to_button_group_.button(0)->isEnabled()) {
        to_button_group_.button(0)->setChecked(true);
        peg_setting_changed();
        return;
    }

    if( event->key() == Qt::Key_9 && to_button_group_.button(1)->isEnabled()) {
        to_button_group_.button(1)->setChecked(true);
        peg_setting_changed();
        return;
    }

    if( event->key() == Qt::Key_0 && to_button_group_.button(2)->isEnabled()) {
        to_button_group_.button(2)->setChecked(true);
        peg_setting_changed();
    }


}

void MainWindow::update_timer()
{

    ui_->labelElapsedTime->setText(get_time_elapsed());

}

void MainWindow::start_button_pressed()
{
    // Calculating minimum moves.
    int amount_of_disks = ui_->spinBoxDiskAmount->value();
    minimum_amount_of_moves_ = static_cast<long long int>(pow(2, amount_of_disks) - 1);

    // Disabling initial start button so that the game has to be finished before
    // new one can beging.
    ui_->pushButtonStart->setDisabled(true);
    ui_->spinBoxDiskAmount->setDisabled(true);

    // Enabling moving buttons.
    ui_->groupBoxFromPeg->setDisabled(false);
    ui_->groupBoxToPeg->setDisabled(false);

    // First move can't to first peg since every disk is in the first peg.
    to_button_group_.button(0)->setDisabled(true);

    // Initializing game with given amount of disks and getting illegal moves.
    engine_.initialize(amount_of_disks);
    illegal_moves_ = engine_.get_illegal_moves();

    // Setting initial first move.
    from_button_group_.button(0)->setChecked(true);
    to_button_group_.button(1)->setChecked(true);
    from_peg_ = 0;
    to_peg_ = 1;

    // Enabling moveing.
    ui_->pushButtonMove->setDisabled(false);

    // Starting timer.
    time_->start();
    timer_->start();

}


void MainWindow::peg_setting_changed()
{
    from_peg_ = from_button_group_.checkedId();
    to_peg_ = to_button_group_.checkedId();
    update_button_states();
}

void MainWindow::move_button_pressed()
{
    engine_.move_disk(from_peg_, to_peg_);
    ++moves_made_;
    update_move_history();
    if_game_over();

    // Updating illegal move vector and button states because disk have been moved.
    illegal_moves_ = engine_.get_illegal_moves();

    update_button_states();

}

QString MainWindow::get_time_elapsed()
{

    int msecs = time_->elapsed() % 100;
    int secs = time_->elapsed() / 1000;
    int mins = (secs / 60) % 60;
    secs = secs % 60;

    // Formatting time.
    QString time_elapsed = (QString("%1:%2:%3")
                    .arg(mins, 2, 10, QLatin1Char('0'))
                    .arg(secs, 2, 10, QLatin1Char('0'))
                    .arg(msecs, 2, 10, QLatin1Char('0')) );

    return time_elapsed;

}

bool MainWindow::current_move_is_illegal()
{
    std::pair<int,int> current_move = {from_peg_, to_peg_};

    if ( std::find(illegal_moves_.begin(), illegal_moves_.end(), current_move)
         != illegal_moves_.end() ) {
        return true;

    } else {
        return false;
    }
}

void MainWindow::update_button_states()
{
    // As default every button is enabled.
    ui_->pushButtonMove->setDisabled(false);

    for ( int i = 0 ; i < 3 ; ++i ) {
        to_button_group_.button(i)->setDisabled(false);
    }

    // Going through illegal moves and disabling buttons accordingly.
    for ( std::pair<int,int> illegal_move : illegal_moves_ ) {
        if ( illegal_move.first == from_peg_ ) {

            to_button_group_.button(illegal_move.second)->setDisabled(true);
        }
    }

    // Finally if selected move is illegal, move button cannot be pressed.
    if ( current_move_is_illegal() ) {
        ui_->pushButtonMove->setDisabled(true);
    }
}

void MainWindow::if_game_over()
{
    if ( engine_.is_game_over() ) {

        timer_->stop();
        engine_.empty_area();

        QString game_ending_message = get_game_ending_message();

        int result = QMessageBox::question(this, "Game over!", game_ending_message,
                                       QMessageBox::Yes, QMessageBox::No);
        if ( result ==  QMessageBox::No) {
            close();

        } else {

            // Settings for new game.
            ui_->groupBoxFromPeg->setDisabled(true);
            ui_->groupBoxToPeg->setDisabled(true);
            ui_->pushButtonMove->setDisabled(true);
            ui_->labelElapsedTime->setText("00:00:00");
            ui_->pushButtonStart->setDisabled(false);
            ui_->spinBoxDiskAmount->setDisabled(false);
            ui_->spinBoxDiskAmount->setValue(1);
            ui_->listWidgetMoveHistory->clear();
            from_peg_ = 0;
            to_peg_ = 0;
            moves_made_ = 0;

        }

    }
}

void MainWindow::update_move_history()
{

    long long int moves_left_from_minimum = moves_made_ - minimum_amount_of_moves_;

    // Creating move nuber to include how many moves away from minimum amount of
    // moves it is. The number is show as - or + debending on if any moves are
    // left. Also if the number has more than 6 digits, a power of 10
    // approximation is shown.
    QString move_number = QString::number(moves_made_) + ". (";

    if ( moves_left_from_minimum < -999999 ) {
        // x is the power of 10.
        int x = static_cast<int>(log10 ((-1)*moves_left_from_minimum));
        move_number.append( "- >10^" + QString::number(x) + ")");

    } else if ( moves_left_from_minimum > 999999) {
        int x = static_cast<int>(log10 (moves_left_from_minimum));
        move_number.append( "+ >10^" + QString::number(x) + ")");

    } else if ( moves_left_from_minimum < 0 ) {
        move_number.append( QString::number(moves_left_from_minimum) + ")");

    } else if ( moves_left_from_minimum > 0 ) {
        move_number.append( "+" + QString::number(moves_left_from_minimum) + ")");

    } else {
        // 0 moves from minimumn has no - or +.
        move_number.append( "0)");
    }

    // Creating other aspects and final string.
    QString move_coordinates = "(" + QString::number(from_peg_) + ", " +
            QString::number(to_peg_) + ")";

    QString elapsed_time = get_time_elapsed();

    QString move_string = move_number + "    " + move_coordinates + "    " +
            elapsed_time;

    ui_->listWidgetMoveHistory->addItem(move_string);

    // Scrolling to bottom so that newest move shows.
    ui_->listWidgetMoveHistory->scrollToBottom();
}

bool MainWindow::is_new_record(int amount_of_disks, QString time)
{
    bool record_made = false;

    if ( highscores_.find(amount_of_disks) != highscores_.end() ) {
        if ( time < highscores_.at(amount_of_disks) ) {
            highscores_.at(amount_of_disks) = time;
            record_made = true;
        }
    } else {
        highscores_.insert( { amount_of_disks, time } );
        record_made = true;
    }

    return record_made;
}

QString MainWindow::get_game_ending_message()
{

    QString game_ending_message;

    int amount_of_disks = ui_->spinBoxDiskAmount->value();
    QString final_time = get_time_elapsed();
    bool new_record_made = is_new_record(amount_of_disks, final_time);

    if ( new_record_made ) {

        game_ending_message.append("New record time: " + final_time +
                                      "!\nTry aging?");
    } else {

        QString old_record = highscores_.at(amount_of_disks);
        QString disks_string = QString::number(amount_of_disks);

        game_ending_message.append("Record time for " + disks_string +
                                      " disk(s) is: " + old_record +
                                      "\nYour time was: " + final_time +
                                      "\nTry aging?");
    }

    return game_ending_message;

}
