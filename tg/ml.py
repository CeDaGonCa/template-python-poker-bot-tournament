import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from typing import List


class PokerModel:
    def __init__(self):
        # Initialize a Logistic Regression model for prediction
        self.model = LogisticRegression()
        

