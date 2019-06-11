from flask import Flask, render_template, request
import sys

from audio import aud


app = Flask(__name__)
 

FLIP = 0



@app.route('/', methods=['POST', 'GET'])
def index():
    global FLIP
    lexa = aud()
    if request.method == 'POST':
        user = request.form
        print(user, file=sys.stdout)
        if 'search-button' in str(user):
            lexa.play()
            print('I GOT IT', FLIP)
            FLIP = not(FLIP)

    return render_template("dashboard.html", flip=FLIP)

if __name__ == '__main__':
    app.run(debug = True)