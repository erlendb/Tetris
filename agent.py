import random
import numpy as np

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Convolution2D, Dropout, Activation, Flatten
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
                verbose=0
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

        # Memory saves episodes in form [board_matrix, reward (int), is_game_over (bool)]
        empty_board_matrix = [[0 for _ in range(board_size[0])] for _ in range(board_size[1])]
        self._memory = np.array([[empty_board_matrix, 0, False] for _ in range(memory_size)], dtype=object)
        self._filled_memory = False

        self._epsilon_decrement = epsilon / num_training_games

        if saved_model_name:
            self._model = keras.models.load_model('models/' + saved_model_name)
        else:
            self._model = self._build_model()


    def get_next_state(self, possible_next_states):
        if random.random() < self.epsilon:
            return random.randint(0, len(possible_next_states)-1)

        else:
            # best_reward = 0
            # best_action = 0
            predicted_rewards = self._predict_reward(possible_next_states)

            return np.argmax(predicted_rewards)
        #     for index, state in enumerate(possible_next_states):
        #         predicted_reward = self._predict_reward(state)
        #         if predicted_reward > best_reward:
        #             best_reward = predicted_reward
        #             best_action = index

        # return best_action

    def add_to_memory(self, action, reward, is_game_over):
        """
        Save an action and related reward to agents memory
        """

        self._memory[self._mem_index] = [action, reward, is_game_over]
        self._mem_index += 1
        if self._mem_index >= self._max_memory_size :
            self._mem_index %= self._max_memory_size
            self._filled_memory = True

    def _build_model(self):
        """
        Create the internal neural network for prediciting values of various actions
        """
        # model = keras.Model(), model.Add()..., model.compile(), return model ish
        # Første lag må ha
        model = Sequential()

        model.add(Convolution2D(8, 4, input_shape=(*self._state_size, 1))) #*self._state_size,
        model.add(Convolution2D(4, 3, input_shape=(*self._state_size, 1))) #*self._state_size,
        model.add(Flatten())
        model.add(Dense(4, activation='relu'))
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

        sample_size = 50 # Set sample_size to 200

        if not self._filled_memory:
            sample_size = min(self._mem_index, sample_size)
            mem_upper_limit = self._mem_index
        else:
            mem_upper_limit = self._max_memory_size

        rewards_absvalue = np.abs(self._memory[:mem_upper_limit, 1])
        sample_probs = rewards_absvalue / sum(rewards_absvalue) # Normalize rewards to use as probability for choosing episode
        sample_probs = sample_probs.astype(np.float)

        sample_idx = np.random.choice(mem_upper_limit, sample_size, p=sample_probs, replace=False)
        sample = self._memory[sample_idx]
        # sample = random.sample(self._memory, sample_size) # Train on a random sample of the memory

        actions = np.array( [np.array(episode[0]).reshape(self._state_size) for episode in sample] ) # X_values for network
        actions = np.expand_dims(actions, axis=3)

        q_values = np.array([]) # Y_values for network
        for episode, index in zip(sample, sample_idx):
            reward = episode[1]
            is_game_over = episode[2]

            if is_game_over:
                q_values = np.append(q_values, reward)
            else:
                next_episode = self._memory[(index + 1) % self._max_memory_size]
                next_q = self._predict_reward(next_episode[0])
                q_value = reward + self.gamma * next_q
                q_values = np.append(q_values, q_value)

        self._model.fit(actions, q_values,
        batch_size=sample_size, epochs=100, verbose=self.verbose
        )


    def _predict_reward(self, possible_next_state):
        """
        input: list of feature_values for current and next state
        output: Predicted value for the action
        """
        possible_next_state = np.array(possible_next_state)
        if len(possible_next_state.shape) == 2:
            possible_next_state = np.expand_dims(possible_next_state, axis=0) # Legg til en akse for antall inputs (1)
        possible_next_state = np.expand_dims(possible_next_state, axis=3) # Legg til en akse for bitdybde (1)
        return self._model.predict([possible_next_state])

    def save_model(self, model_name):
        print("Saving model...")
        self._model.save(filepath = 'models/' + model_name, overwrite = True)
        try:
            plot_model(self._model, to_file='models/visualizations/' + model_name+ '.png', show_shapes=True, show_layer_names=True)
        except Exception as e:
            print(f"Error in plot model: {e}. \n You can probably fix it by doing 'pip install pydot' and 'sudo apt install graphviz'")
        print("Saved.")
