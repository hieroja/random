"""
Jere Liimatainen
3D_object_visualizer / 3-uloitteisten kappaleiden havainnollistaja

Finnish instructions:

Ohjelman tarkoitus on luoda 3-uloitteisia muotoja piirtämällä viivoja
canvakselle. Ohjelma "luo" kolmannen ulottuvuuden projisoimalla kappaleen x-
ja y-koordinaatit z-koordinaatin avulla, minkä avulla kappalaleet saadaan
näyttämään kolmiuloitteisilta.

Ohjelmassa on kolme valmiiksi määriteltyä kappaletta: kuutio, tetraedri ja
säännöllinen dodekaedri, valmiiden muotojen lisäksi käyttäjä voi halutessaan
luoda täysin oman kappaleensa valitsemalla Object typeksi "Custom objectin".
Custom object määritellään antamalla ohjelmalle haluttavan muodon
määrittelevät pisteet tupleina erottelemalla ne pilkulla ja väliliönnillä.
Pisteiden koordinaatit tulee taas erotella pilkulla (eli ilman välilyöntiä).

Pisteiden määrittelemisen lisäksi käyttäjä voi valita mitä pisteet yhdistetään
keskenään viivoilla. Tämä tapahtuu joko valitsemalla "Connect all points",
jolloin ohjelma piirtää kaikkien pisteiden välille viivat tai vastaavasti
käyttäjä voi valita "Custom point connection"-asetuksen, jolloin hän voi
määritellä minkä pisteiden välille viivat piirretään. Tässä tapauksessa
pisteet annetaan myös tupleina pilkun ja välilyönnin erottamina. Esim.
"(0,1), (0,2)" tarkoittaisi viivan piirtämistä ensimmäisen (indeksi 0) ja
toisen pisteen välille sekä ensimmäisen ja kolmannen pisteen välille
piirrettävää viivaa, mutta kolmannen ja toisen pisteen välille ei piirretä
viivaa.

Kappaleen näyttämisen lisäksi ohjelmalla on mahdollista pyörittää kappaletta
rotaatiomatriisien avulla, muokata kappaleen väriä, kokoa, viivojen paksuutta
ja kappaleen liikkumista ikkunassa erinäisin Scale-widgettien avulla.

Ohjelmasta löytyy "Update"-nappula, jota painamalla käyttäjän valitsemat
asetukset otetaan käyttöön. Napin painalluksen sijaan käyttäjä voi
vaihtoehtoisesti painaa Enter-näppäintä.

Ohjelman luomien kappaleiden pyörimisen sulavauus vahtelee riippuen
tietokoneen tehoista, ohjelma suositellaan ajettavaksi pöytäkoneella parhaan
kokemuksen saavuttamiseksi.
"""

from tkinter import *
import time
from math import *
import random
import itertools

def line_length(p1, p2):
    """
    Calculates the length of a line drawn between two points. (Same as the
    distance between two points.)

    :param tuple p1: First point. Coordinates are (x, y, z)
    :param tuple p2: Second point. Coordinates are (x, y, z)
    :return: The distance between p1 and p2.
    """

    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]

    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]

    length = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    return length


def point_connector(points):
    """
    Calculates all possible connections between given points.
    :param list points: Points are given in a list containing points as tuples.
    :return: All possible connections between given points as a list
             containing connections as tuples. A connection has the index of
             points to be connected, for example connection (0, 1) would mean
             connection from 1st point to 2nd point.
    """

    point_numbers = ()

    for i in range(len(points)):
        point_numbers += (i,)

    connections = ()
    for connection in itertools.combinations(point_numbers, 2):
        connections += connection,

    return connections


def matrix_multiplication(matrix, vector):
    """
    This function is used to multiply given vector with given matrix.
    :param list matrix: A 3x3 matrix that is a list containing all rows as
           lists.
    :param list vector: A 1x3 vector.
    :return: Resulting 1x3 vector as a list.
    """

    output_matrix = [0, 0, 0]

    for i in range(3):
        for n in range(len(matrix[i])):
            output_matrix[i] += matrix[i][n] * vector[n]

    return output_matrix


def rotation_matrix_x(degree):
    """
    This function returns a rotation matrix that will be used to rotate
    a vector around x-axis for given degree.
    :param float degree: Used to determinate how much rotation there will be.
    :return: The 3x3 rotation matrix for given degree as a list.
    """

    return [[cos(degree), 0, sin(degree)], [0, 1, 0],
            [-sin(degree), 0, cos(degree)]]


def rotation_matrix_y(degree):
    """
    This function returns a rotation matrix that will be used to rotate
    a vector around y-axis for given degree.
    :param float degree: Used to determinate how much rotation there will be.
    :return: The 3x3 rotation matrix for given degree as a list.
    """

    return [[1, 0, 0], [0, cos(degree), -sin(degree)],
            [0, sin(degree), cos(degree)]]


def rotation_matrix_z(degree):
    """
    This function returns a rotation matrix that will be used to rotate
    a vector around z-axis for given degree.
    :param float degree: Used to determinate how much rotation there will be.
    :return: The 3x3 rotation matrix for given degree as a list.
    """

    return [[cos(degree), -sin(degree), 0], [sin(degree), cos(degree), 0],
            [0, 0, 1]]


