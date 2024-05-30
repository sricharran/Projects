from flask import Flask,request, url_for, redirect, render_template
import pickle,joblib
import numpy as np

app = Flask(__name__, template_folder='templates')

model=pickle.load(open('./model.pkl','rb'))
scaler = joblib.load('./scaler')

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    temp= scaler.transform(np.array(int_features[0]).reshape(1,-1))[0][0]
    int_features[0] = temp
    final=[np.array(int_features)]
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)

    if output>str(0.5):
        return render_template('index.html',pred='You need a treatment.\nProbability of mental illness is {}'.format(output))
    else:
        return render_template('index.html',pred='You do not need treatment.\n Probability of mental illness is {}'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
