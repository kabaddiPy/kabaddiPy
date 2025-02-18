from flask import render_template, jsonify
from app import app
from app.data_fetch import get_live_scores
from app.visualizer import plot_team_performance
from app.notifications import send_push_notification

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live-data')
def live_data():
    live_data = get_live_scores()
    return jsonify(live_data)

@app.route('/team-performance-chart')
def team_performance_chart():
    chart_path = plot_team_performance()
    return jsonify({'chart_path': chart_path})

@app.route('/subscribe')
def subscribe():
    # Simulating subscription to push notifications
    send_push_notification("Kabaddi Match Update", "You're subscribed to live updates!")
    return jsonify({"status": "Subscribed to push notifications"})
