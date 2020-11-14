import random
import numpy as np

class Agent():

    def __init__(
                self,
                gamma=0.9,
                epsilon=0.9,
                ):

        """
        gamma: discount factor for future rewards, [0 , 1]
            0 for not accounting for future rewards at all
            1 for weighting future rewards equal to current rewards

        epsilon: exploration vs exploitation, [0, 1]
            0 for always choosing best known option
            1 for choosing random options
        """
        self.gamma = gamma
        self.epsilon = epsilon
        self._memory = np.array([])
        self._model = self._build_model()

    def get_next_state(self, possible_next_states):
        max_reward = None
        best_state = None

        if random.random() < self.epsilon:
            return random.randint(0, len(possible_next_states)-1)

        else:
            best_reward = 0
            best_action = 0
            for action, state in enumerate(possible_next_states):
                predicted_reward = self._predict_reward(state)
                if predicted_reward > best_reward:
                    best_reward = predicted_reward
                    best_action = action

        return best_action

    def add_to_memory(self, action, reward):
        np.append(self._memory, (action, reward))

    def _build_model(self):
        #TODO: Her initaliseres nettverket som skal vurdere hvor bra et flytt er
        # model = keras.Model(), model.Add()..., model.compile(), return model ish
        return 0

    def _train(self):
        #TODO: Her skal nettverket trenes etter hvert endte spill
        sample_size = min(len(self._memory), 200) # Set sample_size to 200, or size of memory if len(memory) < 200
        sample = random.sample(self._memory, sample_size) # Train on a random sample of the memory

        actions = np.array([episode[0] for episode in sample]) # X_values for network
        q_values = None # Y_values for network


    def _predict_reward(self, possible_next_state):
        """
        input: list of feature_values for current and next state
        output: Predicted Reward for the action
        """
        #TODO: Her skal nettverket brukes til å predikere hvor bra et enkelt flytt er
        # return self.model.predict(possble_next_state)
        return 1

