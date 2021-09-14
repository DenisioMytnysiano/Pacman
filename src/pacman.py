import sys
from agents.agent import Agent
from game.components import layout
from game.components.layout import Layout
from game.rules.game_rules import ClassicGameRules
from graphics.pacman_graphics import PacmanGraphics
from utils.maze_generator import MazeGenerator


def get_size(size):
    return [int(x) for x in size.split("x")]


def setup_game(cli_args):
    from optparse import OptionParser
    args = dict()
    parser = OptionParser()
    parser.add_option("--generate", dest="generate_maze", default=False,
                      help="Whether to generate maze")
    parser.add_option('--generated-size', dest='gen_size',
                      help='Size of generated maze', default='20x10')
    parser.add_option('--ghosts-generated', dest='num_ghosts',
                      help='How many ghosts to generate', default=1)
    options, other_junk = parser.parse_args(cli_args)
    if options.generate_maze:
        file_name = "generatedMaze"
        height, width = get_size(options.gen_size)
        MazeGenerator.generate(height, width, int(options.num_ghosts), file_name)
        args['layout'] = layout.get_layout(file_name)
    else:
        args['layout'] = layout.get_layout("mediumClassic")
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
    setup = setup_game(sys.argv[1:])
    run_game(**setup)
