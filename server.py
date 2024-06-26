from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    if not city:
        return render_template(
            "weather.html",
            title="Error",
            status="No city provided",
            temp="N/A",
            feels_like="N/A",
        )

    try:
        weather_data = get_current_weather(city)
        return render_template(
            "weather.html",
            title=weather_data["name"],
            status=weather_data["weather"][0]["description"].capitalize(),
            temp=f"{weather_data['main']['temp']:.2f}",
            feels_like=f"{weather_data['main']['feels_like']:.1f}",
        )
    except Exception as e:
        return render_template(
            "weather.html", title="Error", status=str(e), temp="N/A", feels_like="N/A"
        )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
