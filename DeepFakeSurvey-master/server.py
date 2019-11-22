from flask import Flask, render_template, request, redirect, session, url_for
import os, glob, random
from testdb import Testdb
import json

real_image_list = [file[7:] for file in glob.glob("static/real-and-fake-face-detection/real_and_fake_face/training_real/*.jpg")]
fake_image_list = [file[7:] for file in glob.glob("static/real-and-fake-face-detection/real_and_fake_face/training_fake/*.jpg")]
merge_list = real_image_list + fake_image_list

client = Testdb()

data_ai = {}
with open('parseDat.txt') as json_file:
    data_ai = json.load(json_file)


app = Flask(__name__)
app.secret_key = "Hello"

@app.route('/empty', methods = ['POST', 'GET'])
def empty():
    return redirect('/r')

@app.route('/r')
def show_results():
    test = session.get('results', None)
    for k in test:
        real = int(client.getReal(k))
        fake = int(client.getFake(k))
        ans = "real" if "real" in k.split('/')[-1] else "fake"
        ai_guess = data_ai[k]
        temp = {
            "choice": test[k],
            "real": real,
            "fake": fake,
            'model': float(ai_guess),
            'ans': ans
        }
        test[k] = temp
    return render_template("result.html", data=test)

@app.route('/postmethod', methods = ['POST', 'GET'])
def my_function():
    if request.method == 'POST':
        result = request.json

        for key, val in result.items():
            if val == 0:
                client.incrementFake(key)
            else:
                client.incrementReal(key)

        session['results'] = result
        print(result)
    return ""

@app.route('/', methods=['POST', 'GET'])
def home():
    data = []
    for _ in range(10):
        data.append(random.choice(merge_list))
    return render_template('index.html', data=data)


        

    
if __name__ == "__main__":
    app.run(threaded=True, debug=True)



    