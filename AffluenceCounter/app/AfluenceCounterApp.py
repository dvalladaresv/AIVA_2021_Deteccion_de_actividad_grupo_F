import time
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from affluence_counter import AffluenceCounter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=False)

@app.route('/process_video',methods=["POST"])
def process_video():
    try:
        f = request.files['file']
        f.save(secure_filename(f.filename))
        app = AffluenceCounter(f.filename)
        count_enter, count_not, time_process = app.process_video()
        results = {
            "video": f.filename,
            "enter": count_enter,
            "noenter": count_not,
            "time": round(time_process/60., 2)
        }
        os.rename(f.filename)

        return render_template('results.html', results=results)

    except:

        return render_template('index.html', error=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')