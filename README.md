# StrategyQA Evaluator

This repo hosts the evaluator for 
[StrategyQA leaderboard](https://leaderboard.allenai.org/strategyqa). You can [read
about StrategyQA on the dataset page](https://allenai.org/data/strategyqa).

This evaluator scores predictions provided in JSON format, and produces a file
with the scores in JSON format.

# Testing the evaluator

Run `test.sh` to build and test the evaluator.

The test will score the prediction file `predictions_small.json` against the
answers in `gold_small.json`. If everything is okay, then the test will pass.

(These gold and predictions JSON files are both representative of the real gold
and prediction files, but we put 3 QA pairs into them, thus the name "small".)

# Running the evaluator locally

You can follow the steps in test.sh to build and run the evaluator yourself
using Docker.

If you want to run the evaluator outside of Docker, look in the `evaluator`
directory and first install the dependencies specified in `requirements.txt`.
Then run `eval.py` as shown in the `test.sh` script.

# Submitting to the Leaderboard

The file `predictions_dummy.json` is a valid dummy submission file for the
[StrategyQA leaderboard](https://leaderboard.allenai.org/strategyqa). It contains
predictions for 490 questions. If you submit it, you'll get this dummy score:

* Acc: 0.5076 (Accuracy)
* R@10: 0.3691 (Recall@10)

To submit your own predictions to the Leaderboard, produce a JSON file like
`predictions_dummy.json` with your predictions, and submit that.
