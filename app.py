"""
Competitor Mapper — Flask Web App
Reads startups from Google Sheets, maps competitors using Claude + web search,
displays results in a dark dashboard.
"""
from flask import Flask, render_template, jsonify
from sheets.sheets_reader import load_startups
from sheets.sheets_writer import write_competitor_map
from agents.competitor_agent import CompetitorAgent
import threading

app = Flask(__name__)

# Global state
analysis_state = {
    "status": "idle",       # idle | running | done | error
    "results": [],
    "current": "",
    "progress": 0,
    "total": 0,
}

agent = CompetitorAgent()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify(analysis_state)


@app.route("/api/results")
def results():
    return jsonify(analysis_state["results"])


@app.route("/api/run", methods=["POST"])
def run_analysis():
    if analysis_state["status"] == "running":
        return jsonify({"error": "Analysis already running"}), 400

    thread = threading.Thread(target=_run_analysis)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started"})


def _run_analysis():
    """Runs in background thread."""
    try:
        analysis_state["status"]  = "running"
        analysis_state["results"] = []
        analysis_state["current"] = "Loading startups from Google Sheets..."
        analysis_state["progress"] = 0

        startups = load_startups()
        analysis_state["total"] = len(startups)

        results = []
        for i, startup in enumerate(startups):
            analysis_state["current"]  = f"Analyzing {startup['company_name']}..."
            analysis_state["progress"] = i + 1

            result = agent.analyze(startup)
            results.append(result)
            analysis_state["results"] = results

        # Write to Google Sheets
        analysis_state["current"] = "Writing results to Google Sheets..."
        write_competitor_map(results)

        analysis_state["status"]  = "done"
        analysis_state["current"] = "Analysis complete"

    except Exception as e:
        analysis_state["status"]  = "error"
        analysis_state["current"] = str(e)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
