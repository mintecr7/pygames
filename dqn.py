import tensorflow as tf
from tensorflow import keras
import numpy as np


class DQN:
    
    def __init__(self, lr, score, paddle) -> None:
        self.lr = lr
        self.score = score
        self.paddle = paddle
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(4, activation='relu'),
            tf.keras.layers.Dense(4,activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid'),
        ])
        self.model.compile(
            loss="binary_crossentropy",
            optimizer="Adam",
            metrics="acc"
        )
    def move(self, predictition):
        if predictition ==1:
            self.paddle.move()
        else:
            self.paddle.move(up=False)
    
    def train(self, states, observation) -> int:
        print("States of the players:- {}".format(states))
        self.model.fit(np.asarray(states).astype('float32'), np.asarray(observation).astype('float32'))
    
    def predict(self, states) -> int:
        return self.model.predict(np.asarray(states).astype('float32'))