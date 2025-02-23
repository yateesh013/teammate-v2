from flask import Flask,render_template,request,jsonify,redirect,url_for,flash,session
import databse as db
from datetime import timedelta
#import firebasedb as f_db



app=Flask(__name__)
app.secret_key="hello"
app.permanent_session_lifetime=timedelta(minutes=30)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))
        
@app.route("/userlogin",methods=['GET','POST'])
def userlogin():
    d3=request.values
    #check password from database
    pas=db.check_user(d3['mail'],d3['password'],login=True)
    if request.method=="POST" and pas==True:
        session["user"]=d3["mail"]
        return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))

@app.route("/usersignup",methods=['GET','POST'])
def usersignup():
    d3=request.values
    #flash message    
    #print(d3.get_json())
    db.add_user(d3)
    return redirect(url_for("login"))


@app.route("/profile",methods=['GET','post'])
def profile():
    if "user" in session:
        projects=db.get_projects(session["user"])    
        return render_template("user.html",user=session["user"],projects=projects)
    return redirect(url_for("login"))

@app.route("/addproject",methods=['GET','POST'])
def addproject():
    d3=request.values
    #add project
    #print(add_project(
    #["p1","ec",3,"skills","hghdrtd","user"]))
    db.add_project([d3["title"],d3["stack"],d3["number"],d3["git"],d3["description"],session["user"]])
   
    return redirect(url_for("profile"))

@app.route("/get_data/<id>",methods=["GET","POST"])
def edit(id):
    d3=db.get_projects(session["user"],name=id)
    return jsonify(d3)

@app.route("/delete/<title>",methods=["GET","POST"])
def delete(title):
    db.delete_project(title)
    return redirect(url_for("profile"))

@app.route("/updateproject/<data>")
def update(data):
    print(data)
    #db.update_project(list(data.split(",")))
    return jsonify("success")
@app.route("/browse-projects",methods=['GET','POST'])
def browse():
    projects=db.get_projects(session["user"],user=False)
    return render_template("browse.html",projects=projects)

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=10000)