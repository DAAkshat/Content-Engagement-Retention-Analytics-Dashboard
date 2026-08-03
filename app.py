from flask import Flask, render_template, jsonify
from database.load_data import load
from analytics import queries as q

app = Flask(__name__)

@app.before_request
def ensure_db():
    if not q.DB.exists():
        load()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/kpis")
def api_kpis():
    return jsonify(q.get_kpis())

@app.route("/api/dau")
def api_dau():
    return jsonify(q.get_dau())

@app.route("/api/mau")
def api_mau():
    return jsonify(q.get_mau())

@app.route("/api/genre")
def api_genre():
    return jsonify(q.get_genre())

@app.route("/api/churn")
def api_churn():
    return jsonify(q.get_churn())

@app.route("/api/abtest")
def api_abtest():
    return jsonify(q.get_abtest())

@app.route("/api/retention")
def api_retention():
    return jsonify(q.get_retention())

@app.route("/api/mau-trend")
def api_mau_trend():
    return jsonify(q.get_mau_trend())

@app.route("/api/cohort-heatmap")
def api_cohort_heatmap():
    return jsonify(q.get_cohort_heatmap())

@app.route("/api/genre-funnel")
def api_genre_funnel():
    return jsonify(q.get_genre_funnel())

@app.route("/api/premium-vs-free")
def api_premium_vs_free():
    return jsonify(q.get_premium_vs_free())

if __name__ == "__main__":
    load()
    app.run(debug=True, port=5000)
