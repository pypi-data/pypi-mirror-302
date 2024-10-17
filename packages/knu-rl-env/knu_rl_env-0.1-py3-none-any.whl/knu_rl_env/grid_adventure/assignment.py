import pygame
from .agent import Agent
from .env import GridAdventureEnv


def _wait_for_keypress():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
                key = pygame.key.name(int(event.key))
                if key == "escape":
                    return True


def do_assignment(agent: Agent):
    env = GridAdventureEnv(render_mode='human')
    observation, _ = env.reset()
    agent.reset()

    while True:
        action = agent.act(observation)
        observation, reward, terminated, truncated, _ = env.step(action)
        env.render()

        if terminated or truncated:
            if _wait_for_keypress():
                pygame.quit()
                quit()
                env.close()
