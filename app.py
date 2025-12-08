from flask import Flask,request,Response,render_template,jsonify

from main import Main

obj=Main()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/from_link",methods=["POST","GET"])
def from_link():
    
    if request.method=="POST":
        data=request.form.get("user_link")
        try:
            response=obj.main_for_web(link=data,question="explain hotw the php code is ")
            return response
        except:
            print("error")
            return "error processing link",500



if __name__=="__main__":
    app.run(host="0.0.0.0",port=1111,debug=True)
    


