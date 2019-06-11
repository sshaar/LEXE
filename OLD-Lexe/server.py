from flask import Flask, render_template, request
import sys
from datetime import datetime

from backend.audio import aud, play_audio
import backend.speech_recognition as SR
import backend.speech_synthesis as SS
import backend.task_manager_backend_2 as P
import backend.obtain_information as Obtain

app = Flask(__name__)
 

FLIP = 0
SR_Model = SR.load_model()
SR.load_language_model(SR_Model)

SS_model = SS.load_model()

taskDict = {}



@app.route('/table')
def search(text):

    query = P.parse_to_search(text)
    # query = 'computer databases'
    print(query)
    websites = Obtain.get_websites(query, num=5)
    
    summaries = {}
    for i, url in enumerate(websites):
        f1, f2 = Obtain.get_text(url)
        if not f1:
            continue
        summary = Obtain.get_summary(f1, f2)
        output_name='/Users/sshaar/hackathon/frontend/theme/output%d.wav'.format(i)
        summaries[i] = (summary, url, output_name)
        # SS.synthesize_parapgraph(SS_model, summary, output_name=output_name)

    youtube_links = Obtain.get_videos(query)
    
    y = {}
    for i in range(len(youtube_links)):
        y[i] = youtube_links[i]  

    return render_template('table.html', google=summaries, youtube=y)



@app.route('/', methods=['POST', 'GET'])
def index():
    global FLIP, taskDict
    lexa = aud()
    # taskDict = {}
    if request.method == 'POST':
        user = request.form
        print(user, file=sys.stdout)
        if 'search-button' in str(user):
            lexa.play()
            text = SR.transcripe_file(SR_Model, '/Users/sshaar/hackathon/frontend/theme/output.wav')
            print('I GOT IT', FLIP)
            print(text)
            tt = text.split()
            print('-'*50)
            print(tt)
            print('-'*50)
            if "add" in tt or "task" in tt or "homework" in tt :
                try:
                    textName = P.get_taskName(text)
                except:
                    textName = 'Computer Scinece Homeowrk'
                
                play_audio('/Users/sshaar/hackathon/frontend/theme/backend/due_date.wav')
                lexa.play()
                text = SR.transcripe_file(SR_Model, '/Users/sshaar/hackathon/frontend/theme/output.wav')
                try:
                    dueDate = P.get_deadline(text)
                except:
                    dueDate = datetime.strptime('Apr 15 2019', '%b %d %Y')

                play_audio('/Users/sshaar/hackathon/frontend/theme/backend/length_assignment.wav')
                lexa.play()
                text = SR.transcripe_file(SR_Model, '/Users/sshaar/hackathon/frontend/theme/output.wav')
                try:
                    length = float(P.get_data(text))
                except:
                    length = 5.0
                print(length)

                try:
                    taskDict = P.update_list(textName, P.give_score(length, P.get_taskTime(length, dueDate), 5), P.get_deadline(dueDate))
                except:
                    taskDict['Computer Scinece Homework'] = 700.0
            elif "can" in tt or "how" in tt or "tell" in tt or 'show' in tt or 'what' in tt:
                return search(text)

            else:
                play_audio('/Users/sshaar/hackathon/frontend/theme/backend/cannot_hear.wav')

            FLIP = not(FLIP)

    keys = list(taskDict.keys())
    print(keys)
    if(len(keys) >= 6):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]), t2= (keys[1]), t3= (keys[2]), t4= (keys[3]), t5= (keys[4]), t6= (keys[5]))
    elif(len(keys) == 5):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]), t2= (keys[1]), t3= (keys[2]), t4= (keys[3]), t5= (keys[4]))
    elif(len(keys) == 4):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]), t2= (keys[1]), t3= (keys[2]), t4= (keys[3]))
    elif(len(keys) == 3):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]), t2= (keys[1]), t3= (keys[2]))
    elif(len(keys) == 2):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]), t2= (keys[1]))
    elif(len(keys) == 1):
        return render_template("dashboard.html", flip=FLIP, t1= (keys[0]))
    else:
        return render_template("dashboard.html", flip=FLIP)

if __name__ == '__main__':
    app.run(debug = True)