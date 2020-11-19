import random
import numpy as np

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Convolution2D, Dropout, Activation, Flatten, Input
from tensorflow.keras.utils import plot_model

class Agent():

    def __init__(
                self,
                gamma=0.9,
                epsilon=1,
                num_training_games=10000,
                memory_size=500,
                board_size=(20, 10),
                saved_model_name="",
                verbose=0,
                epsilon_decrement = True
                ):

        """
        gamma: discount factor for future rewards, [0 , 1]
            0 for not accounting for future rewards at all
            1 for weighting future rewards equal to current rewards

        epsilon: exploration vs exploitation, [0, 1]
            0 for always choosing best known option
            1 for choosing random options

        num_traing_games: How many games should be spent traing
        before utilizing optimal learned strategy

        memory_size: Amount of training episodes that should be stored in memory

        board_size [tuple(x, y)]: dimension of tetris board matrix

        saved_model_name: Path to a previously saved keras_model,
        if blank a new model is created
        """
        self.gamma = gamma
        self.epsilon = epsilon
        self._num_training_games = num_training_games
        self._max_memory_size = memory_size
        self._mem_index = 0
        self._state_size = board_size
        self.verbose = verbose

        # Memory saves episodes in form [board_matrix, reward (int)]
        # empty_board_matrix = [[0 for _ in range(board_size[0])] for _ in range(board_size[1])]
        # np.array([[np.array([0, 0, 0]), 0, False] for _ in range(memory_size)], dtype=object)
        self._memory_actions = np.zeros((memory_size, 3))
        self._memory_rewards = np.array([[0, False] for _ in range(memory_size)], dtype=object)
        self._filled_memory = False

        if epsilon_decrement:
            self._epsilon_decrement = epsilon / num_training_games
        else:
            self._epsilon_decrement = 0

        if saved_model_name:
            self._model = keras.models.load_model('models/' + saved_model_name)
        else:
            self._model = self._build_model()


    def get_next_state(self, possible_next_states):
        if random.random() < self.epsilon:
            return random.randint(0, len(possible_next_states)-1)
        else:
            predicted_rewards = self._predict_rewards(possible_next_states)
            return np.argmax(predicted_rewards)


    def add_to_memory(self, action, reward, is_game_over):
        """
        Save an action and related reward to agents memory
        """

        self._memory_actions[self._mem_index] = np.array(action)
        self._memory_rewards[self._mem_index] = [reward, is_game_over]
        self._mem_index += 1
        if self._mem_index >= self._max_memory_size:
            self._mem_index %= self._max_memory_size
            self._filled_memory = True


    def clear_memory(self):
        self._filled_memory = False
        self._mem_index = 0

    def _build_model(self):
        """
        Create the internal neural network for prediciting values of various actions
        """
        # model = keras.Model(), model.Add()..., model.compile(), return model ish
        # Første lag må ha
        model = Sequential()

        model.add(Input(shape=(3,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))

        model.add(Dense(1, activation='linear'))


        model.compile(optimizer="adam", loss='mse')

        return model

    def train(self):
        """
        Train the neural network on a sample from the internal memory
        """

        if self.epsilon > 0:
            self.epsilon -= self._epsilon_decrement
        else:
            self.epsilon = 0

        sample_size = 50 # Set sample_size to 50

        if not self._filled_memory:
            sample_size = min(self._mem_index, sample_size)
            mem_upper_limit = self._mem_index
        else:
            mem_upper_limit = self._max_memory_size

        rewards_absvalue = np.abs(self._memory_rewards[:mem_upper_limit, 0])
        sample_probs = rewards_absvalue / sum(rewards_absvalue) # Normalize rewards to use as probability for choosing episode
        sample_probs = sample_probs.astype(np.float)

        sample_idx = np.random.choice(mem_upper_limit, sample_size, p=sample_probs, replace=False)
        sample_rewards = self._memory_rewards[sample_idx] # Use a random sample of the network for training
        actions = self._memory_actions[sample_idx] # Use a random sample of the network for training

        q_values = np.array([]) # Y_values for network
        for episode, index in zip(sample_rewards, sample_idx):
            reward = episode[0]
            is_game_over = episode[1]

            if is_game_over:
                q_values = np.append(q_values, reward)
            else:
                next_action = self._memory_actions[(index + 1) % self._max_memory_size]
                next_q = self._predict_rewards(next_action)
                q_value = reward + self.gamma * next_q
                q_values = np.append(q_values, q_value)

        self._model.fit(actions, q_values,
        batch_size=sample_size, epochs=100, verbose=self.verbose
        )

    def _predict_rewards(self, possible_next_states):
        """
        input: list of actions
        output: Predicted values for the actions
        """
        # possible_next_state = np.array([possible_next_states])
        if len(possible_next_states.shape) < 2:
            possible_next_states = np.expand_dims(possible_next_states, axis=(0))

        return self._model.predict(possible_next_states)

    def save_model(self, model_name, should_plot_model = False):
        print("Saving model...")
        self._model.save(filepath = 'models/' + model_name, overwrite = True)
        if should_plot_model:
            try:
                plot_model(self._model, to_file='models/visualizations/' + model_name+ '.png', show_shapes=True, show_layer_names=True)
            except Exception as e:
                print(f"Error in plot model: {e}. \n You can probably fix it by doing 'pip install pydot' and 'sudo apt install graphviz'")
        print("Saved.")
