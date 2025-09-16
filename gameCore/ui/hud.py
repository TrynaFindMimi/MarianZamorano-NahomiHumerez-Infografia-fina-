import arcade
from util.gameState import GameState

HUD_Y = 710
BUTTON_X = 700
BUTTON_Y = HUD_Y
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 30

def draw_hud(score, lives, level, score_to_advance):
    arcade.draw_text(f"Score: {score}", 30, HUD_Y, arcade.color.WHITE, 18)
    arcade.draw_text(f"Lives: {lives}", 200, HUD_Y, arcade.color.WHITE, 18)
    arcade.draw_text(f"Level: {level}", 350, HUD_Y, arcade.color.WHITE, 18)
    arcade.draw_text(f"Goal: {score_to_advance}", 470, HUD_Y, arcade.color.LIGHT_GRAY, 16)

    if GameState.ready_for_next_level:
        arcade.draw_lrbt_rectangle_filled(
            BUTTON_X,
            BUTTON_X + BUTTON_WIDTH,
            BUTTON_Y,
            BUTTON_Y + BUTTON_HEIGHT,
            arcade.color.DARK_GREEN
        )
        arcade.draw_text("Siguiente Nivel", BUTTON_X + 20, BUTTON_Y + 5, arcade.color.WHITE, 16)

def check_next_level_click(x, y):
    if not GameState.ready_for_next_level:
        return False
    return BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT
