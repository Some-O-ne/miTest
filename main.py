from flask import Flask, redirect, session, send_from_directory,render_template,request
from db.scripts import DBWrapper
from db.queries import get_by_id, get_question_amount
from utils.settings import settings
from professions.get_profession_list import get_prof_list
from summaries.summaries import summaries
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
        "Учитель":0,
        "Воин":0,
        "Торговец":0,
        "Мастер":0
    }

    return render_template("main.html")


@app.route('/test')
def test():
    data = db.get(get_by_id, [session["statementID"]])
    
    questionAmount = db.get(get_question_amount)[0][0] # у мекя 0 идей почему, но оно выдает [(0,), (0,), (0,) ... (0,)] 45 раз
    print(questionAmount)

    if not data:
        return redirect('/result')
    question = data[0][1]


    return render_template("test.html",question=question,statementID=session["statementID"],percent=int(((session["statementID"]-1)/questionAmount)*100) if session["statementID"] > 1 else 0)


@app.route("/back")
def back():
    if session["statementID"] < 1: return
    session["intellectScores"][session["last"]["intellect"]] -= session["last"]["answer"]
    personality = session["last"]["personality"]
    if personality:
        session["personalityScores"][personality] -= session["last"]["answer"]

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
    if personality:
        session["personalityScores"][personality] += answer

    session["last"] = {"intellect":intellect, "personality":personality, "answer":answer}


    session["statementID"] += 1
    return redirect("/test")
    

@app.route('/result')
def result():
    intellects = [name for name in session["intellectScores"] if session["intellectScores"][name] >= 5]
    personalities = [name for name in session["personalityScores"] if session["personalityScores"][name] >= 7]

    for name in session["intellectScores"]: session["intellectScores"][name] = max(0,session["intellectScores"][name])
    for name in session["personalityScores"]: session["personalityScores"][name] = max(0,session["personalityScores"][name])

    prof_list = get_prof_list(intellects, personalities)

    return render_template("result.html",
        intellectScores=session["intellectScores"],
        personalityScores=session["personalityScores"],
        intellects=intellects,
        personalities=personalities,
        prof_list = prof_list,
        summaries=summaries,
        list=list,len=len)

if __name__ == '__main__':
    app.run(debug=True)