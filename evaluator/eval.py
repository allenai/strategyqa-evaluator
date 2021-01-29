import argparse
import json

from sari import SARI


class AnswerEvaluator:
    def __init__(self, args):
        self._correct = 0.0
        self._total = 0.0

    def __call__(self, gold, prediction):
        self._correct += int(gold["answer"] == prediction)
        self._total += 1

    def get_metrics(self):
        return {"Accuracy": self._correct / self._total}


class DecompositionEvaluator:
    def __init__(self, args):
        self._sari = SARI()

    def __call__(self, gold, prediction):
        sources = [gold["question"].replace("?", " ?").split()]
        predictions = [" ".join(prediction).replace("?", " ?").split()]
        targets = [[" ".join(gold["decomposition"]).replace("?", " ?").split()]]

        self._sari(sources, predictions, targets)

    def get_metrics(self):
        return {"SARI": self._sari.get_metric()["SARI"]}


class ParagraphsEvaluator:
    def __init__(self, args):
        self._scores = []
        self._retrieval_limit = args.retrieval_limit

    @staticmethod
    def _recall(relevant_paragraphs, retrieved_paragraphs):
        result = len(set(relevant_paragraphs).intersection(retrieved_paragraphs)) / len(
            relevant_paragraphs
        )
        return result

    def __call__(self, gold, prediction):
        evidence_per_annotator = []
        for annotator in gold["evidence"]:
            evidence_per_annotator.append(
                set(
                    evidence_id
                    for step in annotator
                    for x in step
                    if isinstance(x, list)
                    for evidence_id in x
                )
            )
        retrieved_paragraphs = prediction[: self._retrieval_limit]

        score_per_annotator = []
        for evidence in evidence_per_annotator:
            score = self._recall(evidence, retrieved_paragraphs) if len(evidence) > 0 else 0
            score_per_annotator.append(score)

        annotator_maximum = max(score_per_annotator)
        self._scores.append(annotator_maximum)

    def get_metrics(self):
        return {f"Recall@{self._retrieval_limit}": float(sum(self._scores)) / len(self._scores)}


class EvaluatorWrapper:
    def __init__(self, eval_keys, args):
        self._evaluators = {eval_key: self._get_evaluator(eval_key, args) for eval_key in eval_keys}
        self._retrieval_limit = args.retrieval_limit

    @staticmethod
    def _get_evaluator(eval_key, args):
        evaluator = {
            "answer": AnswerEvaluator(args),
            "decomposition": DecompositionEvaluator(args),
            "paragraphs": ParagraphsEvaluator(args),
        }[eval_key]

        return evaluator

    def __getitem__(self, eval_key):
        return self._evaluators[eval_key]

    def get_metrics(self):
        metrics = {
            "Accuracy": 0.0,
            "SARI": 0.0,
            f"Recall@{self._retrieval_limit}": 0.0,
        }
        for evaluator in self._evaluators.values():
            metrics.update(evaluator.get_metrics())
        return metrics


def evaluate(gold_annotations, all_predictions, args):
    evaluator = EvaluatorWrapper(all_predictions.keys(), args)
    for gold_instance in gold_annotations:
        qid = gold_instance["qid"]
        for predictions_key, predictions in all_predictions.items():
            evaluator[predictions_key](gold_instance, predictions[qid])
    return evaluator.get_metrics()


def main(args):
    golds_file = args.golds_file
    predictions_file = args.predictions_file
    metrics_output_file = args.metrics_output_file

    with open(golds_file) as infile:
        gold_annotations = json.load(infile)

    with open(predictions_file) as infile:
        predictions = json.load(infile)
        if len(gold_annotations) != len(predictions):
            raise Exception(
                f"The predictions file does not contain the same number of instances as the "
                "number of test instances."
            )

    all_predictions = {}
    for qid, prediction in predictions.items():
        if len(all_predictions) == 0:
            for key_option in ["answer", "decomposition", "paragraphs"]:
                if key_option in prediction.keys():
                    all_predictions[key_option] = {}
        else:
            error_message = f"There is a difference betweeen prediction types provided for instances: {all_predictions.keys()} != {prediction.keys()}"
            for prediction_key in all_predictions.keys():
                assert prediction_key in prediction, error_message
            assert len(all_predictions.keys()) == len(prediction.keys()), error_message

        for prediction_key in all_predictions.keys():
            all_predictions[prediction_key][qid] = prediction[prediction_key]

    results = evaluate(gold_annotations, all_predictions, args=args)
    with open(metrics_output_file, "w") as f:
        output = json.dumps(results, indent=4)
        print(output)
        f.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate StrategyQA predictions")
    # Required Parameters
    parser.add_argument(
        "--golds_file",
        type=str,
        help="Location of all gold annotations",
        required=True,
    )
    parser.add_argument(
        "--predictions_file",
        type=str,
        help="Location of predictions",
        required=True,
    )
    parser.add_argument("--retrieval_limit", type=int, default=10)
    parser.add_argument(
        "--metrics_output_file",
        type=str,
        help="Location of output metrics file",
        default="metrics.json",
    )

    args = parser.parse_args()
    print("====Input Arguments====")
    print(json.dumps(vars(args), indent=2, sort_keys=True))
    print("=======================")
    main(args)
