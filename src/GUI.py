import arcade
import arcade.gui
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent

from engine import *
from screenconfig import *

global LEVEL

LEVEL = 2

cur_song_index = 0
songs = ["../music/music1.mp3", "../music/music2.mp3", "../music/music3.mp3"]
my_music = arcade.load_sound(songs[cur_song_index])
media_player = my_music.play(volume=0.5)


default_style = {
    "font_name": ("Kenney Future"),
    "font_size": 15,
    "font_color": arcade.color.WHITE,
}

'''
GRAPHICAL USER INTERFACE - Arcade library was used to implement the GUI. The View class was used to
switch between screens, therefore, each specific screen has a view (e.g. menu, tutorial, difficulty leve, the game itself,
game over screen, etc).
'''

#Menu screen
class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    #Function called when setting the screen
    def on_show_view(self):
        """ Called when switching to this view"""

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        #Setting the background
        self.background = arcade.load_texture("../img/back.png")

        self.v_box = arcade.gui.UIBoxLayout()

        # Create text
        ui_text_label = arcade.gui.UITextArea(text="BATTLESHIP - BRALUX",
                                              x=120,
                                              y=300,
                                              width=884,
                                              height=90,
                                              font_size=35,
                                              font_name="Kenney Future")

        self.manager.add(ui_text_label)

        #Texture for the buttons
        texture = arcade.load_texture(
            ":resources:onscreen_controls/flat_dark/play.png")
        play_button = arcade.gui.UITextureButton(texture=texture)
        self.v_box.add(play_button.with_space_around(top=60))

        #Settings button
        settings_button = arcade.gui.UIFlatButton(
            text="SETTINGS", width=200, style=default_style)
        self.v_box.add(settings_button.with_space_around(top=40))

        #Tutorial button
        tutorial_button = arcade.gui.UIFlatButton(
            text="TUTORIAL", width=200, style=default_style)
        self.v_box.add(tutorial_button.with_space_around(top=40))

        #What happens when user clicks button
        @play_button.event("on_click")
        def on_click_texture_button(event):
            self.manager.disable()
            player = GridPlayer(10, LEVEL)
            enemy = GridPC(10)
            enemy.place_all_boats_random()
            game_view = GameView(player, enemy)
            self.window.show_view(game_view)

        #What happens when user clicks button
        @settings_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            setting_view = SettingsView()
            self.window.show_view(setting_view)
            # pass
        
        #What happens when user clicks button
        @tutorial_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            tutorial_view = TutorialView()
            self.window.show_view(tutorial_view)

        #Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    #Function called each time the screen is refreshed
    def on_draw(self):
        """ Draw the menu """
        #Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_rectangle_filled(
            410, 368,  width=994,  height=70, color=arcade.color.BLACK)

        #Draw the screen
        self.manager.draw()

#Tutorial screen
class TutorialView(arcade.View):
    """ Class to manage the game over view """

    def on_show_view(self):
        """ Called when switching to this view"""
        #Set background
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="TUTORIAL:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future", x=110, y=380)
        self.manager.add(ui_text_label.with_space_around(bottom=350))

        x_b = 50
        y_b = 20
        
        #Menu button
        menu_button = arcade.gui.UIFlatButton(
            text="MENU", style=default_style, x=x_b, y=y_b, width=90)
        self.manager.add(menu_button)

        #Texture for the button
        texture_advance = arcade.load_texture(
            ":resources:onscreen_controls/flat_dark/right.png")
        advance_button = arcade.gui.UITextureButton(
            texture=texture_advance, x=x_b+600, y=y_b)
        self.manager.add(advance_button.with_space_around(bottom=20))

        #What happens when the user clicks
        @menu_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = MenuView()
            self.window.show_view(menu_view)

        @advance_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = Tutorial2()
            self.window.show_view(menu_view)

        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    #What happens when the screen refreashes
    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("To configure the initial setup of your grid,",
                         start_x=530, start_y=350, font_size=10)
        arcade.draw_text("you will have to place 8 ships in total, 2",
                         start_x=530, start_y=330, font_size=10)
        arcade.draw_text("of sizes 2, 3, 4\n and 1 of sizes 5, 7. To",
                         start_x=530, start_y=310, font_size=10)
        arcade.draw_text("place the boats you will always have to",
                         start_x=530, start_y=290, font_size=10)
        arcade.draw_text("click the starting square, followed by its",
                         start_x=530, start_y=270, font_size=10)
        arcade.draw_text("ending square. You only have the option to",
                         start_x=530, start_y=250, font_size=10)
        arcade.draw_text("place boats horizontally or vertically (not",
                         start_x=530, start_y=230, font_size=10)
        arcade.draw_text("diagonally). Please be aware that the ships",
                         start_x=530, start_y=210, font_size=10)
        arcade.draw_text("are not allowed to overlap one another and",
                         start_x=530, start_y=190, font_size=10)
        arcade.draw_text("are not allowed to partially leave the grid.",
                         start_x=530, start_y=170, font_size=10)

        self.image1 = arcade.load_texture("../img/tuto1.png")
        arcade.draw_texture_rectangle(300, 230, 300,
                                      300, self.image1)
        self.manager.draw()

