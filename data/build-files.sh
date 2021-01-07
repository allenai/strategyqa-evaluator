#!/bin/bash

set -euo pipefail

if [[ ! -f strategyqa_dataset.zip  ]]; then
  echo Missing file strategyqa_dataset.zip
  echo
  echo Download it first: https://storage.googleapis.com/ai2i/strategyqa/data/strategyqa_dataset.zip
  exit 1
fi

# Questions with correct answers for the training set (test set is hidden)
unzip -zxvOf strategyqa_dataset.zip QASC_Dataset/train.jsonl > train.jsonl

# Predicted answers for the training and test sets (always "True").
tar -zxvOf qasc_dataset.tar.gz QASC_Dataset/train.jsonl | jq -r '[.id, "A"] | @csv' > train-predictions.csv
tar -zxvOf qasc_dataset.tar.gz QASC_Dataset/test.jsonl | jq -r '[.id, "A"] | @csv' > test-predictions.csv
