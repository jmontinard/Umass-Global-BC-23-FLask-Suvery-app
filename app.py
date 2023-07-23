from flask import Flask, request, render_template,redirect, session, flash
from random import choice, sample
from flask_debugtoolbar import DebugToolbarExtension
# from stories import story 
# from stories import Story
from surveys import satisfaction_survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#  As people answer questions, you should store their answers in this list.
# responses = []
sess_key = 'responses'
@app.route('/')
def index():
    """Show home page"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('home.html', title = title, instructions = instructions)

@app.route('/start', methods=['POST'])
def show_start():
    
    session[sess_key] = []

    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def show_question(id):
    """show Questions """
    responses  = session.get(sess_key)
    if (responses is None):
        #if users trys to access a question page  early
        return redirect('/')
    
    if (len(responses) == len(satisfaction_survey.questions)): 
        #all questions have been answered
        return redirect('/complete')
    
    if (len(responses) != id):
          #if a user trys to access a question out of order they will be flashed with a message and then redirected to current message
          flash(f"Question #{id} does not exist")
          return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[id].question
    
    choices = satisfaction_survey.questions[id].choices

    return render_template('questions.html', question = question ,choices = choices, question_index = id)


@app.route("/answer", methods=["POST"])
def show_answer():
     """ shows anwser and appends to responses and redirects back to questions"""

     answer = request.form['choice']
     #seting sessions
     responses = session[sess_key]
     responses.append(answer)
     session[sess_key] = responses
          
     if (len(responses) == len(satisfaction_survey.questions)): 
        #all questions have been answered
        return redirect('/complete')
     else:
        return redirect(f'/questions/{len(responses)}')

@app.route("/complete")
def show_complete_route():
    """if all questions are reached show the user the a thank you page"""
    title = satisfaction_survey.title
    return render_template("thank-you.html", title = title)