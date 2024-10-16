"""A collection of styles that work with any theme and are imported upon initialization of the token_interface module"""

from token_interface.token_studio_interface import Color, add_alpha, DropShadow, BoxShadow

black = Color("#000000")
white = Color("#FFFFFF")

shadow_1 = DropShadow(add_alpha(black, 30), 0, 1, 2, 0)
shadow_2 = DropShadow(add_alpha(black, 15), 0, 1, 3, 1)
shadow_3 = DropShadow(add_alpha(black, 15), 0, 2, 6, 2)
shadow_4 = DropShadow(add_alpha(black, 15), 0, 4, 8, 2)
shadow_5 = DropShadow(add_alpha(black, 30), 0, 1, 3, 0)
shadow_6 = DropShadow(add_alpha(black, 15), 0, 6, 10, 4)
shadow_7 = DropShadow(add_alpha(black, 30), 0, 2, 3, 0)
shadow_8 = DropShadow(add_alpha(black, 15), 0, 8, 12, 6)
shadow_9 = DropShadow(add_alpha(black, 30), 0, 4, 4, 0)

class CoreStyles:
    black = black
    white = white
    elevation_1 = BoxShadow(shadow_1, shadow_2)
    elevation_2 = BoxShadow(shadow_1, shadow_3)
    elevation_3 = BoxShadow(shadow_4, shadow_5)
    elevation_4 = BoxShadow(shadow_6, shadow_7)
    elevation_5 = BoxShadow(shadow_8, shadow_9)
