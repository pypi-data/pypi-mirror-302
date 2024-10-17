import pygame
from minigrid.manual_control import ManualControl
from .env import make_grid_adventure
from .agent import GridAdventureAgent


def evaluate(agent: GridAdventureAgent):
    env = make_grid_adventure(render_mode="human")
    done = False
    observation, _ = env.reset()

    while not done:
        action = agent.act(observation)
        observation, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                break

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(int(event.key))
                if key == 'escape':
                    env.close()
                    return


def run_manual():
    env = make_grid_adventure(render_mode='human', with_wrapper=False)
    env = ManualControl(env)
    env.start()
