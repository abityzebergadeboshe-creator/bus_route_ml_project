from flask import Flask, render_template, request, redirect
import sqlite3
import joblib
import pandas as pd

app = Flask(__name__)

# Load models
model = joblib.load("model.pkl")
eta_model = joblib.load("eta_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/driver")
def driver():
    return render_template("driver.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule():

    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            route TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            passengers INTEGER NOT NULL
        )
    """)

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        route = request.form["route"]
        date = request.form["date"]
        start_time = request.form["start_time"]
        passengers = int(request.form["passengers"])

        cursor.execute("""
            INSERT INTO schedules
            (driver_name, route, date, start_time, passengers)
            VALUES (?, ?, ?, ?, ?)
        """, (
            driver_name,
            route,
            date,
            start_time,
            passengers
        ))

        conn.commit()

    cursor.execute("""
        SELECT id, driver_name, route, date, start_time, passengers
        FROM schedules
        ORDER BY date, start_time
    """)

    schedules = cursor.fetchall()

    conn.close()

    return render_template(
        "schedule.html",
        schedules=schedules
    )


@app.route("/passenger")
def passenger():
    return render_template("passenger.html")




@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        # Get passenger inputs
        distance = float(request.form["distance"])
        duration = float(request.form["duration"])
        traffic = int(request.form["traffic"])
        hour = int(request.form["hour"])
        passengers = int(request.form["passengers"])

        # ---------------- FARE PREDICTION ---------------- #

        input_data = pd.DataFrame([[
            distance,
            duration,
            traffic,
            hour,
            passengers
        ]], columns=[
            "distance_km",
            "duration_min",
            "traffic_level",
            "hour",
            "passenger_count"
        ])

        prediction = model.predict(input_data)[0]

        # ---------------- ETA PREDICTION ---------------- #

        eta_input = pd.DataFrame([[
            distance,
            traffic,
            hour,
            passengers
        ]], columns=[
            "distance_km",
            "traffic_level",
            "hour",
            "passenger_count"
        ])

        eta_prediction = eta_model.predict(eta_input)[0]

        # ---------------- SHOW RESULTS ---------------- #

        return render_template(
            "prediction.html",
            prediction=round(prediction, 2),
            eta=round(eta_prediction, 1),
            traffic=traffic
        )

    return render_template("predict.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():

    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            driver_id TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        driver_id = request.form["driver_id"]
        phone = request.form["phone"]
        vehicle = request.form["vehicle"]

        cursor.execute("""
            INSERT INTO drivers
            (driver_name, driver_id, phone, vehicle)
            VALUES (?, ?, ?, ?)
        """, (driver_name, driver_id, phone, vehicle))

        conn.commit()
        conn.close()

        return render_template(
            "verification_result.html",
            driver_name=driver_name,
            driver_id=driver_id,
            phone=phone,
            vehicle=vehicle,
            status="Pending"
        )

    conn.close()

    return render_template("verify.html")

@app.route("/admin")
def admin():

    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM drivers")
    drivers = cursor.fetchall()

    conn.close()

    return render_template("admin.html", drivers=drivers)

@app.route("/approve/<int:driver_id>")
def approve(driver_id):

    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE drivers SET status = 'Approved' WHERE id = ?",
        (driver_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/reject/<int:driver_id>")
def reject(driver_id):

    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE drivers SET status = 'Rejected' WHERE id = ?",
        (driver_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)