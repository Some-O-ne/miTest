from flask import Flask, redirect, session, send_from_directory,render_template,request
from db.scripts import do
from db.queries import get_by_id, get_question_amount
from utils.settings import settings
from professions.scripts import test_results


app = Flask(__name__)
app.config['SECRET_KEY'] = settings.key


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
    data = do(get_by_id, [session["statementID"]])
    if not data:
        return redirect('/result')
    question = data[0][1]
    
    questionAmount = len(do(get_question_amount))-1

    return render_template("test.html",question=question,statementID=session["statementID"],percent=int(((session["statementID"]-1)/questionAmount)*100))



@app.route("/back")
def back():
    if session["statementID"] < 1: return
    
    intellect = session["last"]["intellect"]
    personality = session["last"]["personality"]

    session["intellectScores"][intellect] -= session["last"]["answer"]
    session["personalityScores"][personality] -= session["last"]["answer"]

    session["statementID"] -= 1
    return redirect("/test")



@app.route("/answer")
def next():
    data = do(get_by_id, [session["statementID"]])
    if not data:
        return redirect("/result")
    
    answer = int(request.args.get('value'))
    intellect = data[0][2]
    personality = data[0][3]

    session["intellectScores"][intellect] += answer
    session["personalityScores"][personality] += answer

    session["last"] = {"intellect":intellect, "personality":personality, "answer":answer}

    session["statementID"] += 1
    return redirect("/test")
    


@app.route('/result')
def result():
    for key in session["intellectScores"]:
        if session["intellectScores"][key] < 0: session["intellectScores"][key] = 0
    for key in session["personalityScores"]:
        if session["personalityScores"][key] < 0: session["personalityScores"][key] = 0
    

    print("Тип интеллекта:", test_results(session["intellectScores"], session["personalityScores"])[0])
    print("Тип личности:", test_results(session["intellectScores"], session["personalityScores"])[1])
    print("Профессии:", test_results(session["intellectScores"], session["personalityScores"])[2])

    return render_template("result.html",labels=list(session["intellectScores"].keys()),data =list(session["intellectScores"].values()))



if __name__ == '__main__':
    app.run(debug=True)