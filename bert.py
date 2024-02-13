# https://colab.research.google.com/drive/1CHJLsqOmoFE-XMrNtOxTXs4k2cvefgSh#scrollTo=1B8tFfYpGGPU

import tensorflow_text as text
import tensorflow as tf
import tensorflow_hub as hub

import pandas as pd
import numpy as np

labels = {"Strong Sell": 1, "Sell": 2, "Hold": 3, "Buy": 4, "Strong Buy": 5}
