import copy
import time
from dataclasses import dataclass

from utils.logger import Logger


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
        self.elapsed = 0
        self.logger = Logger()

    def serialize(self):
        if self.game_over:
            result = {
                "is_win": self.state.is_win(),
                "time": self.elapsed,
                "score": self.state.get_score(),
                "agentType": type(self.agents[0]).__name__,
            }
            return result
        return None

    def run(self):

        self.display.initialize(self.state.data)
        agent_index = self.starting_index
        num_agents = len(self.agents)

        for agent in self.agents:
            if hasattr(agent, "register_state"):
                agent.register_state(self.state)

        start_time = time.time()
        while not self.game_over:
            agent = self.agents[agent_index]
            action = agent.get_action(copy.deepcopy(self.state))

            self.move_history.append((agent_index, action))
            self.state = self.state.generate_successor(agent_index, action)

            self.display.update(self.state.data)
            self.rules.process(self.state, self)

            if agent_index == num_agents + 1:
                self.num_moves += 1
            agent_index = (agent_index + 1) % num_agents

            for agent in self.agents:
                if hasattr(agent, "final"):
                    agent.final(self.state)

        self.elapsed = time.time() - start_time
        record = self.serialize()
        if record is not None:
            self.logger.save(record)
        self.display.finish()
