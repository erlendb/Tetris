import random
import numpy as np
import keras

class Agent():

    def __init__(
                self,
                gamma=0.9,
                epsilon=0.9,
                num_training_games=10000,
                memory_size=5000
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
        """
        self.gamma = gamma
        self.epsilon = epsilon
        self._memory = np.array([])
        self._model = self._build_model()
        self._num_training_games = num_training_games
        self._max_memory_size = memory_size
        self._mem_index = 0

        self._epsilon_decrement = epsilon / num_training_games


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
        np.append(self._memory, (action, reward, is_game_over, self._mem_index))
        self._mem_index += 1

        if self._mem_index > self._max_memory_size:
            self._memory = self._memory[1:]
            self._mem_index -= 1

    def _build_model(self):
        #TODO: Her initaliseres nettverket som skal vurdere hvor bra et flytt er
        # model = keras.Model(), model.Add()..., model.compile(), return model ish
        return 0


    def train(self):
        #TODO: Her skal nettverket trenes etter hvert endte spill

        self.epsilon -= self._epsilon_decrement

        sample_size = min(len(self._memory), 200) # Set sample_size to 200, or size of memory if len(memory) < 200
        sample = np.random.choice(self._memory, sample_size) # Train on a random sample of the memory

        actions = np.array([episode[0] for episode in sample]) # X_values for network

        q_values = np.array([]) # Y_values for network
        for episode in sample:
            reward = episode[1]
            is_game_over = episode[2]
            index = episode[3]

            if is_game_over:
                np.append(q_values, reward)
            else:
                next_episode = self._memory[index + 1]
                next_q = self._predict_reward(next_episode[0])
                q_value = reward + self.gamma * next_q
                np.append(q_values, q_value)

        # self._model.fit(actions, q_values)


    def _predict_reward(self, possible_next_state):
        """
        input: list of feature_values for current and next state
        output: Predicted Reward for the action
        """
        #TODO: Her skal nettverket brukes til å predikere hvor bra et enkelt flytt er
        # return self.model.predict(possble_next_state)
        return 1