class Object:
    # This class is used to define a 3d object that can be drawn on a canvas.
    # The object will consist of given points that will be connected with
    # lines.

    def __init__(self, vertexes, edges, canvas_width, canvas_height, size,
                 color, chameleon_mode, thickness, velocity, x_rotation,
                 y_rotation, z_rotation):

        """
        :param list vertexes: List of points that are used to make the object.
               All points are given as tuples that contain the coordinates
               (x, y, z).
        :param list edges: List of edges that make the object. Each edge is a
               tuple containing the index of the points to be connected
               (p1, p2).
        :param int canvas_width: The width of the canvas the object will be
               drawn on.
        :param int canvas_height: The height of the canvas the object will be
               drawn on.
        :param float size: A float that is used to determinate the size of the
               object.
        :param tuple color: The RGB-color of the object as a (R, G, B) tuple.
        :param boolean chameleon_mode_setting: If chameleon_mode is set to 
               True, the object's color will vary.
        :param int thickness: The thickness of the lines that make the object.
        :param float velocity: The velocity of the object's movement.
        :param float x_rotation: Rotation speed around the object's x-axis.
               If set to 0, there will be no rotation around the x-axis.
        :param float y_rotation: Rotation speed around the object's y-axis.
               If set to 0, there will be no rotation around the y-axis.
        :param float z_rotation: Rotation speed around the object's z-axis.
               If set to 0, there will be no rotation around the z-axis.

        Additionally few more parameters will be needed to construct the
        object:

        :param float x_pos: The x-coordinate of the center position of the
               object.
        :param float y_pos: The y-coordinate of the center position of the
               object.
        :param boolean x_inc: If set to True, the object's x_pos will get
               bigger, if set to False, the object's x_pos will get smaller.
        :param boolean y_inc: If set to True, the object's y_pos will get
               bigger, if set to False, the object's y_pos will get smaller.

        x- and y_inc will be used to determinate the movement of the object.
        At the beginning both will be chosen by random.

        :param float x_degree: The degree of rotation around the object's
               x-axis. If x_rotation > 0, x_rotation will be added to x_degree
               every time the object moves on the canvas.
        :param float y_degree: The degree of rotation around the object's
               y-axis. If y_rotation > 0, y_rotation will be added to y_degree
               every time the object moves on the canvas.
        :param float z_degree: The degree of rotation around the object's
               z-axis. If z_rotation > 0, z_rotation will be added to z_degree
               every time the object moves on the canvas.
        :param boolean r_inc: This boolean is used to check if object's red
               color-value will be increased or decreased when chameleon mode 
               is activated.
        :param boolean g_inc: This boolean is used to check if object's green
               color-value will be increased or decreased when chameleon mode 
               is activated.
        :param boolean b_inc: This boolean is used to check if object's blue
               color-value will be increased or decreased when chameleon mode 
               is activated.
        """

        self.__vertexes = vertexes
        self.__edges = edges
        self.__canvas_width = canvas_width
        self.__canvas_height = canvas_height
        self.__size = size
        self.__color = color
        self.__chameleon_mode_setting = chameleon_mode
        self.__thickness = thickness
        self.__velocity = velocity
        self.__x_rotation = x_rotation
        self.__y_rotation = y_rotation
        self.__z_rotation = z_rotation

        self.__x_pos = canvas_width/2
        self.__y_pos = canvas_height/2
        self.__x_inc = random.choice([True, False])
        self.__y_inc = random.choice([True, False])
        self.__x_degree = 0
        self.__y_degree = 0
        self.__z_degree = 0
        self.__r_inc = True
        self.__g_inc = True
        self.__b_inc = True

        self.__z_pos = 0
        self.__z_inc = False

    def proj(self, point):
        """
        This function is used to rotate the object's three-dimensional point
        around x-, y- and z-axis, if rotation parameters are set higher than 0.
        After the rotations, it will project the 3D point into 2D space and
        return the result.
        :param tuple point: One of the object's points as a tuple (x, y, z)
        :return: The final projected point as a tuple that contains the points
                coordinates on the canvas (x, y)
        """

        matrixes_to_be_used = []

        if self.__x_rotation > 0:
            matrix_x = rotation_matrix_x(self.__x_degree)
            matrixes_to_be_used.append(matrix_x)

        if self.__y_rotation > 0:
            matrix_y = rotation_matrix_y(self.__y_degree)
            matrixes_to_be_used.append(matrix_y)

        if self.__z_rotation > 0:
            matrix_z = rotation_matrix_z(self.__z_degree)
            matrixes_to_be_used.append(matrix_z)

        result_point = point

        try:
            # If there aren't any rotation matrixes to be used, result_point
            # will stay as the default point.

            result_point = matrix_multiplication(matrixes_to_be_used[0], point)
            for matrix in matrixes_to_be_used[1:]:
                result_point = matrix_multiplication(matrix, result_point)

        except IndexError:
            pass

        x, y, z = result_point    # Extract the x-, y- and z-coordinates.
        f = z + self.__size    # Projection value f will also determinate size.
        x, y = x * f, y * f    # The actual projection to 2D space

        # The point's final position will also depend on the object's center,
        # therefore the centerpoint's coordinates will be added.
        x += self.__x_pos
        y += self.__y_pos

        return int(x), int(y)

    def point_rotation(self):
        """
        This function is used to increase the degrees used in object rotation
        if the corresponding rotation settings are set to be higher than 0.
        :return: none
        """

        if self.__x_rotation > 0:
            self.__x_degree += self.__x_rotation

        if self.__y_rotation > 0:
            self.__y_degree += self.__y_rotation

        if self.__z_rotation > 0:
            self.__z_degree += self.__z_rotation

    def max_cordinates(self):
        """
        This function is used to calculate the object's maximum and minimum
        coordinates.
        :return: The maximum and minimum x- and y-coordinates.
        """

        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0

        for vertex in self.__vertexes:
            # Loops over object's vertexes, projects them to 2-dimensional
            # space, and finds the max and min coordinates.

            vertex = self.proj(vertex)

            if vertex[0] > max_x:
                max_x = vertex[0]
            elif vertex[0] < min_x:
                min_x = vertex[0]

            if vertex[1] > max_y:
                max_y = vertex[1]
            elif vertex[1] < min_y:
                min_y = vertex[1]

        return max_x, min_x, max_y, min_y

    def move_object(self, max_x, min_x, max_y, min_y):
        """
        This function moves the object's position (the center of the object)
        on the canvas. This function also checks if any of the object's
        vertexes touches the edges of the canvas, if this happens, the
        movement direction will be flipped accordingly.
        :param float max_x: The object's maximum x-coordinate
        :param float min_x: The object's minimum x-coordinate
        :param float max_y: The object's maximum y-coordinate
        :param float min_y: The object's minimum y-coordinate
        :return: none
        """

        if self.__x_inc:
            self.__x_pos += self.__velocity

        # Collusion with the right edge of the canvas.
        if max_x >= self.__canvas_width:
            self.__x_inc = False

        if self.__x_inc == False:
            self.__x_pos -= self.__velocity

        # Collusion with the left edge of the canvas.
        if min_x < 0:
            self.__x_inc = True


        if self.__y_inc:
            self.__y_pos += self.__velocity

        # Collusion with the bottom edge of the canvas.
        if max_y >= self.__canvas_height:
            self.__y_inc = False

        if self.__y_inc == False:
            self.__y_pos -= self.__velocity

        # Collusion with the top edge of the canvas.
        if min_y < 0:
            self.__y_inc = True

    def chameleon_mode(self):
        """
        This function is used to make the object change color over time, if
        chameleon mode is selected.
        :return: none
        """

        if self.__chameleon_mode_setting:

            # Gets the red-, green- and blue color values.
            r = self.__color[0]
            g = self.__color[1]
            b = self.__color[2]

            # For each color, checks if the color has reached its limits and
            # adjusts the corresponding color increasement parameters
            # accordingly.
            if r == 255:
                self.__r_inc = False
            elif r == 0:
                self.__r_inc = True

            if g == 255:
                self.__g_inc = False
            elif g == 0:
                self.__g_inc = True

            if b == 255:
                self.__b_inc = False
            elif b == 0:
                self.__b_inc = True

            # Next increases or decreases each color-value accordingly.
            if self.__r_inc:
                r += 1
            else:
                r -= 1

            if self.__g_inc:
                g += 1
            else:
                g -= 1

            if self.__b_inc:
                b += 1
            else:
                b -= 1

            # Finally sets the object's color to be the final value.
            self.__color = (r, g, b)

    def draw(self, canvas):
        """
        Draws the object into given canvas.
        :param tkinter Canvas widget canvas: The canvas that the object will be
               drawn on. This is also used to get the canvas' width and height
               in case it has changed from the original size.
        :return: none
        """

        # Update the current canvas size.
        self.__canvas_width = canvas.winfo_width()
        self.__canvas_height = canvas.winfo_height()

        # Get the current maximum coordinates of the object and move the object
        # accordingly.
        max_x, min_x, max_y, min_y = self.max_cordinates()

        if self.__velocity == 0:
            # Set the object to the center of the canvas, this is done to keep
            # the object at the center even if the window size is modified.
            self.__x_pos = self.__canvas_width/2
            self.__y_pos = self.__canvas_height/2

        else:
            self.move_object(max_x, min_x, max_y, min_y)

        # Change the object color if necessary.
        self.chameleon_mode()

        for edge in self.__edges:
            # Loop over every edge of the object and get the corresponding
            # vertexes that make up the edge. Project these points into
            # 2-dimensional space to get the actual coordinates for each line,
            # that make up the object.
            p1 = self.proj(self.__vertexes[edge[0]])
            p2 = self.proj(self.__vertexes[edge[1]])

            # Draw the line that makes the edge in question.
            # The 'fill'-command takes in hexadecimal values, so the RGB value
            # needs to be converted to hexadecimal.
            canvas.create_line(p1, p2, fill='#%02x%02x%02x' % self.__color,
                               width=self.__thickness)

        # After each of the object's lines have been drawn, increases the
        # rotation degrees if needed.
        self.point_rotation()


