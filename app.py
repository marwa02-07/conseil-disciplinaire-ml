from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from ml.predict import predict_gravity

app = Flask(__name__)
CORS(app)  # autorise React à communiquer avec Flask


@app.get("/")
def compare_reports():
    return render_template("compare_reports.html")


@app.route("/api/analyze-report", methods=["POST"])
def analyze_report():
    data = request.get_json()

    if not data or "report_text" not in data:
        return jsonify({"error": "report_text is required"}), 400

    report_text = data["report_text"]

    from nlp.nlp_service import classify_report_fr

    result = classify_report_fr(report_text)

    return jsonify({
        "report_text": report_text,
        "disciplinary_level": result["level"],
        "details": {
            "stars": result["stars"],
            "confidence": result["confidence"],
            "reason": result["reason"]
        }
    }), 200


@app.post("/api/analyze-report-ml")
def analyze_report_ml():
    data = request.get_json(silent=True)
    report_text = data.get("report_text") if isinstance(data, dict) else None
    if not isinstance(report_text, str) or not report_text.strip():
        return jsonify({"error": "Saisissez un rapport non vide."}), 400

    try:
        result = predict_gravity(report_text.strip())
    except FileNotFoundError:
        return jsonify({
            "error": "Modèle ML absent. Lancez l’entraînement avec python -m ml.train."
        }), 503

    return jsonify({"report_text": report_text, **result})


if __name__ == "__main__":
    app.run(debug=True)
