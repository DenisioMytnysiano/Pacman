from dataclasses import dataclass

from game.states.game_state import GameState


@dataclass(eq=False)
class ReflexState:
    game_state: GameState
    agent: int = 0
    depth: int = 0

    @property
    def action(self) -> int:
        return self.game_state.get_last_action()