import gym
import numpy as np
from gym.envs.box2d.lunar_lander import LunarLanderContinuous, SCALE
from gym.envs.classic_control import rendering

class LunarLanderWithCoin(LunarLanderContinuous):
    def __init__(self):
        super().__init__()
        self.coin_position = None
        self.coin_collected = False
        self.coin_value = 500  # Reward value of the coin
        self.viewer = None  # To hold the viewer instance

    def reset(self):
        state = super().reset()
        self.place_coin()
        self.coin_collected = False
        return state

    def place_coin(self):
        # Place the coin at a random position within the screen bounds
        x = np.random.uniform(-1, 1) * SCALE
        y = (np.random.uniform(0, 1.2) + 0.2) * SCALE  # Adjust vertical offset
        self.coin_position = (x, y)

    def step(self, action):
        state, reward, done, info = super().step(action)
        
        # Check if lander is near the coin and collect it
        if not self.coin_collected:
            lander_pos = self.lander.position
            if np.linalg.norm(np.array([lander_pos.x, lander_pos.y]) - np.array(self.coin_position)) < 0.1 * SCALE:
                reward += self.coin_value
                self.coin_collected = True
                info['coin_collected'] = True
        
        return state, reward, done, info

    def render(self, mode='human'):
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(600, 400)

        # Call the parent render to draw the environment as usual
        result = super().render(mode)
        
        if not self.coin_collected:
            # Draw the coin
            coin = rendering.make_circle(0.05 * SCALE)
            coin_trans = rendering.Transform(translation=self.coin_position)
            coin.add_attr(coin_trans)
            coin.set_color(1.0, 0.84, 0)  # Gold color
            self.viewer.add_onetime(coin)
        
        return result

# Usage:
# env = LunarLanderWithCoin()
# state = env.reset()
# frames = []
# for _ in range(200):  # Example of running the environment
#     action = env.action_space.sample()
#     state, reward, done, info = env.step(action)
#     frames.append(env.render(mode='rgb_array'))
#     if done:
#         break
# env.close()

# # To save frames as an animated GIF
# save_rgb_animation(frames, "lunar_lander_with_coin.gif")


class LunarLanderWithCoin(LunarLanderContinuous):
    def __init__(self):
        super().__init__()
        self.coin_position = None
        self.coin_collected = False
        self.coin_value = 500  # Reward value of the coin

    def reset(self):
        state = super().reset()
        self.place_coin()
        self.coin_collected = False
        # Extend the state to include coin position
        return np.append(state, self.normalize_position(self.coin_position))

    def place_coin(self):
        # Place the coin at a random position within the screen bounds
        x = np.random.uniform(-1, 1)  # Adjust range as per the environment's scale
        y = np.random.uniform(0, 1.2)  # Adjust range as per the environment's scale
        self.coin_position = (x, y)

    def step(self, action):
        state, reward, done, info = super().step(action)
        
        # Check if lander is near the coin and collect it
        if not self.coin_collected:
            lander_pos = state[:2]  # Assuming state contains x, y coordinates in the first two indices
            if np.linalg.norm(np.array(lander_pos) - np.array(self.coin_position)) < 0.1:  # Check proximity
                reward += self.coin_value
                self.coin_collected = True
                info['coin_collected'] = True
        
        # Extend the state to include coin position if not collected
        if not self.coin_collected:
            extended_state = np.append(state, self.normalize_position(self.coin_position))
        else:
            # Append placeholder values if coin is collected
            extended_state = np.append(state, [-1, -1])  # Indicates coin is collected

        return extended_state, reward, done, info

    def normalize_position(self, position):
        # Normalize the position based on environment scale
        return [position[0] / self.x_threshold, position[1] / self.y_threshold]  # Adjust normalization as needed

    def render(self, mode='human'):
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(600, 400)

        # Call the parent render to draw the environment as usual
        result = super().render(mode)
        
        if not self.coin_collected:
            # Draw the coin
            coin = rendering.make_circle(0.05 * SCALE)
            coin_trans = rendering.Transform(translation=(self.coin_position[0]*SCALE, self.coin_position[1]*SCALE))
            coin.add_attr(coin_trans)
            coin.set_color(1.0, 0.84, 0)  # Gold color
            self.viewer.add_onetime(coin)
        
        return result
    