class Interface:
    # This class is used to create the GUI of the program and to draw the
    # object.

    def __init__(self):
        
        # Root settings
        # ====================================================================
        
        # Used to configure the starting size of the program, to check if user 
        # wants to skip intro and to initialize settings canvas, wich will be
        # used as a host to all of the program's widgets.

        self.__root = Tk()
        self.__root.title("Interface test")
        self.__root.geometry("1152x864")
        self.__root.configure()
        self.__intro_font = "Consolas 10"
        self.__x_pressed = False
        self.__root.protocol("WM_DELETE_WINDOW", self.quit)

        if not disable_intro:
            self.welcome()

        self.__root.bind("<Return>", self.start_object)
        self.__settings_canvas = Canvas(self.__root)
        self.__settings_canvas.pack(side=LEFT, fill=BOTH)
        # ====================================================================

        # Shape settings
        # ====================================================================

        # These widgets are used to select the shape of the object, if user
        # has selected custom object setting, will call functions to
        # initialize custom shape options.

        self.__object_shape_frame = LabelFrame(self.__settings_canvas,
                                               text="Object type")
        self.__object_shape_frame.pack(pady=5)
        
        self.__object_shape = StringVar(self.__object_shape_frame)
        self.__shape_options = [
            "Regular dodecahedron",
            "Cube",
            "Tetrahedron",
            "Custom object"
        ]
        self.__object_shape.set(self.__shape_options[0])
        self.__object_shape_widget = OptionMenu(self.__object_shape_frame,
                                                self.__object_shape,
                                                *self.__shape_options)
        self.__object_shape_widget.pack(pady=5)
        self.__object_shape.trace("w", callback=self.custom_shape_menu)
        # ====================================================================

        # Rotation settings
        # ====================================================================

        # These widgets are used to determinate the rotation of the object
        # around its own center point.

        self.__object_rotation_frame = LabelFrame(self.__settings_canvas,
                                                  text="Rotation settings")
        self.__object_rotation_frame.pack(pady=5)
        self.__random_rotation = BooleanVar(self.__object_rotation_frame,
                                            value=True)

        self.__x_rotation_label = Label(self.__object_rotation_frame, text="X")
        self.__x_rotation_label.grid(row=0, column=0)
        self.__x_rotation_value = Scale(self.__object_rotation_frame,
                                        from_=0, to=20, orient=VERTICAL)
        self.__x_rotation_value.set(5)
        self.__x_rotation_value.grid(row=1, column=0)

        self.__y_rotation_label = Label(self.__object_rotation_frame, text="Y")
        self.__y_rotation_label.grid(row=0, column=1)
        self.__y_rotation_value = Scale(self.__object_rotation_frame, from_=0,
                                        to=20, orient=VERTICAL)
        self.__y_rotation_value.set(5)
        self.__y_rotation_value.grid(row=1, column=1)

        self.__z_rotation_label = Label(self.__object_rotation_frame, text="Z")
        self.__z_rotation_label.grid(row=0, column=2)
        self.__z_rotation_value = Scale(self.__object_rotation_frame, from_=0,
                                        to=20, orient=VERTICAL)
        self.__z_rotation_value.set(0)
        self.__z_rotation_value.grid(row=1, column=2)
        # ====================================================================

        # Color settings
        # ====================================================================

        # These widgets are used to set the color of the object to a permanent
        # color or alternating color if chameleon-mode is selected.

        self.__color_picker_frame = LabelFrame(self.__settings_canvas,
                                               text="Object color")
        self.__color_picker_frame.pack(pady=5)
        self.__random_color = BooleanVar(self.__color_picker_frame,
                                         value=False)
        self.__chameleon_mode = Checkbutton(self.__color_picker_frame,
                                            variable=self.__random_color,
                                            text="Chameleon mode")
        self.__chameleon_mode.grid(row=2, column=0, columnspan=3)

        self.__red_label = Label(self.__color_picker_frame, text="Red")
        self.__red_label.grid(row=0, column=0)
        self.__red_slider = Scale(self.__color_picker_frame, from_=0, to=255,
                                  orient=VERTICAL)
        self.__red_slider.set(0)
        self.__red_slider.grid(row=1, column=0)

        self.__green_label = Label(self.__color_picker_frame, text="Green")
        self.__green_label.grid(row=0, column=1)
        self.__green_slider = Scale(self.__color_picker_frame, from_=0, to=255,
                                    orient=VERTICAL)
        self.__green_slider.set(255)
        self.__green_slider.grid(row=1, column=1)

        self.__blue_label = Label(self.__color_picker_frame, text="Blue")
        self.__blue_label.grid(row=0, column=2)
        self.__blue_slider = Scale(self.__color_picker_frame, from_=0, to=255,
                                   orient=VERTICAL)
        self.__blue_slider.set(0)
        self.__blue_slider.grid(row=1, column=2)
        # ====================================================================

        # Size settings
        # ====================================================================

        self.__object_size_frame = LabelFrame(self.__settings_canvas,
                                              text="Object size")
        self.__object_size_frame.pack(pady=5)
        self.__object_size = Scale(self.__object_size_frame, from_=20, to=150,
                                   orient=HORIZONTAL)
        self.__object_size.set(100)
        self.__object_size.pack()
        # ====================================================================

        # Thickness settings
        # ====================================================================

        self.__object_thickness_frame = LabelFrame(self.__settings_canvas,
                                                   text="Object thickness")
        self.__object_thickness_frame.pack(pady=5)
        self.__object_thickness = Scale(self.__object_thickness_frame, from_=1,
                                        to=10, orient=HORIZONTAL)
        self.__object_thickness.set(3)
        self.__object_thickness.pack()
        # ====================================================================

        # Velocity settings
        # ====================================================================
        self.__object_velocity_frame = LabelFrame(self.__settings_canvas,
                                                  text="Object velocity")
        self.__object_velocity_frame.pack(pady=5)
        self.__object_velocity = Scale(self.__object_velocity_frame, from_=0,
                                       to=3, resolution=.1, orient=HORIZONTAL)
        self.__object_velocity.set(0)
        self.__object_velocity.pack()
        # ====================================================================

        # Update-button and canvas
        # ====================================================================

        # Update button is used to update the object with the currently
        # selected object settings. self.__canvas is used as a background to
        # the object.

        self.__update_button = Button(self.__settings_canvas,
                                      text="Update\n<Enter>",
                                      command=self.start_object)
        self.__update_button.pack()
        
        self.__canvas = Canvas(self.__root, bg=BLACK)
        self.__canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # ====================================================================

        self.start_object()  # Start the object with default settings on start.

        # Checks if user has clicked the "X"-button.
        if self.crashed():
            return

        self.__root.mainloop()

    def quit(self):
        # Executed when the "X"-button is pressed.

        print('User pressed "X", program terminating')
        self.__x_pressed = True

    def crashed(self):
        # Check's if the "X"-button is pressed.

        if self.__x_pressed:
            return True
        else:
            return

    def stop_intro(self):
        # Used to check if user pressed spacebar to skip the intro.
        if self.__stop_intro_flag:
            self.__canvas.destroy()
            self.__root.unbind("<space>")
            print("Intro skipped")

            return True

        else:
            return False

    def set_stop_intro(self, *args):
        # Sets stop_intro_flag.
        self.__stop_intro_flag = True

    def welcome(self):
        # This method is used to create the intro for this program. All above
        # elements are purely for cosmetic purposes and do not affect the 
        # program's functionality.

        self.__canvas = Canvas(self.__root, bg=BLACK)
        self.__canvas.pack(expand=True, fill=BOTH)
        self.__canvas.update()

        # If user presses space, the intro will be skipped.
        self.__stop_intro_flag = False
        self.__root.bind("<space>", self.set_stop_intro)
        
        # Actual width and height of a single char in pixels as a tuple.
        char_dimensions = self.string_dimensions("|")
        
        # ASCII-art of the welcoming text.
        WELCOME = \
