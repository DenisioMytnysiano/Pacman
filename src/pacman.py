import sys
from agents.agent import Agent
from game.components import layout
from game.components.layout import Layout
from game.rules.game_rules import ClassicGameRules
from graphics.pacman_graphics import PacmanGraphics

def setup_game():

    args = dict()
    args['layout'] = layout.get_layout("originalClassic")
    pacman_type = load_agent("KeyboardAgent")
    pacman = pacman_type()
    args['pacman'] = pacman

    ghost_type = load_agent("RandomGhost")
    args['ghosts'] = [ghost_type(i + 1) for i in range(4)]

    from graphics import pacman_graphics
    args['display'] = pacman_graphics.PacmanGraphics(frame_time=0.1)

    return args


def load_agent(agent_name: str, no_graphics: bool = False):
    try:
        module = __import__("agents")
        if no_graphics and agent_name == 'KeyboardAgent':
            raise Exception('Using the keyboard agent requires graphics (not text display)')
        return getattr(module, agent_name)
    except ImportError:
        raise Exception(f'The agent {agent_name} cannot be found in /agents directory')


def run_game(layout: Layout, pacman: Agent, ghosts: list[Agent],
             display: PacmanGraphics, timeout: int = 30):

    rules = ClassicGameRules(timeout)
    game_display = display
    rules.quiet = False
    game = rules.new_game(layout, pacman, ghosts, game_display)
    game.run()
    score = game.state.get_score()
    print(f'Score:{score}')


if __name__ == '__main__':
    setup = setup_game()
    run_game(**setup)
