import io
import json
from contextlib import redirect_stdout

from sklearn.metrics import confusion_matrix, f1_score

from ml.dataset import load_reports
from ml.predict import LEVELS, load_model


def summarize(reports, predictions):
    expected = [report.level for report in reports]
    labels = list(LEVELS)
    return {
        "f1_macro": f1_score(expected, predictions, labels=labels, average="macro"),
        "confusion_matrix": confusion_matrix(expected, predictions, labels=labels).tolist(),
        "errors": [
            {
                "scenario": report.scenario,
                "report_text": report.text,
                "expected": LEVELS[report.level],
                "predicted": LEVELS[int(prediction)],
            }
            for report, prediction in zip(reports, predictions, strict=True)
            if report.level != prediction
        ],
    }


def main():
    reports = load_reports()["test"]
    model = load_model()
    ml_predictions = model.predict([report.text for report in reports])

    with redirect_stdout(io.StringIO()):
        from nlp.nlp_service import classify_report_fr

        bert_predictions = [classify_report_fr(report.text)["level"] for report in reports]

    print(json.dumps({
        "test_reports": len(reports),
        "test_scenarios": len({report.scenario for report in reports}),
        "labels": list(LEVELS.values()),
        "bert_keywords": summarize(reports, bert_predictions),
        "tfidf_logistic_regression": summarize(reports, ml_predictions),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
