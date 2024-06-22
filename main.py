from flask import Flask, redirect, session, send_from_directory,render_template,request
from db.scripts import DBWrapper
from db.queries import get_by_id, get_question_amount
from utils.settings import settings
from professions.professions import professions
from professions.get_profession_list import get_prof_list

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.key
db = DBWrapper(settings.DBName)


@app.route('/')
def index():
    session["statementID"] = 1
    
    session["intellectScores"] = {
        "Логический":0,
        "Внутренний":0,
        "Телесный":0,
        "Вербальный":0,
        "Музыкальный":0,
        "Образный":0,
        "Философский":0,
        "Социальный":0,
        "Природный":0
    }

    session["personalityScores"] = {
        "учитель":0,
        "воин":0,
        "торговец":0,
        "мастер":0
    }

    return send_from_directory("./static/html/","main.html")


@app.route('/test')
def test():
    data = db.get(get_by_id, [session["statementID"]])
    
    questionAmount = len(db.get(get_question_amount))-1 # у мекя 0 идей почему, но оно выдает [(0,), (0,), (0,) ... (0,)] 45 раз
    print(questionAmount)

    if not data:
        return redirect('/result')
    question = data[0][1]


    return render_template("test.html",question=question,statementID=session["statementID"],percent=int(((session["statementID"]-1)/questionAmount)*100))


@app.route("/back")
def back():
    if session["statementID"] < 1: return
    intellect = session["last"]["intellect"]
    personality = session["last"]["personality"]

    session["intellectScores"][intellect] -= session["last"]["answer"]
    if session["intellectScores"][intellect] < 0: session["intellectScores"][intellect] = 0
    
    if personality:
        session["personalityScores"][personality] -= session["last"]["answer"]
        if session["personalityScores"][personality] < 0: session["personalityScores"][personality] = 0
    session["statementID"] -= 1
    return redirect("/test")


@app.route("/answer")
def next():
    answer = int(request.args.get('value'))
    
    data = db.get(get_by_id, [session["statementID"]])

    if not data:
        return redirect("/result")
    intellect = data[0][2]
    personality = data[0][3]

    session["intellectScores"][intellect] += answer
    if session["intellectScores"][intellect] < 0: session["intellectScores"][intellect] = 0
    
    if personality: 
        session["personalityScores"][personality] += answer
        if session["personalityScores"][personality] < 0: session["personalityScores"][personality] = 0

    session["last"] = {"intellect":intellect, "personality":personality, "answer":answer}


    session["statementID"] += 1
    return redirect("/test")
    

@app.route('/result')
def result():
    intellect = max(session["intellectScores"], key=session["intellectScores"].get)
    personality = max(session["personalityScores"], key=session["personalityScores"].get)
    prof_list = get_prof_list(professions[intellect], professions[personality])
    print(prof_list)
    return render_template("result.html",labels=list(session["intellectScores"].keys()),data =list(session["intellectScores"].values()))

if __name__ == '__main__':
    app.run(debug=True)