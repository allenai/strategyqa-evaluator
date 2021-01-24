# StrategyQA Evaluator

This repo hosts the evaluator for 
[StrategyQA leaderboard](https://leaderboard.allenai.org/strategyqa). You can [read
about StrategyQA on the dataset page](https://allenai.org/data/strategyqa).

This evaluator scores predictions provided in JSON format, and produces a file
with the scores in JSON format.

# Testing the evaluator

Run `test.sh` to build and test the evaluator.

The test will score the prediction files `answers_file_small.json`, `decomps_file_small.json` and `paras_file_small.json` against the
gold annotations in `gold_small.json`. If everything is okay, then the test will pass.

(These gold and predictions JSON files are representative of the real gold
and prediction files, but we put only 10 examples into them, thus the name "small".)

# Running the evaluator locally

You can follow the steps in test.sh to build and run the evaluator yourself
using Docker.

If you want to run the evaluator outside of Docker, look in the `evaluator`
directory and first install the dependencies specified in `requirements.txt`.
Then run `eval.py` as shown in the `test.sh` script.

# Submitting to the Leaderboard

To submit your own predictions to the [StrategyQA leaderboard](https://leaderboard.allenai.org/strategyqa), produce JSON files for all 490 test examples, in accordance with the desired evaluation:
- QA accuracy: produce file like `answers_file_small.json`
- Decomposition SARI score: produce file like `decomps_file_small.json`
- Recall@10 score: produce file like `paras_file_small.json`
