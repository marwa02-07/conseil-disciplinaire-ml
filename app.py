from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp.nlp_service import classify_report_fr

app = Flask(__name__)
CORS(app)  # autorise React à communiquer avec Flask

@app.route("/api/analyze-report", methods=["POST"])
def analyze_report():
    data = request.get_json()

    if not data or "report_text" not in data:
        return jsonify({"error": "report_text is required"}), 400

    report_text = data["report_text"]

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


if __name__ == "__main__":
    app.run(debug=True)
