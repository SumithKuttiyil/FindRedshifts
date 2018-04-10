from flask import Flask, render_template, request
app = Flask(__name__)
import  src.main as main



@app.route("/")
def hello():
    #main.mainMethod()
    return render_template('home.html', show='hidden')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    main.mainMethod(int(processed_text))
    return render_template('onClickhome.html', show='visible')

if __name__ == '__main__':
    app.run()