#Second time of tutorial screen (when user clicks 'next' button)
class Tutorial2(arcade.View):
    """ Class to manage the game over view """

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="TUTORIAL:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future", x=110, y=380)
        self.manager.add(ui_text_label.with_space_around(bottom=350))

        x_b = 100
        y_b = 30

        texture_back = arcade.load_texture(
            ":resources:onscreen_controls/flat_dark/left.png")
        back_button = arcade.gui.UITextureButton(
            texture=texture_back, x=x_b, y=y_b)
        self.manager.add(back_button.with_space_around(bottom=20))

        texture_advance = arcade.load_texture(
            ":resources:onscreen_controls/flat_dark/right.png")
        advance_button = arcade.gui.UITextureButton(
            texture=texture_advance, x=x_b+600, y=y_b)
        self.manager.add(advance_button.with_space_around(bottom=20))

        # What happens when user clicks button

        @back_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = TutorialView()
            self.window.show_view(menu_view)

        @advance_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = Tutorial3()
            self.window.show_view(menu_view)

        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    #Drawing on screen refreash
    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("Once you have placed all 8 ships correctly, the fun",
                         start_x=530, start_y=350, font_size=10)
        arcade.draw_text("can begin! You will now take turns with the AI to",
                         start_x=530, start_y=330, font_size=10)
        arcade.draw_text("shoot at each other’s grids. The user always gets to",
                         start_x=530, start_y=310, font_size=10)
        arcade.draw_text("shoot first. To shoot at the opponents grid, simply",
                         start_x=530, start_y=290, font_size=10)
        arcade.draw_text("click on their grid (“Enemy Waters”). After having",
                         start_x=530, start_y=270, font_size=10)
        arcade.draw_text("shot at a certain square, its colour changes. Here",
                         start_x=530, start_y=250, font_size=10)
        arcade.draw_text("is the meaning of the different colours used in our",
                         start_x=530, start_y=230, font_size=10)
        arcade.draw_text("game: light blue: unshot square; dark blue: shot",
                         start_x=530, start_y=210, font_size=10)
        arcade.draw_text("a ship has been hit; dark red: shot square where a",
                         start_x=530, start_y=190, font_size=10)
        arcade.draw_text("ship has been sunk. Please be aware that you can",
                         start_x=530, start_y=170, font_size=10)
        arcade.draw_text("only shoot at every square once during the game.",
                         start_x=530, start_y=150, font_size=10)

        self.image2 = arcade.load_texture("../img/tuto2.png")
        arcade.draw_texture_rectangle(300, 260, 400, 240, self.image2)

        self.manager.draw()

