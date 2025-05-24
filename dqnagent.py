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


    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(self.state_size,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model
    
    def update_target_network(self):
        self.target_model.set_weights(self.model.get_weights())