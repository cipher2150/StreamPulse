from flask import Flask, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

# Load data into SQLite
def load_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_csv("streaming_data.csv")
    df.to_sql("logs", conn, if_exists="replace", index=False)
    conn.close()

load_data()

@app.route("/")
def home():
    return "Streaming Analytics API Running"

@app.route("/metrics")
def metrics():
    conn = sqlite3.connect("database.db")

    query = """
    SELECT 
        AVG(bitrate) as avg_bitrate,
        AVG(startup_time) as startup_delay,
        SUM(buffer_duration)*1.0 / SUM(watch_time) as buffer_ratio,
        SUM(CASE WHEN error_code != 0 THEN 1 ELSE 0 END)*1.0 / COUNT(*) as error_rate
    FROM logs
    """

    result = pd.read_sql(query, conn).to_dict(orient="records")[0]
    conn.close()

    return jsonify(result)

@app.route("/network")
def network():
    conn = sqlite3.connect("database.db")

    query = """
    SELECT network_type,
           COUNT(*) as users,
           AVG(bitrate) as avg_bitrate
    FROM logs
    GROUP BY network_type
    """

    result = pd.read_sql(query, conn).to_dict(orient="records")
    conn.close()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)