class GameState:
    score = 0
    lives = 3
    level = 1
    score_to_advance = 1500
    ready_for_next_level = False

    @staticmethod
    def reset_for_level(level):
        GameState.level = level
        GameState.score = 0
        GameState.lives = 3
        GameState.ready_for_next_level = False
        GameState.score_to_advance = 1500 + (level - 1) * 500

    @staticmethod
    def add_score(points):
        GameState.score = max(0, GameState.score + points)

    @staticmethod
    def check_level_completion():
        if GameState.score >= GameState.score_to_advance:
            GameState.ready_for_next_level = True

    @staticmethod
    def next_level():
        GameState.level += 1
        GameState.reset_for_level(GameState.level)