from dataclasses import dataclass
from agents.agent import Agent
from game.components.layout import Layout
from game import Game
from game.states.game_state import GameState
from graphics.pacman_graphics import PacmanGraphics

COLLISION_TOLERANCE = 0.7


@dataclass
class ClassicGameRules:

    timeout: int = 30

    def new_game(self, layout: Layout, pacman_agent: Agent, ghost_agents: list[Agent], display: PacmanGraphics, quiet=False):
        agents = [pacman_agent] + ghost_agents[:layout.num_ghosts]
        init_state = GameState()
        init_state.initialize(layout, len(ghost_agents))
        game = Game(agents, display, self)
        game.state = init_state
        self.initial_state = init_state.deep_copy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        if state.is_win():
            self.win(state, game)
        if state.is_lose():
            self.lose(state, game)

    def win(self, state, game):
        if not self.quiet:
            print("Pacman emerges victorious! Score: %d" % state.data.score)
        game.game_over = True

    def lose(self, state, game):
        if not self.quiet:
            print("Pacman died! Score: %d" % state.data.score)
        game.game_over = True




