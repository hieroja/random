/* Main.cpp
 * ---------------
 *
 * Creates GameArea, GameEngine and MainWindow.
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
#include "mainwindow.hh"
#include "gameengine.hh"
#include "gamearea.hh"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    GameArea graphical_game_area;
    GameEngine engine(graphical_game_area);

    MainWindow w(engine, graphical_game_area);

    w.show();

    return a.exec();
}
