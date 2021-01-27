#!/bin/bash

set -e

echo ------------------------------
echo Building evaluator
echo ------------------------------
echo

cd evaluator
docker build -t strategyqa-evaluator .
cd ..

echo
echo ------------------------------
echo Running evaluator
echo ------------------------------
echo

OUTPUT_DIR=$(mktemp -d)

docker run \
  -v $PWD/gold_small.json:/data/gold_small.json:ro \
  -v $PWD/predictions_small.json:/predictions/predictions_small.json:ro \
  -v $OUTPUT_DIR:/output:rw \
  strategyqa-evaluator \
  python eval.py --golds_file /data/gold_small.json --predictions_file /predictions/predictions_small.json --metrics_output_file /output/metrics.json

echo
echo ------------------------------
echo Metrics
echo ------------------------------
echo

EXPECTED=$'{\n    "Accuracy": 0.8,\n    "SARI": 0.6644986320583632,\n    "Recall@10": 0.2833333333333333\n}'
ACTUAL=$(cat $OUTPUT_DIR/metrics.json)

echo Metrics obtained in file $OUTPUT_DIR/metrics.json:
echo 
echo $ACTUAL
echo

if [ "$ACTUAL" == "$EXPECTED" ]; then
    echo Metrics match expected values!
    echo 
    echo Test passed.
else
    echo Metrics DO NOT match expected values! Expected:
    echo
    echo $EXPECTED
    echo
    echo Something is wrong, test failed.
    exit 1
fi

