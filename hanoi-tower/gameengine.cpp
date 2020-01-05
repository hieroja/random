#include "gameengine.hh"

GameEngine::GameEngine(GameArea& game_area, QObject *parent):
  QObject (parent),
  game_area_(game_area)

{}

void GameEngine::initialize(int disk_amount)
{

    // Getting initial disk properties.
    std::vector<int> properties_vector = get_disk_properties(disk_amount);

    // Unpacking properties.
    int biggest_disk_width = properties_vector.at(0);
    int disk_height = properties_vector.at(1);
    int disk_width_difference = properties_vector.at(2);

    // First peg's disks will be stored here.
    std::vector<Disk*> disks_in_left_peg;

    // Creating initial disk objects and adding them to first peg.
    for ( int i = 0; i < disk_amount; ++i ) {

        // Initial pointer for the disk.
        Disk* new_disk = nullptr;

        // Random color at start.
        QColor initial_color = random_color();

        // Disk width debends on how many have been created before it, because
        // every disk has to be different size.
        int disk_width = biggest_disk_width - i*disk_width_difference;

        // At first, every disk will be at the left peg (index 0).
        int peg = 0;

        // Disk position tells how many disks are under it (have been created
        // before it).
        int position = i;

        new_disk = new Disk(peg,
                            position,
                            disk_width,
                            disk_height,
                            initial_color);

        disks_in_left_peg.push_back(new_disk);
    }

    disks_.push_back(disks_in_left_peg);

    // Creating empty containers for center- and right pegs and adding them to
    // the disks-vector.
    std::vector<Disk*> disks_in_center_peg;
    std::vector<Disk*> disks_in_right_peg;
    disks_.push_back(disks_in_center_peg);
    disks_.push_back(disks_in_right_peg);

    // Drawing each disk on scene.
    for ( Disk* disk_to_be_drawn : disks_in_left_peg ) {
        game_area_.draw_disk(disk_to_be_drawn);
    }

}

void GameEngine::move_disk(int from_peg, int to_peg)
{

    Disk* disk_to_be_moved = nullptr;

    // Grapping selected disk.
    disk_to_be_moved = disks_.at(static_cast<std::size_t>(from_peg)).back();

    // Changing its color.
    disk_to_be_moved->change_color(random_color());

    // New position will be at the top of the destination peg.
    int new_position = static_cast<int>(disks_.at(static_cast<std::size_t>(to_peg)).size());

    // Changing disk's local stored location values.
    disk_to_be_moved->change_disk_location(to_peg, new_position);

    // Allocating the disk to new peg vector.
    disks_.at(static_cast<std::size_t>(from_peg)).pop_back();
    disks_.at(static_cast<std::size_t>(to_peg)).push_back(disk_to_be_moved);

    // Finally moving the graphical representation of the disk on scene.
    game_area_.move_disk_on_scene(disk_to_be_moved);

}

std::vector<std::pair<int, int> > GameEngine::get_illegal_moves()
{
    // Adding first- and last possible illegal moves to make sure they will
    // always be there.
    std::vector<std::pair<int, int> > illegal_moves =
    { {0,0}, {disks_.size()-1, disks_.size()-1} };

    // Will contain all of the top most disks of each peg.
    std::vector<int> first_disk_sizes;

    // Going through every peg and adding top disk to the vector.
    for ( auto peg : disks_ ) {
        if ( peg.empty() ) {
            // Big number representing empty for convenience. Only case where
            // this would cause problems is if someone set the biggest disk width
            // to be bigger than this.
            first_disk_sizes.push_back(9999999);
        } else {
            // Inserting size.
            first_disk_sizes.push_back(peg.back()->get_width());
        }
    }

    // Comapring the sizes.
    for ( int i = 0 ; i < static_cast<int>(first_disk_sizes.size()) ; ++i) {

        // It is always illegal to make move from peg n to peg n.
        add_to_vector(illegal_moves, {i, i});

        for ( int j = i+1 ; j < static_cast<int>(first_disk_sizes.size()) ; ++j ) {

            // Moving bigger disk on top of smaller is illegal (here if peg is
            // empty this will still apply cause even if initial disk size is
            // made bigger, no one has this many pixels in their screen.
            if ( (first_disk_sizes.at(static_cast<std::size_t>(i)) >
                  first_disk_sizes.at(static_cast<std::size_t>(j))) ) {

                add_to_vector(illegal_moves, {i, j});

            // If trying to add disk from empty peg to empty peg, both moves
            // are illegal.
            } else if ( first_disk_sizes.at(static_cast<std::size_t>(i)) ==
                        first_disk_sizes.at(static_cast<std::size_t>(j)) ) {

                add_to_vector(illegal_moves, {i, j});
                add_to_vector(illegal_moves, {j, i});

            // In other case, the opposite move will be illegal.
            } else {

                add_to_vector(illegal_moves, {j, i});
            }
        }

    }
    return illegal_moves;
}

