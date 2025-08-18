import os
import csv
from flask import Flask, render_template,send_from_directory,url_for,request


app = Flask(__name__)


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path,"static"),
#                                "favicon.ico",mimetype='image/vnd.microsoft.icon')


@app.route("/")
def my_home():
    return render_template("./index.html")

@app.route("/<page>")
def pages(page="index.html"):
    return render_template(page)

def write_to_file(data):
    with open("database.txt",mode="a") as db:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = db.write(f"\nName:{name},Email:{email},Subject:{subject},Message:{message}")

def write_to_csv(data):
    with open("database.csv",mode="a",newline="") as db:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(db,delimiter=",",quotechar="\"",quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,subject,message])


@app.route("/submit_form", methods=["POST","GET"])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        write_to_csv(data=data)
        return render_template("contact.html")