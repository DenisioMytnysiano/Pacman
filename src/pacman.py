import sys
from agents.agent import Agent
from game.components import layout
from game.components.layout import Layout
from game.rules.game_rules import ClassicGameRules
from graphics.pacman_graphics import PacmanGraphics


def default(string: str) -> str:
    return string + ' [Default: %default]'


def parse_agent_params(string: str) -> dict:
    if not string:
        return {}
    pieces = string.split(',')
    params = {}
    for piece in pieces:
        if '=' in piece:
            key, value = piece.split('=')
        else:
            key, value = piece, 1
        params[key] = value
    return params


def setup_game(argv):
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('-n', '--numGames', dest='numGames', type='int',
                      help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    parser.add_option('-l', '--layout', dest='layout',
                      help=default('the LAYOUT_FILE from which to load the map layout'),
                      metavar='LAYOUT_FILE', default='originalClassic')
    parser.add_option('-p', '--pacman', dest='pacman',
                      help=default('the agent TYPE in the pacmanAgents module to use'),
                      metavar='TYPE', default='KeyboardAgent')
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics',
                      help='Display output as text only', default=False)
    parser.add_option('-q', '--quietTextGraphics', action='store_true', dest='quietGraphics',
                      help='Generate minimal output and no graphics', default=False)
    parser.add_option('-g', '--ghosts', dest='ghost',
                      help=default('the ghost agent TYPE in the ghostAgents module to use'),
                      metavar='TYPE', default='DirectionalGhost')
    parser.add_option('-k', '--numghosts', type='int', dest='numGhosts',
                      help=default('The maximum number of ghosts to use'), default=4)
    parser.add_option('-z', '--zoom', type='float', dest='zoom',
                      help=default('Zoom the size of the graphics window'), default=1.0)
    parser.add_option('-r', '--recordActions', action='store_true', dest='record',
                      help='Writes game histories to a file (named by the time they were played)', default=False)
    parser.add_option('--replay', dest='gameToReplay',
                      help='A recorded game file (pickle) to replay', default=None)
    parser.add_option('-a', '--agentArgs', dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--numTraining', dest='numTraining', type='int',
                      help=default('How many episodes are training (suppresses output)'), default=0)
    parser.add_option('--frameTime', dest='frameTime', type='float',
                      help=default('Time to delay between frames; <0 means keyboard'), default=0.1)
    parser.add_option('--timeout', dest='timeout', type='int',
                      help=default('Maximum length of time an agent can spend computing in a single game'), default=30)

    options, other_junk = parser.parse_args(argv)
    if len(other_junk) != 0:
        raise Exception('Command line input not understood: ' + str(other_junk))
    args = dict()
    args['layout'] = layout.get_layout(options.layout)
    no_keyboard = options.gameToReplay is None and (options.textGraphics or options.quietGraphics)
    pacman_type = load_agent(options.pacman, no_keyboard)
    agent_opts = parse_agent_params(options.agentArgs)
    if options.numTraining > 0:
        args['numTraining'] = options.numTraining
        if 'numTraining' not in agent_opts:
            agent_opts['numTraining'] = options.numTraining
    pacman = pacman_type(**agent_opts)
    args['pacman'] = pacman

    if 'numTrain' in agent_opts:
        options.numQuiet = int(agent_opts['numTrain'])
        options.numIgnore = int(agent_opts['numTrain'])

    ghost_type = load_agent(options.ghost, no_keyboard)
    args['ghosts'] = [ghost_type(i + 1) for i in range(options.numGhosts)]

    from graphics import pacman_graphics
    args['display'] = pacman_graphics.PacmanGraphics(options.zoom, frame_time=options.frameTime)
    args['num_games'] = options.numGames
    args['timeout'] = options.timeout

    return args


def load_agent(agent_name: str, no_graphics: bool):
    try:
        module = __import__("agents")
        if no_graphics and agent_name == 'KeyboardAgent':
            raise Exception('Using the keyboard agent requires graphics (not text display)')
        return getattr(module, agent_name)
    except ImportError:
        raise Exception(f'The agent {agent_name} cannot be found in /agents directory')


def run_game(layout: Layout, pacman: Agent, ghosts: list[Agent],
             display: PacmanGraphics, num_games: int,
             num_training: int = 0, timeout: int = 30):

    rules = ClassicGameRules(timeout)
    games = []

    for i in range(num_games):
        be_quiet = i < num_training
        game_display = display
        rules.quiet = False
        game = rules.new_game(layout, pacman, ghosts, game_display, be_quiet)
        game.run()
        if not be_quiet:
            games.append(game)

    if num_games > num_training:
        scores = [game.state.get_score() for game in games]
        wins = [game.state.is_win() for game in games]
        win_rate = wins.count(True) / float(len(wins))
        print(f'Average Score:{sum(scores) / float(len(scores))}')
        print(f'Scores:{",".join([str(score) for score in scores])}')
        print(f'Win Rate:{wins.count(True)}/{len(wins)} ({win_rate}%)')

    return games


if __name__ == '__main__':
    setup = setup_game(sys.argv[1:])
    run_game(**setup)
