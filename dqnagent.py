import numpy as np
import tensorflow as tf
from collections import deque


class DQNAgent:
    def __init__(self, state_size, action_size, memory=2000, gamma=0.95, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995, batch_size=64, update_target_every=100):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=memory)  # Последние действия
        self.gamma = gamma                # Дискаунт фактор
        self.epsilon = epsilon                # Процент исследования
        self.epsilon_min = epsilon_min             # Минимальный процент исследования
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.update_target_every = update_target_every    # Когда должна обновляться модель.

        #Инициализация основной модели.
        self.model = self.build_model()
        #Инициализация целевой модели
        self.target_model = self.build_model()
        self.update_target_network()

    def take_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)  # Исследование
        state_tensor = tf.convert_to_tensor([state])
        q_values = self.model(state_tensor)
        return tf.argmax(q_values[0]).numpy()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.Input((self.state_size,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model
    
    def train(self):
        if len(self.memory) < self.batch_size:
            return
        
        # Выборка батча из памяти
        minibatch = np.random.choice(len(self.memory), self.batch_size, replace=False)
        states = np.array([self.memory[i][0] for i in minibatch])
        actions = np.array([self.memory[i][1] for i in minibatch])
        rewards = np.array([self.memory[i][2] for i in minibatch])
        next_states = np.array([self.memory[i][3] for i in minibatch])
        dones = np.array([self.memory[i][4] for i in minibatch])

        # Подсчёт Q-чисел
        target_q = self.model.predict(states, verbose=0)
        target_next_q = self.target_model.predict(next_states, verbose=0)
        
        for i in range(self.batch_size):
            if dones[i]:
                target_q[i][actions[i]] = rewards[i]
            else:
                target_q[i][actions[i]] = rewards[i] + self.gamma * np.max(target_next_q[i])

        self.model.train_on_batch(states, target_q)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        self.target_model.set_weights(self.model.get_weights())