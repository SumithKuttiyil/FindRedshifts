from flask import Flask, render_template, request
app = Flask(__name__)
import  src.main as main
import  random
import numpy as np
import src.passingObjectClass as passObj
from flask_table import Table, Col



@app.route("/")
def hello():
    visibility='hidden'
    if (request.method == 'POST'):
        visibility = 'visible'
        pasObject = passObj.passingObjectClass(request.form['number_of_system'], request.form['firstname'],
                                               request.form['lastname'], request.form['Ions'],
                                               np.loadtxt(request.files['pic']), request.files['pic'].filename,
                                               request.form.getlist('Ions'))
        main.mainMethod(pasObject)
        return render_template('home.html', imgName=str(random.randint(1, 10000000)), visibility=visibility)

    else:

         return render_template('home.html',imgName=str(random.randint(1, 10000000)),  visibility=visibility)

@app.route('/onClickhome', methods=['POST', 'GET'])
def my_form_post():
    visibility = 'visible'
    tab=""

    if(request.method=='POST'):
         pasObject = passObj.passingObjectClass(request.form['number_of_system'], request.form['firstname'], request.form['lastname'], request.form['Ions'], np.loadtxt(request.files['pic']), request.files['pic'].filename, request.form.getlist('Ions') )
         #print(pasObject)
         final_needed_point=main.mainMethod(pasObject)
         class ItemTable(Table):
             observedWavelenth = Col('Observed Wavelength')
             flux = Col('Flux')
             restWavelength=Col('Rest Wavelength')
             ion=Col('Ion')

         # Get some objects
         class Item(object):
             def __init__(self, observedWavelenth, flux, restWavelength, ion):
                 self.observedWavelenth = observedWavelenth
                 self.flux = flux
                 self.restWavelength=restWavelength
                 self.ion=ion
         tem_list=[]
         for lis in final_needed_point:
             for l in lis:
                 tem_list.append(dict(observedWavelenth=str(l[0]), flux=str(l[1]), restWavelength=str(l[2]), ion=str(l[3])))


         table = ItemTable(tem_list)


    return render_template('onClickhome.html', imgName=str(random.randint(1, 10000000)), visibility=visibility, tab=table)

if __name__ == '__main__':
    app.run()