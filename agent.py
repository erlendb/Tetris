import random
import numpy as np

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Convolution2D, Dropout, Activation, Flatten

class Agent():

    def __init__(
                self,
                gamma=0.9,
                epsilon=1,
                num_training_games=10000,
                memory_size=5000,
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
        self._memory = []
        self._num_training_games = num_training_games
        self._max_memory_size = memory_size
        self._mem_index = 0
        self._state_size = board_size

        self._epsilon_decrement = epsilon / num_training_games

        if saved_model_name:
            self._model = keras.models.load_model('models/' + saved_model_name)
        else:
            self._model = self._build_model()

        self.verbose = verbose

    def get_next_state(self, possible_next_states):
        if random.random() < self.epsilon:
            return random.randint(0, len(possible_next_states)-1)

        else:
            best_reward = 0
            best_action = 0
            for index, state in enumerate(possible_next_states):
                predicted_reward = self._predict_reward(state)
                if predicted_reward > best_reward:
                    best_reward = predicted_reward
                    best_action = index

        return best_action

    def add_to_memory(self, action, reward, is_game_over):
        if reward == 1:
            return
        self._memory.append([action, reward, is_game_over, self._mem_index])
        self._mem_index += 1

        if self._mem_index > self._max_memory_size:
            self._memory = self._memory[1:]
            self._mem_index -= 1

    def _build_model(self):
        #TODO: Her initaliseres nettverket som skal vurdere hvor bra et flytt er
        # model = keras.Model(), model.Add()..., model.compile(), return model ish
        # Første lag må ha
        model = Sequential()

        model.add(Convolution2D(4, 3, input_shape=(*self._state_size, 1))) #*self._state_size,
        model.add(Flatten())
        model.add(Dense(4, activation='relu'))
        model.add(Dense(1, activation='linear'))

        model.compile(optimizer="adam", loss='mse')

        return model


    def train(self):
        #TODO: Her skal nettverket trenes etter hvert endte spill
        
        if self.epsilon > 0:
            self.epsilon -= self._epsilon_decrement
        else:
            self.epsilon = 0

        sample_size = min(len(self._memory), 200) # Set sample_size to 200, or size of memory if len(memory) < 200
        sample = random.sample(self._memory, sample_size) # Train on a random sample of the memory

        actions = np.array( [np.array(episode[0]).reshape(self._state_size) for episode in sample] ) # X_values for network
        actions = np.expand_dims(actions, axis=3)
        q_values = np.array([]) # Y_values for network
        for episode in sample:
            reward = episode[1]
            is_game_over = episode[2]
            index = episode[3]

            if is_game_over or index >= self._max_memory_size - 1:
                q_values = np.append(q_values, reward)
            else:
                next_episode = self._memory[index + 1]
                next_q = self._predict_reward(next_episode[0])
                q_value = reward + self.gamma * next_q
                q_values = np.append(q_values, q_value)

        self._model.fit(actions, q_values,
        batch_size=sample_size, epochs=100, verbose=self.verbose
        )


    def _predict_reward(self, possible_next_state):
        """
        input: list of feature_values for current and next state
        output: Predicted Reward for the action
        """
        #TODO: Her skal nettverket brukes til å predikere hvor bra et enkelt flytt er
        possible_next_state = np.array(possible_next_state)
        possible_next_state = np.expand_dims(possible_next_state, axis=(0, 3))
        return self._model.predict([possible_next_state])

    def save_model(self, model_name):
        print("Saving model...")
        self._model.save(filepath = 'models/' + model_name, overwrite = True)
        print("Saved.")
