from dataclasses import dataclass


@dataclass
class Game:

    def __init__(self, agents, display, rules, starting_index=0):
        self.agents = agents
        self.display = display
        self.rules = rules
        self.starting_index = starting_index
        self.game_over = False
        self.move_history = []
        self.num_moves = 0

    def run(self):

        self.display.initialize(self.state.data)
        agent_index = self.starting_index
        num_agents = len(self.agents)

        while not self.game_over:
            agent = self.agents[agent_index]
            observation = self.state.deep_copy()
            action = agent.get_action(observation)
            self.move_history.append((agent_index, action))
            self.state = self.state.generate_successor(agent_index, action)
            self.display.update(self.state.data)
            self.rules.process(self.state, self)
            if agent_index == num_agents + 1:
                self.num_moves += 1
            agent_index = (agent_index + 1) % num_agents
        self.display.finish()
