from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# Start the flask server
app = Flask(__name__)
# Add this when you import the flask debug toolbar extension
app.config['SECRET_KEY'] = "passwordistaco1234"
# This will turn displaying the 302 message off and then just redirect 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Tracks responses
RESPONSES = []
# Create a Key for the Session "Dictionary" Key
RESPONSES_KEY = "resp"

# "Homepage"
@app.route('/')
def show_start():
    """ Display the Start page for the survey """
    return render_template("start.html", survey=survey)

# Once Survey is complete Thank you
@app.route('/thank_you')
def show_thank_you():
    """ Survey is complete, thank you! """
    return render_template('/thank_you.html')

# Reset the Responses list and Redirect to first question
@app.route('/begin', methods=["POST"])
def start_survey():
    """ Clear any responses """
    RESPONSES = []

    session[RESPONSES_KEY] = []

    print(f"This is the LIST Length {len(RESPONSES)}")

    return redirect('/questions/0')

# Use an int path variable to note the question number
@app.route('/questions/<int:q_num>')
def show_question(q_num):
    """ Display the Question Based on Number """
    user_responses = session.get(RESPONSES_KEY)
    
    if (user_responses is None):
        # trying to access question page too soon
        return redirect("/")

    if(len(user_responses) == len(survey.questions)):
        return redirect('/thank_you')
    
    if (len(user_responses) != q_num):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {q_num}.")
        return redirect(f"/questions/{len(RESPONSES)}")

    question = survey.questions[q_num]
    return render_template('question.html', question_num=q_num, question=question)


# Display the Next Question or Thank you
@app.route('/answer', methods=["POST"])
def handle_response():

    # Get user submission
    choice = request.form['answer']

    # OLD VERSION
    RESPONSES.append(choice)
    print(len(RESPONSES))

    # Using a session 
    user_responses = session[RESPONSES_KEY]
    user_responses.append(choice)
    session[RESPONSES_KEY] = user_responses

    print(session['resp'])

    if(len(user_responses) == len(survey.questions)):
        # Survey complete
        RESPONSES.clear()
        return redirect('/thank_you')

    else:
        return redirect(f'/questions/{len(user_responses)}')