bool GameEngine::is_game_over()
{

    bool game_over = true;

    // If all pegs exept the last are empty, game is over.
    for ( int i = 0 ; i < static_cast<int>(disks_.size()) - 1 ; ++i ) {

        if ( !is_peg_empty(i) ) {
            game_over = false;
        }
    }

    return game_over;
}

void GameEngine::empty_area()
{
    for( std::vector<Disk*> peg : disks_ ) {
        for ( Disk* disk_to_be_removed : peg ) {

            game_area_.removeItem(disk_to_be_removed);
            delete disk_to_be_removed;
            disk_to_be_removed = nullptr;
        }
    }

    disks_.clear();
}

QColor GameEngine::random_color()
{
    // Random values for red, gree, and blue components.
    int r = std::rand() % 255;
    int g = std::rand() % 255;
    int b = std::rand() % 255;

    QColor color(r,g,b);

    return color;
}

std::vector<int> GameEngine::get_disk_properties(int disk_amount)
{

    // Initially, standard sizes will be used.
    int biggest_disk_width = STANDARD_BIGGEST_DISK_WIDTH;
    int disk_height = STANDARD_DISK_HEIGHT;
    int disk_width_difference = STANDARD_DISK_SIZE_DIFFERENCE;

    // If however the standard size disk don't fit into peg, width and height
    // will be reduced untill all of the disks fit.
    int max_by_height = PEG_HEIGHT/disk_height;
    int max_by_width = (biggest_disk_width - MINIMUM_DISK_WIDTH)/disk_width_difference;

    // Reducing the size of the disks untill all of them fit.
    while ( (disk_amount > max_by_width) || (disk_amount > max_by_height)) {

        // Firstly, adding biggest disk's size rather than reducing size difference.
        if ( (disk_amount > max_by_width) &&
             (biggest_disk_width + 2 <= MAXIMUM_DISK_WIDTH) ) {

            biggest_disk_width = biggest_disk_width + 2;

        // If biggest disk is at maximium amount.
        } else if ( (biggest_disk_width >= MAXIMUM_DISK_WIDTH) &&
                    (disk_amount > max_by_width) ) {

            disk_width_difference = disk_width_difference - 2;
        }

        // Reducing disk height if necessary.
        if ( (disk_amount > max_by_height) &&
             (max_by_height - 1 > MINIMUM_DISK_HEIGHT)) {

            --disk_height;
        }

        // Calculating new maximum amount of disks.
        max_by_height = PEG_HEIGHT/disk_height;
        max_by_width = (biggest_disk_width - MINIMUM_DISK_WIDTH)/disk_width_difference;
    }

    std::vector<int> properties;

    // Adding properties to the vector.
    properties.push_back(biggest_disk_width);
    properties.push_back(disk_height);
    properties.push_back(disk_width_difference);

    return properties;

}

bool GameEngine::is_peg_empty(int peg)
{
    if ( disks_.at(static_cast<std::size_t>(peg)).empty() ) {
        return true;
    } else {
        return false;
    }
}

void GameEngine::add_to_vector(std::vector<std::pair<int,int> >& vector,
                               std::pair<int, int> move)
{
    if ( std::find(vector.begin(), vector.end(), move) == vector.end() ) {
        vector.push_back(move);
    }
}
