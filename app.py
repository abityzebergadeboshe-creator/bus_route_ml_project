from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import joblib 
import pandas as pd
from datetime import datetime, timedelta

from database import create_database


app = Flask(__name__)

# Secret key for flash messages
app.secret_key = "guzoai-secret-key"


# ==============================
# DATABASE
# ==============================

DATABASE = "guzoai.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# Create database tables when the application starts
create_database()


# ==============================
# LOAD ML MODELS
# ==============================

model = joblib.load("model.pkl")
eta_model = joblib.load("eta_model.pkl")


# ==============================
# HOME
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# DRIVER DASHBOARD
# ==============================

@app.route("/driver")
def driver():
    return render_template("driver.html")


# ==============================
# DRIVER VERIFICATION
# ==============================

@app.route("/verify", methods=["GET", "POST"])
def verify():

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        driver_id = request.form["driver_id"]
        phone = request.form["phone"]
        vehicle = request.form["vehicle"]

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO drivers
                (driver_name, driver_id, phone, vehicle)
                VALUES (?, ?, ?, ?)
            """, (
                driver_name,
                driver_id,
                phone,
                vehicle
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            flash(
                "This Driver ID is already registered."
            )

            return redirect(url_for("verify"))

        conn.close()

        return render_template(
            "verification_result.html",
            driver_name=driver_name,
            driver_id=driver_id,
            phone=phone,
            vehicle=vehicle,
            status="Pending"
        )

    return render_template("verify.html")


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin")
def admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM drivers
        ORDER BY id DESC
    """)

    drivers = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        drivers=drivers
    )


# ==============================
# APPROVE DRIVER
# ==============================

@app.route("/approve/<int:driver_id>")
def approve(driver_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE drivers
        SET status = 'Approved'
        WHERE id = ?
    """, (driver_id,))

    conn.commit()
    conn.close()

    flash("Driver approved successfully.")

    return redirect(url_for("admin"))


# ==============================
# REJECT DRIVER
# ==============================

@app.route("/reject/<int:driver_id>")
def reject(driver_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE drivers
        SET status = 'Rejected'
        WHERE id = ?
    """, (driver_id,))

    conn.commit()
    conn.close()

    flash("Driver rejected.")

    return redirect(url_for("admin"))


# ==============================
# DRIVER SCHEDULE
# ==============================

@app.route("/schedule", methods=["GET", "POST"])
def schedule():

    if request.method == "POST":

        driver_name = request.form["driver_name"]
        route = request.form["route"]
        date = request.form["date"]
        start_time = request.form["start_time"]
        passengers = int(request.form["passengers"])

        # Convert selected date
        selected_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()

        today = datetime.now().date()

        two_weeks_from_now = today + timedelta(days=14)

        # Check 2-week limit
        if selected_date < today or selected_date > two_weeks_from_now:

            flash(
                "Schedules can only be added for the next two weeks."
            )

            return redirect(url_for("schedule"))

        conn = get_connection()
        cursor = conn.cursor()

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
        conn.close()

        flash("Schedule saved successfully.")

        return redirect(url_for("schedule"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            driver_name,
            route,
            date,
            start_time,
            passengers
        FROM schedules
        ORDER BY date, start_time
    """)

    schedules = cursor.fetchall()

    conn.close()

    return render_template(
        "schedule.html",
        schedules=schedules
    )


# ==============================
# PASSENGER DASHBOARD
# ==============================

@app.route("/passenger")
def passenger():
    return render_template("passenger.html")


# ==============================
# AI PREDICTION
# ==============================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        # Passenger inputs
        distance = float(
            request.form["distance"]
        )

        duration = float(
            request.form["duration"]
        )

        traffic = int(
            request.form["traffic"]
        )

        hour = int(
            request.form["hour"]
        )

        passengers = int(
            request.form["passengers"]
        )


        # ==============================
        # FARE PREDICTION
        # ==============================

        input_data = pd.DataFrame(
            [[
                distance,
                duration,
                traffic,
                hour,
                passengers
            ]],
            columns=[
                "distance_km",
                "duration_min",
                "traffic_level",
                "hour",
                "passenger_count"
            ]
        )

        prediction = model.predict(
            input_data
        )[0]


        # ==============================
        # ETA PREDICTION
        # ==============================

        eta_input = pd.DataFrame(
            [[
                distance,
                traffic,
                hour,
                passengers
            ]],
            columns=[
                "distance_km",
                "traffic_level",
                "hour",
                "passenger_count"
            ]
        )

        eta_prediction = eta_model.predict(
            eta_input
        )[0]


        # ==============================
        # SHOW RESULTS
        # ==============================

        return render_template(
            "prediction.html",
            prediction=round(
                prediction,
                2
            ),
            eta=round(
                eta_prediction,
                1
            ),
            traffic=traffic
        )

    return render_template("predict.html")


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
