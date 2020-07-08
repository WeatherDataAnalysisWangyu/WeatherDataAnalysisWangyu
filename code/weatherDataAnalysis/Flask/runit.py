from flask import Flask, url_for, make_response
from flask import Flask, request, render_template,flash
# Define the WSGI application object

app=Flask(__name__)

app.secret_key='180'


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username,password]):
            print("参数不完整")
            flash(u'参数不完整')
        else:
            return render_template('pic_data.html')
    return render_template("login.html")

@app.route('/date/<date_>')
def get_date_(date_):
    my_list=[1,2,3,4,5]
    return render_template("pic_data.html",
                           date_=date_,
                           date_type=min,
                           my_list=my_list)

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if not all([username,password,password2]):
            print("参数不完整")
            flash(u'参数不完整')
        elif password!=password2:
            print("密码不一致")
            flash(u'密码不一致')
        else:
            return 'success'
    return render_template('demo.html')

@app.route('/data/')
def data():
    return  render_template("pic_data.html")

@app.route('/resp/')
def resp():
    resp=make_response()
    resp.status_code=200
    resp.headers["content-type"]="text/html"
    resp.response=render_template("resp.html")
    return resp






if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=8000)
    # app.run()