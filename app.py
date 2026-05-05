from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

words = ["apple", "banana", "grape", "mango", "peach"]

def start_game():
    session["word"] = random.choice(words)
    session["guessed"] = []
    session["attempts"] = 6

@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        start_game()

    word = session["word"]
    guessed = session["guessed"]
    attempts = session["attempts"]
    message = ""

    if request.method == "POST":
        guess = request.form.get("letter").lower()

        if guess in guessed:
            message = "Already guessed!"
        else:
            guessed.append(guess)
            session["guessed"] = guessed

            if guess not in word:
                attempts -= 1
                session["attempts"] = attempts

    display = " ".join([l if l in guessed else "_" for l in word])

    if "_" not in display:
        message = "🎉 You Won!"
    elif attempts == 0:
        message = f"💀 You Lost! Word was {word}"

    return render_template("index.html", display=display, attempts=attempts, message=message)

@app.route("/reset")
def reset():
    start_game()
    return "<h3>Game Restarted!</h3><a href='/'>Go Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)