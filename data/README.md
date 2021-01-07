The file [test-predictions.csv](test-predictions.csv) is a valid example prediction file that can be submitted to the [StrategyQA Leaderboard](https://leaderboard.allenai.org/). This is a prediction that every question's correct answer is the choice `True` ("Yes"), and scores about 13% correct. This file shows the submission format without revealing the correct answers.

The file [train-predictions.csv](train-predictions.csv) show similarly random answers (all predictions are for answer choice `True`) for the training set.

The file [train.jsonl](train.jsonl) has the correct answers to the training set. It can be used for improving the performance of your predictor before it predicts answers to the hidden test questions.