#Third and final screen of the tutorial (final instructions)
class Tutorial3(arcade.View):
    """ Class to manage the game over view """

    def on_show_view(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text="TUTORIAL:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future", x=110, y=380)
        self.manager.add(ui_text_label.with_space_around(bottom=350))

        x_b = 50
        y_b = 20

        texture_back = arcade.load_texture(
            ":resources:onscreen_controls/flat_dark/left.png")
        back_button = arcade.gui.UITextureButton(
            texture=texture_back, x=x_b, y=y_b)
        self.manager.add(back_button.with_space_around(bottom=20))

        # Handle Clicks

        @back_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = Tutorial2()
            self.window.show_view(menu_view)

        menu_button = arcade.gui.UIFlatButton(
            text="MENU", style=default_style, x=x_b+650, y=y_b+20, width=90)
        self.manager.add(menu_button)

        @menu_button.event("on_click")
        def on_click_flatbutton(event):
            menu_view = MenuView()
            self.window.show_view(menu_view)
    
    # Drawing screen every time it refreashes
    def on_draw(self):
        """ Draw the game over view """
        self.clear()
        arcade.draw_text("The game ends once one of the players has",
                         start_x=530, start_y=350, font_size=10)
        arcade.draw_text("been able to sink all their opponents ships",
                         start_x=530, start_y=330, font_size=10)
        arcade.draw_text("successfully. You then have the option to",
                         start_x=530, start_y=310, font_size=10)
        arcade.draw_text("either play again (which we highly recommend)",
                         start_x=530, start_y=290, font_size=10)
        arcade.draw_text("or close the game by clicking on the “X” in",
                         start_x=530, start_y=270, font_size=10)
        arcade.draw_text("the top right corner.", start_x=530,
                         start_y=250, font_size=10)

        self.image3 = arcade.load_texture("../img/tuto3.png")
        arcade.draw_texture_rectangle(300, 250, 400, 240, self.image3)

        self.manager.draw()