"     ____      ____  ________   _____        ______     ___     ____    ____   ________ \n\
    |_  _|    |_  _||_   __  | |_   _|     .' ___  |  .'   `.  |_   \  /   _| |_   __  |\n\
      \ \  /\  / /    | |_ \_|   | |      / .'   \_| /  .-.  \   |   \/   |     | |_ \_|\n\
       \ \/  \/ /     |  _| _    | |   _  | |        | |   | |   | |\  /| |     |  _| _ \n\
        \  /\  /     _| |__/ |  _| |__/ | \ `.___.'\ \  `-'  /  _| |_\/_| |_   _| |__/ |\n\
         \/  \/     |________| |________|  `.____ .'  `.___.'  |_____||_____| |________|"


        WELCOME_width, WELCOME_height = self.string_dimensions(WELCOME)
        
        WELCOME_chars = []
        empty_WELCOME_chars = []
        
        # Creating similar sized string but with spaces.
        for char in WELCOME:
            WELCOME_chars.append(char)
            if char != "\n":
                empty_WELCOME_chars.append(" ")
            else:
                empty_WELCOME_chars.append("\n")

        # At first, revealed strings height is same as one char's height.
        revealed_chars_height = char_dimensions[1]

        welcome_printed = False   # Used to determinate if WELCOME is printed.
        
        CURSOR_COLOR = WHITE    # Set initial cursor color


        # The speed of wich the WELCOME text is writen and deleted.
        PRINT_SPEED = 0.005

        if not welcome_printed:
            revealed_chars_row = ""
            all_revealed_chars = ""

            # Makes the cursor blink at the start.
            for n in range(5):

                # Check's if space or "X" is pressed. Space skips the intro,
                # "X" press shuts down the whole program.
                if self.stop_intro() or self.crashed():
                    return

                # Starting point of WELCOME.
                x = (self.__root.winfo_width() - WELCOME_width) // 2
                y = (self.__root.winfo_height() - WELCOME_height) // 2

                # Determinates the starting and ending point of the cursor.
                x0 = x + self.string_dimensions(revealed_chars_row)[0] - 5
                x1 = x0 + char_dimensions[0]
                y1 = y + revealed_chars_height
                y0 = y1 - char_dimensions[1]

                self.__canvas.create_rectangle(x0, y0, x1, y1,
                                               fill=CURSOR_COLOR)

                self.__canvas.create_text(self.__root.winfo_width() / 2,
                                          self.__root.winfo_height() / 1.1,
                                          fill=GREY, anchor=N,
                                          text="Press SPACE to skip intro",
                                          font=self.__intro_font)

                self.update_all()

                # Cursor blinking.
                if CURSOR_COLOR == WHITE:
                    CURSOR_COLOR = BLACK
                else:
                    CURSOR_COLOR = WHITE

                time.sleep(0.7)

            # Prints WELCOME one letter at a time.
            for i in range(len(WELCOME_chars)):
                if self.stop_intro() or self.crashed():
                    return

                x = (self.__root.winfo_width() - WELCOME_width) // 2
                y = (self.__root.winfo_height() - WELCOME_height) // 2

                revealed_chars_row += WELCOME_chars[i]
                all_revealed_chars += WELCOME_chars[i]

                if WELCOME_chars[i] == "\n":
                    revealed_chars_row = ""
                    revealed_chars_height = \
                    self.string_dimensions(all_revealed_chars)[1]

                empty_WELCOME_chars[i] = WELCOME_chars[i]
                text = "".join(empty_WELCOME_chars)

                x0 = x + self.string_dimensions(revealed_chars_row)[0] - 5
                x1 = x0 + char_dimensions[0]
                y1 = y + revealed_chars_height
                y0 = y1 - char_dimensions[1]

                self.__canvas.create_rectangle(x0, y0, x1, y1,
                                               fill=WHITE)

                self.__canvas.create_text(x, y, fill=GREEN, anchor=NW,
                                          text=text, font=self.__intro_font)

                self.update_all()
                time.sleep(PRINT_SPEED)

            # Makes the cursor blink at the end of printing WELCOME.
            for n in range(5):
                if self.stop_intro() or self.crashed():
                    return

                x = (self.__root.winfo_width() - WELCOME_width) // 2
                y = (self.__root.winfo_height() - WELCOME_height) // 2

                x0 = x + self.string_dimensions(revealed_chars_row)[0] - 5
                x1 = x0 + char_dimensions[0]
                y1 = y + revealed_chars_height
                y0 = y1 - char_dimensions[1]

                self.__canvas.create_rectangle(x0, y0, x1, y1,
                                               fill=CURSOR_COLOR)

                self.__canvas.create_text(x, y, fill=GREEN, anchor=NW,
                                          text=WELCOME,
                                          font=self.__intro_font)

                # Cursor blinking.
                if CURSOR_COLOR == WHITE:
                    CURSOR_COLOR = BLACK
                else:
                    CURSOR_COLOR = WHITE

                self.update_all()
                time.sleep(0.7)

            # Erases WELCOME-text two characters at a time, one from front one
            # from the end of the text.
            for i in range(len(WELCOME_chars) // 2):
                if self.stop_intro() or self.crashed():
                    return

                if WELCOME_chars[i] != "\n":
                    WELCOME_chars[i] = " "

                if WELCOME_chars[-i] != "\n":
                    WELCOME_chars[-i] = " "

                text = "".join(WELCOME_chars)

                cursor = self.__canvas.create_text(
                    (self.__root.winfo_width() - WELCOME_width) // 2,
                    (self.__root.winfo_height() - WELCOME_height) // 2,
                    fill=GREEN, anchor=NW,
                    text=text, font=self.__intro_font)

                self.update_all()
                time.sleep(PRINT_SPEED)

            self.__canvas.destroy()

            return

    def update_all(self):
        # Used to update root and canvas and clear canvas after updates, this
        # is used to animate things on canvas.
        self.__canvas.update()
        self.__root.update()
        self.__canvas.pack(expand=True, fill=BOTH)
        self.__canvas.delete(ALL)

    def custom_shape_menu(self, *args):
        # Used to construct a custom shape menu if selected at shape options,
        # additionally if different stock shape is selected, will destroy the
        # menu. Also if custom point connection is selected, will call
        # custom point connection function.

        try:
            self.__custom_points.get()

            if self.__object_shape.get() != "Custom object":
                self.__custom_points.destroy()
                self.__custom_points_label.destroy()
                self.__connect_all_points_box.destroy()
                self.__custom_connection_box.destroy()
                self.__custom_point_connection_label.destroy()
                self.__custom_point_connection.destroy()

        except:
            if self.__object_shape.get() == "Custom object":
                self.__custom_points_label = Label(self.__object_shape_frame,
                                                   text="Enter custom points as tuples:")
                self.__custom_points_label.pack(anchor=W, pady=2)
                self.__custom_points = Entry(self.__object_shape_frame)
                self.__custom_points.insert(1, "")
                self.__custom_points.pack(anchor=W, pady=2)
                self.__point_connection_type = BooleanVar(self.__object_shape_frame,
                                                    value=True)
                self.__connect_all_points_box = Radiobutton(
                                                self.__object_shape_frame,
                                                text="Connect all points",
                                                variable=self.__point_connection_type,
                                                value=True)
                self.__custom_connection_box = Radiobutton(
                                               self.__object_shape_frame,
                                               text="Custom point connection",
                                               variable=self.__point_connection_type,
                                               value=False)

                self.__connect_all_points_box.pack(anchor=W, pady=2)
                self.__custom_connection_box.pack(anchor=W, pady=2)
                self.__point_connection_type.trace("w",
                                                   callback=self.custom_point_connection_menu)

    def custom_point_connection_menu(self, *args):
        # This function is called to create custom point connection menu. If
        # custom point connection is not selected, will destroy the menu.

        point_connection_type = self.__point_connection_type.get()
        try:
            self.__custom_point_connection.get()
            if point_connection_type == True:
                self.__custom_point_connection_label.destroy()
                self.__custom_point_connection.destroy()

        except:
            if point_connection_type == False:
                self.__custom_point_connection_label = Label(self.__object_shape_frame,
                                                             text="Enter custom points as tuples:")
                self.__custom_point_connection_label.pack(anchor=W, pady=2)
                self.__custom_point_connection = Entry(self.__object_shape_frame)
                self.__custom_point_connection.insert(1, "")
                self.__custom_point_connection.pack(anchor=W, pady=2)

    def entryfield_error(self, entryfield, packtype, grid_row, grid_column):
        """
        Used to show error message on entry field for a brief period of time
        when executed.
        :param Entry-widget entry field: The entry filed that the error message
               is going to be shown on.
        :param str pack type: The managing type of the entry field.
        :param int grid_row: The row of given grid.
        :param int grid_column: The column of given grid.
        :return: None
        """

        # Original entry is stored in variable so that it can be put back on
        # the field after error message is shown.
        original_entry = entryfield.get()

        # Show error message on field.
        entryfield.delete(0, END)
        entryfield.insert(1, "Invalid input!")
        entryfield.configure(foreground=RED)

        if packtype == "pack":
            entryfield.pack(pady=5)
        else:
            entryfield.grid(row=grid_row, column=grid_column)

        # Show changes and wait for a bit before restoring to original value.
        self.__root.update()
        time.sleep(0.5)

        entryfield.delete(0, END)
        entryfield.insert(1, original_entry)

        if packtype == "pack":
            entryfield.pack(pady=5)
        else:
            entryfield.grid(row=grid_row, column=grid_column)

    def string_dimensions(self, string):
        """
        This function measures the actual width and height of given string in
        actual pixels and returns both values.
        :param str string: String of character/characters to be measured.
        :return: A tuple containing the width and height of the input string
                 in pixels (width, height)
        """

        # Puts the desired string on root.
        measure = Label(Frame(self.__root), font=self.__intro_font,
                        text=string)

        measure.grid(row=0, column=0)
        measure.update_idletasks()

        # Gets the actual measures of the string.
        string_width = measure.winfo_width()
        string_height = measure.winfo_height()
        measure.destroy()

        return string_width, string_height

    # These next methods, "_get"-ending functions, are used to check user's
    # set settings and return them. They are used to construct the object.

    def custom_points_get(self, points_str):
        """
        Convert's given string of points into a list containing all vertexes
        as tuples (x, y, z).
        :param Entry-widget points_str: An entry field containing user's given
               points as a string of text. The string should be formatted as:
               "(x1,y1,z1), (x2,y2,z2)", otherwise will return error.
        :return: Complete list containing all given vertexes as tuples, or an
                 error message.
        """

        object_points = ()
        object_points_strlist = points_str.get().split(", ")

        for value in object_points_strlist:
            value = value.strip()

            # All points have to have exatly 3 values (x,y,z).
            if len(value.split(",")) != 3:
                return "custom points error"

            point = ()

            if ")" in value:
                value = value[1:-1]
            else:
                value =value[1:]

            for cordinate in value.split(","):
                point += (int(cordinate),)

            object_points += (point,)

        return object_points

    def custom_point_connections_get(self, point_connections, object_points,
                                     max_connections):
        """
        Used to check if user's given custom point connections are given
        correctly, return's error if not. A connection is represented as for
        example: (0, 1), which means connect the first vertex to the second.
        :param Entry-widget point_connections: The entry that contains the
               connections as a list of tuples.
        :param lst object_points: A list that contains the vertexes of the
               object as tuples. This is used to check that given connections
               aren't out of range.
        :param lst max_connections: A list that contains all possible
               connections between object vertexes.
        :return: A list of connections between the object's vertexes or error.
        """

        connections = ()
        connections_strlist = point_connections.get().split(", ")

        max_index = len(object_points)

        for value in connections_strlist:
            value = value.strip()

            connection = ()

            if ")" in value:
                value = value[1:-1]
            else:
                value = value[1:]

            # Makes sure there are only 2 vertexes to be connected.
            if len(value.split(",")) != 2:
                return "connecting points error"

            for vertex_index in value.split(","):

                # Makes sure the given index is in range.
                if int(vertex_index) < 0 or int(vertex_index) > max_index:
                    return "connecting points error"

                if len(connection) != len(set(connection)):
                    return "connecting points error"

                # Creates the connection that is going to be added to the list
                # containing the connections.
                connection += (int(vertex_index),)

            connections += (connection,)

        # Finally checks that there aren't dublicate connections.
        if len(connections) > len(max_connections):
            return "connecting points error"

        return connections

    def selected_object_get(self, objects, default_object_settings):
        """
        Used to determinate what object-type has been selected.
        :param lst objects: List of pre-defined objects.
        :param lst default_object_settings: A list containing settings, that
               are needed to construct the object.
        :return: Fully constructed Object-class with settings chosen by user
                or an error message.
        """

        # Formatting the shape name.
        shape_name = self.__object_shape.get().lower()

        if " " in shape_name:
            shape_name = shape_name.replace(" ", "_")

        if shape_name == "custom_object":   # User selected custom object.

            # Checks what kind of connection is going to be used.
            point_connection_type = self.__point_connection_type.get()

            # Gets the custom points given by user and returns error if needed.
            try:
                object_points = self.custom_points_get(self.__custom_points)
                if object_points == "custom points error":
                    return "custom points error"

            except:
                return "custom points error"

            # There needs to be at least 2 point to draw an object.
            if len(object_points) < 2:
                return "custom points error"

            # All possible connections between vertexes.
            max_connections = point_connector(object_points)

            if point_connection_type:
                object_edges = max_connections

            else:   # User want's to use custom connections.
                try:
                    object_edges = self.custom_point_connections_get(self.__custom_point_connection,
                                                                     object_points,
                                                                     max_connections)

                    # Checks for error.
                    if object_edges == "connecting points error":
                        return "connecting points error"

                except:
                    return "connecting points error"

            # Finally, if no errors occurred, constructs the Object with given
            # vertexes and edges.
            object = Object(object_points, object_edges,
                            *default_object_settings)

        else:
            # If user has selected pre-defined object.
            object = objects[shape_name]

        return object

    def color_get(self):
        # Used to return user's color choice in RGB-tuple.

        if self.__random_color.get() == False:
            r = int(self.__red_slider.get())
            g = int(self.__green_slider.get())
            b = int(self.__blue_slider.get())

        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

        return (r, g, b)

    def rotations_get(self):
        # Used to return user's chosen rotation amounts. The actual amounts
        # are converted into smaller values.

        x_rotation = float(self.__x_rotation_value.get()) * 0.001
        y_rotation = float(self.__y_rotation_value.get()) * 0.001
        z_rotation = float(self.__z_rotation_value.get()) * 0.001

        return x_rotation, y_rotation, z_rotation

    def start_object(self, *args):
        """
        This method is used to construct the object with user's configuration
        and to animate the movement of the object.
        :return: None
        """

        x_rotation, y_rotation, z_rotation = self.rotations_get()

        # No matter what kind of object will be defined, these settings will
        # be the same for all.
        default_object_settings = [
            self.__canvas.winfo_width(),
            self.__canvas.winfo_height(),
            self.__object_size.get(),
            self.color_get(),
            self.__random_color.get(),
            int(self.__object_thickness.get()),
            self.__object_velocity.get(),
            x_rotation,
            y_rotation,
            z_rotation
            ]

        # Pre-defined objects.
        objects = {
            "cube": Object(
            cube_vertexes,
            cube_edges,
            *default_object_settings),

            "tetrahedron": Object(
                tetrahedron_vertexes,
                tetrahedron_edges,
                *default_object_settings),

            "regular_dodecahedron": Object(
                regular_dodecahedron_vertexes,
                regular_dodecahedron_edges,
                *default_object_settings)
        }

        object = self.selected_object_get(objects, default_object_settings)
        
        try:
            if object == "custom points error":
                raise IndexError
            
            elif object == "connecting points error":
                raise ValueError

            # This makes sure that the entry fields containing custom point
            # settings have black font on them when there is no error raised.
            if self.__object_shape.get() == "Custom object":
                self.__custom_points.configure(foreground=BLACK)

                try:
                    self.__custom_point_connection.configure(foreground=BLACK)
                except:
                    pass

        # Using the entryfield_error method to show error message on the
        # entry-widget.
        except IndexError:
            print("custom points error occured!")
            self.entryfield_error(self.__custom_points, "pack", 0, 0)

            if object == "connecting points error":
                print("connecting points error occured!")
                self.entryfield_error(self.__custom_point_connection, "pack",
                                      0, 0)
                
            return

        except ValueError:
            print("connecting points error occured!")
            self.entryfield_error(self.__custom_point_connection, "pack", 0, 0)
            
            return

        while True:
            if self.crashed():
                return

            object.draw(self.__canvas)
            self.update_all()

            time.sleep(0.001)


BLACK = "#000000"
GREY = "#4f4f4f"
WHITE = "#ffffff"
RED = "#ff0000"
GREEN = "#00ff00"
BLUE = "#0000ff"

PHI = (1+sqrt(5))/2   # Golden ratio
regular_dodecahedron_vertexes = (-1, 1, 1), (-1, -1, 1), (1, -1, 1), \
                                (1, 1, 1), (-1, 1, -1), (-1, -1, -1), \
                                (1, -1, -1), (1, 1, -1), (0, PHI, 1/PHI), \
                                (0, -PHI, -1/PHI), (0, PHI, -1/PHI), \
                                (0, -PHI, 1/PHI), (1/PHI, 0, PHI), \
                                (-1/PHI, 0, -PHI), (-1/PHI, 0, PHI), \
                                (1/PHI, 0, -PHI), (PHI, 1/PHI, 0), \
                                (-PHI, -1/PHI, 0), (-PHI, 1/PHI, 0), \
                                (PHI, -1/PHI, 0)

REGULAR_DODECAHEDRON_EDGE_LENGTH = "{:5f}".format(sqrt(5) - 1)
regular_dodecahedron_edges = ()

a1 = ()
# b has the index of all dodecahedron vertexes. The for-loop is used to create
# all possible connections between the vertexes.
b = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
for value in itertools.combinations(b, 2):
    a1 += value,

# Next for-loop is used to check if a certain connection between 2 points, aka
# certain edge is the same length as REGULAR_DODECAHEDRON_EDGE_LENGTH, if so
# it will be added to regular_dodecahedron_edges.
try:
    for item in a1:
        l = "{:5f}".format(line_length(regular_dodecahedron_vertexes[item[0]],
                                       regular_dodecahedron_vertexes[item[1]])
                           )

        if l == REGULAR_DODECAHEDRON_EDGE_LENGTH:
            regular_dodecahedron_edges += (item[0], item[1]),
except:
    pass

cube_vertexes = (-1, 1, 1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, -1), \
                (-1, -1, -1), (1, -1, -1), (1, 1, -1)

cube_edges = (0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), \
             (4, 5), (4, 7), (5, 6), (6, 7)

tetrahedron_vertexes = (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)

tetrahedron_edges = (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)

disable_intro = False  # Disables intro if set to True.


def main():
    Interface()


main()
