import os
import sys
import time
import json

# ensure project root and the "app" subfolder are on path so we can import existing modules
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root)
sys.path.append(os.path.join(root, "app"))


from flask import Flask, render_template, request, redirect, url_for, session, flash

# import profile utilities from the backend (the code lives in the `app` directory)
# since `app` is not a package we load modules directly after adjusting sys.path
try:
    import profiles as pf
    import prompt_engine as pe
except ImportError as exc:
    # if we still fail, re-raise to make debugging easier
    raise


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "devsecret")


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        senha = request.form.get("senha")
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        nivel = request.form.get("nivel")
        estilo = request.form.get("estilo")
        profile = {
            "name": nome,
            "idade": idade,
            "nivel de conhecimento": nivel,
            "estilo de aprendizagem": estilo,
            "senha": senha,
        }
        try:
            pf.register_user_profile(user_id, profile)
            flash("Registro bem‑sucedido. Faça o login.")
            return redirect(url_for("login"))
        except Exception as e:
            flash(str(e))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        senha = request.form.get("senha")
        profile = pf.get_user_profile(user_id)
        if profile and profile.get("senha") == pf.hash_password(senha):
            session["user_id"] = user_id
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    
    result = None
    images = []
    user = session["user_id"]
    question = None
    if request.method == "POST":
        question = request.form.get("topic")  # name matches form field in dashboard.html
        print("Pergunta recebida:", question)
        try:
            # the backend helpers expect sanitized input
            question = pe.check_input(user, question)
            prompt_model = pe.determine_prompt_model(user, question)
            response, images = pe.infer_engine(user, question, prompt_model)

        except Exception as e:
            # generation may fail if model not configured
            response = {"error": str(e)}
            prompt = None
            model_used = None
            images = []

        result = response
    return render_template("dashboard.html", question=question, response=result, images=images)


if __name__ == "__main__":
    # simple local server for development
    app.run(debug=True, host="0.0.0.0", port=5000)