#Screen that allows us to set the different types of difficulty
class SettingsDifficultyView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""

        arcade.set_background_color(arcade.color.BLACK)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        ui_text_label = arcade.gui.UITextArea(text="DIFFICULTY:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        text = " \n" \
               "Choose one mode to play: \n\n" \
               "EASY - Great for beginners! \n\n" \
               "MEDIUM - Good challenge for experienced players!\n\n"\
               "HARD - Almost impossible to beat!\n\n"
        ui_text_label = arcade.gui.UITextArea(text=text,
                                              width=550,
                                              height=180,
                                              font_size=12,
                                              font_name="Arial")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        # Create a simple button
        easy_button = arcade.gui.UIFlatButton(
            text="EASY", width=200, style=default_style)
        self.v_box.add(easy_button.with_space_around(bottom=20))

        medium_button = arcade.gui.UIFlatButton(
            text="MEDIUM", width=200, style=default_style)
        self.v_box.add(medium_button.with_space_around(bottom=20))

        hard_button = arcade.gui.UIFlatButton(
            text="HARD", width=200, style=default_style)
        self.v_box.add(hard_button.with_space_around(bottom=20))

        # Handle Clicks
        @easy_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            game_view = SettingsView()
            # set the difficulty in a global variable
            self.window.show_view(game_view)

        @medium_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            game_view = SettingsView()
            self.window.show_view(game_view)

        @hard_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            game_view = SettingsView()
            self.window.show_view(game_view)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        self.manager.draw()

#Screen that allows to change the music settings (volume and music style)
class SettingsMusicView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""

        arcade.set_background_color(arcade.color.BLACK)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Text label
        ui_text_label = arcade.gui.UITextArea(text="Music:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=90))

        #music buttons positioning
        x_b = 140
        y_b = 312

        #IFlatButton
        m1_button = arcade.gui.UIFlatButton(
            x=x_b, y=y_b, text="MUSIC 1", width=200, style=default_style)
        self.manager.add(m1_button.with_space_around(bottom=20))

        m2_button = arcade.gui.UIFlatButton(
            x=x_b+220, y=y_b, text="MUSIC 2", width=200, style=default_style)
        self.manager.add(m2_button.with_space_around(bottom=20))

        m3_button = arcade.gui.UIFlatButton(
            x=x_b+440, y=y_b, text="MUSIC 3", width=200, style=default_style)
        self.manager.add(m3_button.with_space_around(bottom=20))

        ui_text_label = arcade.gui.UITextArea(text="Volume:",
                                              width=600,
                                              height=35,
                                              font_size=24,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=20))

        ui_slider = UISlider(value=50, width=300, height=50)
        self.v_box.add(ui_slider)

        # When user clicks button
        @m1_button.event("on_click")
        def on_click_flatbutton(event):

            global my_music, cur_song_index, my_music, media_player, songs

            my_music.stop(media_player)
            ui_slider.value = 50
            cur_song_index = 0
            my_music = arcade.load_sound(songs[cur_song_index])
            media_player.volume = 0.5
            media_player = my_music.play(volume=0.5, loop=True)

        @m2_button.event("on_click")
        def on_click_flatbutton(event):

            global my_music, cur_song_index, my_music, media_player, songs

            my_music.stop(media_player)
            ui_slider.value = 50
            cur_song_index = 1
            my_music = arcade.load_sound(songs[cur_song_index])
            media_player.volume = 0.5
            media_player = my_music.play(volume=0.5, loop=True)

        @m3_button.event("on_click")
        def on_click_flatbutton(event):

            global my_music, cur_song_index, my_music, media_player, songs

            my_music.stop(media_player)
            ui_slider.value = 50
            cur_song_index = 2
            my_music = arcade.load_sound(songs[cur_song_index])
            media_player.volume = 0.5
            media_player = my_music.play(volume=0.5, loop=True)

        @ui_slider.event()
        def on_change(event: UIOnChangeEvent):
            global media_player
            media_player.volume = 0.01*ui_slider.value

        self.v_box.add(UIAnchorWidget(child=ui_slider))

        #UIFlatButton
        menu_button = arcade.gui.UIFlatButton(
            text="MENU", style=default_style, width=90)
        self.v_box.add(menu_button.with_space_around(bottom=20))

        #Clicks
        @menu_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            game_view = SettingsView()
            self.window.show_view(game_view)

        #Center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        self.manager.draw()

#Overall settings screen
class SettingsView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show_view(self):
        """ Called when switching to this view"""

        arcade.set_background_color(arcade.color.BLACK)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a text label
        ui_text_label = arcade.gui.UITextArea(text="SETTINGS:",
                                              width=600,
                                              height=55,
                                              font_size=24,
                                              font_name="Kenney Future")
        self.v_box.add(ui_text_label.with_space_around(bottom=0))

        #UIFlatButton
        settings_d_button = arcade.gui.UIFlatButton(
            text="DIFFICULTY", width=200, style=default_style)
        self.v_box.add(settings_d_button.with_space_around(bottom=20))

        settings_m_button = arcade.gui.UIFlatButton(
            text="MUSIC", width=200, style=default_style)
        self.v_box.add(settings_m_button.with_space_around(bottom=20))

        menu_button = arcade.gui.UIFlatButton(
            text="MENU", style=default_style, width=90)
        self.v_box.add(menu_button.with_space_around(bottom=20))

        # What happens when user clicks button

        @settings_d_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            view = SettingsDifficultyView()
            self.window.show_view(view)

        @settings_m_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            view = SettingsMusicView()
            self.window.show_view(view)

        @menu_button.event("on_click")
        def on_click_flatbutton(event):
            self.manager.disable()
            game_view = MenuView()
            self.window.show_view(game_view)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        """ Draw the menu """
        self.clear()
        self.manager.draw()

    """ Class to manage the game over view """

#Game over screen
class EndView(arcade.View):
    """ Class that manages the 'menu' view. """

    def __init__(self, winner):
        self.you_won = 0
        super().__init__()
        if (winner == 'Player'):
            self.you_won = 1

    def on_show_view(self):
        """ Called when switching to this view"""

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        #vertical BoxGroup to align buttons

        self.background = arcade.load_texture("../img/back.png")

        self.v_box = arcade.gui.UIBoxLayout()

        #text label
        self.text = "CONGRATULATIONS, YOU WON!"
        if (self.you_won):
            ui_text_label = arcade.gui.UITextArea(text="CONGRATULATIONS, YOU WON!",
                                                  x=130,
                                                  y=295,
                                                  width=884,
                                                  height=90,
                                                  font_size=25,
                                                  font_name="Kenney Future")

        else:
            self.text = "COMMISERATIONS, COMPUTER WON!"
            ui_text_label = arcade.gui.UITextArea(text="COMMISERATIONS, YOU LOST!",
                                                  x=130,
                                                  y=295,
                                                  width=884,
                                                  height=90,
                                                  font_size=25,
                                                  font_name="Kenney Future")

        self.manager.add(ui_text_label)

        #Coordinates in which to draw
        x_b = 14
        y_b = 30

        #UIFlatButton
        play_button = arcade.gui.UIFlatButton(
            x=x_b, y=y_b, text="PLAY AGAIN", width=200, style=default_style)
        self.manager.add(play_button)

        quit_button = arcade.gui.UIFlatButton(
            x=x_b + 650, y=y_b, text="QUIT", width=200, style=default_style)
        self.manager.add(quit_button)

        # What happens when user clicks button

        @play_button.event("on_click")
        def on_click_texture_button(event):
            self.manager.disable()
            menu_view = MenuView()
            self.window.show_view(menu_view)

        @quit_button.event("on_click")
        def on_click_flatbutton(event):
            arcade.exit()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(
            anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_rectangle_filled(
            410, 368,  width=994,  height=70, color=arcade.color.BLACK)

        self.manager.draw()

'''

Main game view (actual game)

It has two main steps:

PLACING THE BOATS: shows only one central grid

SHOOTING AT THE ENEMY'S GRID AND ENEMY SHOOTING AT YOUR GRID: shows two grids, side by side

'''

class GameView(arcade.View):

    def __init__(self, player, enemy):

        super().__init__()
        self.place_boats = True
        self.boats_to_place = []
        self.start_click = True
        self.x_b = 0
        self.y_b = 0
        self.game_over = False
        self.winner = ""
        self.boat_size_list = player.get_boat_size_list()
        self.current_boat = 0
        self.player = player
        self.enemy = enemy
        self.player_grid = player.get_grid()
        self.enemy_grid = enemy.get_grid()
        self.texture_h = []
        self.texture_v = []
        self.boat_list = []
        #Names of graphical files to retrieve from secondary storage
        img_files_h = ['7h', '5h', '4h', '3h', '2h']
        img_files_v = ['7v', '5v', '4v', '3v', '2v']

        #Maps boat sizes to a list index
        self.dic_text = {7: 0, 5: 1, 4: 2, 3: 3, 2: 4}

        #Retrieves images of horizontal boats
        for img in img_files_h:
            self.texture_h.append(
                arcade.load_texture("../img/" + img + ".png"))

        #Retrieves images of vertical boats
        for img in img_files_v:
            self.texture_v.append(
                arcade.load_texture("../img/" + img + ".png"))

        #Retrives explosion image
        self.texture_e = arcade.load_texture("../img/explosion.png")

    def on_show_view(self):
        """ Called when switching to this view"""
        
        #Set background
        arcade.set_background_color(arcade.color.BLACK)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

    def on_draw(self):

        self.clear()
        self.manager.draw()

        #Checks if boats are already placed, if not, shows the place boats screen
        if (self.place_boats):
            for row in range(len(self.player_grid)):
                for column in range(len(self.player_grid[0])):
                    # Figure out what color to draw each square
                    if self.start_click == False and column == self.x_b and row == self.y_b:
                        color = arcade.color.ORANGE_RED
                    elif self.player_grid[row][column].get_value() == 1:
                        color = arcade.color.DEEP_SKY_BLUE
                    elif self.player_grid[row][column].get_value() == 2:
                        color = arcade.color.BABY_BLUE
                    elif self.player_grid[row][column].get_value() == 3:
                        color = arcade.color.RED_ORANGE
                    elif self.player_grid[row][column].get_value() == 4:
                        color = arcade.color.RED_DEVIL
                    else:
                        color = arcade.color.BABY_BLUE

                    # Coordinates of each square
                    x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2 + 200
                    y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2

                    # Draw the square
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

            #Draw boats
            for i, boat in enumerate(self.boat_list):
                if boat.direction == 1:
                    s = boat.size
                    bottom_left_x = 42*min(boat.begin_x, boat.end_x)+202
                    bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                    texture = self.texture_v[self.dic_text[s]]
                    width = 40
                    height = 41 * int(s) + (2-int(self.dic_text[s]))
                    arcade.draw_lrwh_rectangle_textured(
                        bottom_left_x, bottom_left_y, width, height, texture)
                else:
                    s = boat.size
                    bottom_left_x = 42*min(boat.begin_x, boat.end_x)+202
                    bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                    texture = self.texture_h[self.dic_text[s]]
                    width = 41 * int(s) + (2-int(self.dic_text[s]))
                    height = 40
                    arcade.draw_lrwh_rectangle_textured(
                        bottom_left_x, bottom_left_y, width, height, texture)

            #Draw text to show user which boat they must place
            arcade.draw_text(f"Place a boat of size {self.boat_size_list[self.current_boat]}:", font_name='Kenney Future',
                             font_size=15, bold=True, anchor_x="left", anchor_y="top", start_x=255, start_y=445, color=arcade.color.PEACH_YELLOW)

            return

        # Draw the grid
        # & what happens when we computer shots our field
        my_explosion_list = []
        for row in range(len(self.player_grid)):
            for column in range(len(self.player_grid[0])):

                # Calculate coordinates
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2

                # Square colors
                if self.player_grid[row][column].get_value() == 1:
                    color = arcade.color.OCEAN_BOAT_BLUE
                elif self.player_grid[row][column].get_value() == 2:
                    color = arcade.color.BABY_BLUE
                elif self.player_grid[row][column].get_value() == 3:
                    color = arcade.color.RED_ORANGE
                    my_explosion_list.append((x-20, y-20))
                elif self.player_grid[row][column].get_value() == 4:
                    color = arcade.color.RED_DEVIL
                    my_explosion_list.append((x-20, y-20))
                else:
                    color = arcade.color.BABY_BLUE

                # Draw the square
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

        #Draw explosions
        enem_explosion_list = []
        enem_boat = self.enemy.boat_list
        # what happens when we click enemys field
        for row in range(len(self.enemy_grid)):
            for column in range(len(self.enemy_grid)):

                #Coordinates
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2 + 450
                y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2

                #Determine color
                if self.enemy_grid[row][column].get_value() == 1:
                    color = arcade.color.OCEAN_BOAT_BLUE
                elif self.enemy_grid[row][column].get_value() == 2:
                    color = arcade.color.BABY_BLUE
                elif self.enemy_grid[row][column].get_value() == 3:
                    color = arcade.color.RED_ORANGE
                    enem_explosion_list.append((x-20, y-20))
                elif self.enemy_grid[row][column].get_value() == 4:
                    color = arcade.color.RED_DEVIL
                    enem_explosion_list.append((x-20, y-20))

                else:
                    color = arcade.color.BABY_BLUE

                # Draw the square
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
        
        #Draw boats
        for i, boat in enumerate(self.boat_list):
            if boat.direction == 1:
                s = boat.size
                bottom_left_x = 42*min(boat.begin_x, boat.end_x)+2
                bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                texture = self.texture_v[self.dic_text[s]]
                width = 40
                height = 41 * int(s) + (2-int(self.dic_text[s]))
                arcade.draw_lrwh_rectangle_textured(
                    bottom_left_x, bottom_left_y, width, height, texture)
            else:
                s = boat.size
                bottom_left_x = 42*min(boat.begin_x, boat.end_x)+2
                bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                texture = self.texture_h[self.dic_text[s]]
                width = 41 * int(s) + (2-int(self.dic_text[s]))
                height = 40
                arcade.draw_lrwh_rectangle_textured(
                    bottom_left_x, bottom_left_y, width, height, texture)

        for i, explosion in enumerate(my_explosion_list):
            arcade.draw_lrwh_rectangle_textured(
                explosion[0], explosion[1], WIDTH, HEIGHT, self.texture_e)

        for i, boat in enumerate(enem_boat):
            if boat.sunk:
                if boat.direction == 1:
                    s = boat.size
                    bottom_left_x = 42*min(boat.begin_x, boat.end_x)+452
                    bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                    texture = self.texture_v[self.dic_text[s]]
                    width = 40
                    height = 41 * int(s) + (2-int(self.dic_text[s]))
                    arcade.draw_lrwh_rectangle_textured(
                        bottom_left_x, bottom_left_y, width, height, texture)
                else:
                    s = boat.size
                    bottom_left_x = 42*min(boat.begin_x, boat.end_x)+452
                    bottom_left_y = min(boat.begin_y, boat.end_y)*42+2
                    texture = self.texture_h[self.dic_text[s]]
                    width = 41 * int(s) + (2-int(self.dic_text[s]))
                    height = 40
                    arcade.draw_lrwh_rectangle_textured(
                        bottom_left_x, bottom_left_y, width, height, texture)

        for i, explosion in enumerate(enem_explosion_list):
            arcade.draw_lrwh_rectangle_textured(
                explosion[0], explosion[1], WIDTH, HEIGHT, self.texture_e)

        if not self.game_over:
            arcade.draw_text("Friendly Waters", font_name='Kenney Future', font_size=15, bold=True,
                             anchor_x="left", anchor_y="top", start_x=75, start_y=445, color=arcade.color.PEACH_YELLOW)
            arcade.draw_text("Enemy Waters", font_name='Kenney Future', font_size=15, bold=True,
                             anchor_x="left", anchor_y="top", start_x=555, start_y=445, color=arcade.color.PEACH_YELLOW)
        else:
            self.on_game_over()

    #Action when user clicks with the mouse
    def on_mouse_press(self, x, y, button, modifiers):
        #If the click is off the grid just ignore it
        if (x >= 871 or y >= 420 or (420 <= x <= 450)) and not self.place_boats:
            return
        """
        Called when the user presses a mouse button.
        """
        #If the game is over just returns
        if self.game_over:
            return

        # Change the x/y screen coordinates to grid coordinates

        '''
        GAME MECHANICS: user clicks one time to select the beginning square and click once again to select the
        square where the boat ends. If the clicks do not allow to place a boat of the demanded size, just return
        '''
        if self.place_boats:
            column = (x-200) // (WIDTH + MARGIN)
            row = y // (HEIGHT + MARGIN)

            if self.start_click:
                self.x_b = column
                self.y_b = row
                self.start_click = False

            else:

                #Place the boat on the grid if possible
                
                boat = Boat(self.x_b, column, self.y_b, row, self.player_grid,
                            True, self.boat_size_list[self.current_boat])
                self.start_click = True
                if (not boat.get_invalid()) and self.player.place_boat(boat):
                    self.current_boat += 1

                    self.boat_list.append(boat)

                    if (self.current_boat == len(self.boat_size_list)):
                        self.place_boats = False
                        return

            return

        column = 0
        row = 0

        #Determine if we are clicking on the first of second grid
        if x < 425:
            column = x // (WIDTH + MARGIN)
            row = y // (HEIGHT + MARGIN)
        else:
            column = (x-450) // (WIDTH + MARGIN)
            row = y // (HEIGHT + MARGIN)

        if x >= 425:
            #Shoots and check victory for both sides

            valid = self.enemy.shoot((row, column))

            if self.enemy.check_victory():
                self.game_over = True
                self.winner = "Player"
                return

            if valid:
                self.player.shoot_pc()

            if self.player.check_victory():
                self.game_over = True
                self.winner = "Computer"
                return

    def on_game_over(self):
        self.manager.disable()
        end_view = EndView(self.winner)
        self.window.show_view(end_view)

#Starts user interface
def main():
    """ Startup """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,
                           "BATTLESHIP - BRALUX")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
