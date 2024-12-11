from flask import Flask
from flask import render_template
from flask import request,session, redirect,send_from_directory,make_response,jsonify
from flask_session import Session
from datetime import timedelta
from user import *
from samples import *
from sequencing import *
from taxonomy import *
from detections import *
from export import *
import time
import datetime
import pandas as pd

#create Flask app instance
app = Flask(__name__,static_url_path='')

#Configure serverside sessions 
app.config['SECRET_KEY'] = '56hdtryhRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

#Basic root route - show the word 'homepage'
@app.route('/')  #route name
def home(): #view function
    return redirect('main')


@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')

@app.route('/main')
def main():
    session['filter_column'] = None
    session['filter_value'] = None
    if checkSession() == False: 
        return redirect('/login')
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    elif session['user']['role'] == 'LabTech':
        return render_template('main_LabTech.html', title='Main menu')
    elif session['user']['role'] == 'Analyst':
        return render_template('main_Analyst.html', title='Main menu')  
    
@app.route('/taxonomy/taxonomy_main_menu')
def taxonomy_main_menu():
    if checkSession() == False: 
        return redirect('/login')
    if session['user']['role'] == 'Analyst' or session['user']['role'] == 'admin':
        return render_template('/taxonomy/taxonomy_main_menu.html', title='Main menu') 
    else:
        return render_template('/taxonomy/taxonomy_main_menu_LabTech.html', title='Main menu') 

#### ALL THE VIEWS

@app.route('/users/view',methods=['GET','POST'])
def view_users():
    o = user()
    o.getAll()
    return render_template('users/view.html', title='Users Table',objs = o)
@app.route('/samples/view',methods=['GET','POST'])
def view_samples():
    o = samples()
    o.getAll()
    u = user()
    u.getAll()
    o.users = u
    return render_template('samples/view.html', title='Samples Table',objs = o)
@app.route('/sequencing/view',methods=['GET','POST'])
def view_sequencing():
    o = sequencing()
    o.getAll()
    u = user()
    u.getAll()
    o.users = u
    return render_template('sequencing/view.html', title='Sequencing Table',objs = o)
@app.route('/taxonomy/view',methods=['GET','POST'])
def view_taxonomy():
    o = user()
    spe = species()
    spe.getAll()
    o.species = spe
    g = genus()
    g.getAll()
    o.genus = g
    p = phylum()
    p.getAll()
    o.phylum = p
    return render_template('taxonomy/view.html', title='Taxonomy Tables',objs = o)
@app.route('/detections/view',methods=['GET','POST'])
def view_detections():
    o = detections()
    o.getAll()
    u = user()
    u.getAll()
    o.users = u
    s = samples()
    s.getAll()
    o.samples = s
    seq = sequencing()
    seq.getAll()
    o.sequencing = seq
    spe = species()
    spe.getAll()
    o.species = spe
    g = genus()
    g.getAll()
    o.genus = g
    p = phylum()
    p.getAll()
    o.phylum = p
    return render_template('detections/view.html', title='Detections Table',objs = o)

#### Export the Data
@app.route('/export/view',methods=['GET','POST'])
def export_data():
    if checkSession() == False: 
        return redirect('/login')
    # Join all the tables together approproiatly 
    o = export()
    o.getAll()
    o.getFields()
    # Get which column to filter by
    column = request.args.get('FilterColumn')
    value = request.args.get('FilterValue')
    extension = request.args.get('Download_type')
    print(f'column: {column}',flush=True)
    print(f'value: {value}',flush=True)
    print(f'extension: {extension}',flush=True)
    # Get list of values for that column
    if column != None and column != '':
        session['filter_column'] = column
        o.getCol(session['filter_column'])
        # Reset the value field too
        session['filter_value'] = None
    if value != None and value != '' and session['filter_column'] != None:
        print('here')
        session['filter_value'] = value
        o.getByField(session['filter_column'],session['filter_value'])
    if extension != None:
        print(session['filter_column'],flush=True)
        print(session['filter_value'],flush=True)
        if session['filter_column'] != None and session['filter_value'] != None:
            o.getByField(session['filter_column'],session['filter_value'])
            data = {}
            for field in o.fields:
                data[field] = []
                for row in o.data:
                    data[field].append(row[field])
            df = pd.DataFrame(data)
            print(df,flush=True)
            if extension == 'tsv':
                df.to_csv('output.tsv', sep="\t") 
            elif extension == 'csv':
                df.to_csv('output.csv') 
        
    
    return render_template('export/view.html',objs = o,temp_column=session['filter_column'], 
                           temp_value=session['filter_value'])



#### ALL THE MANAGES

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg="Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['user_name'] = request.form.get('name')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['user_name'] = request.form.get('name')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. <")
        else:
            return render_template('users/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)

@app.route('/samples/manage',methods=['GET','POST'])
def manage_samples():
    if checkSession() == False or (session['user']['role'] == 'Analyst'): 
        return redirect('/login')
    o = samples()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    u = user()
    u.getAll()
    o.users = u
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['SampleName'] = request.form.get('SampleName')
        d['DateSampled'] = request.form.get('DateSampled')
        d['Location'] = request.form.get('Location')
        d['Collector_uid'] = request.form.get('Collector_uid')#session['user']['uid']
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Sample added.")
        else:
            return render_template('samples/add.html',obj = o)
    if action is not None and action == 'update':
        print("Nope, over here!")
        o.getById(pkval)
        o.data[0]['SampleName'] = request.form.get('SampleName')
        o.data[0]['DateSampled'] = request.form.get('DateSampled')
        o.data[0]['Location'] = request.form.get('Location')
        o.data[0]['Collector_uid'] = request.form.get('Collector')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Sample updated.")
        else:
            return render_template('samples/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('samples/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('samples/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('samples/manage.html',obj = o)

@app.route('/sequencing/manage',methods=['GET','POST'])
def manage_sequencing():
    if checkSession() == False: 
        return redirect('/login')
    o = sequencing()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    u = user()
    u.getByField('role','LabTech')
    o.users = u
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['Technique'] = request.form.get('Technique')
        d['DateSeq'] = request.form.get('DateSeq')
        d['LabTech'] = request.form.get('LabTech')
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Sample added.")
        else:
            return render_template('sequencing/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['Technique'] = request.form.get('Technique')
        o.data[0]['DateSeq'] = request.form.get('DateSeq')
        o.data[0]['LabTech'] = request.form.get('LabTech')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Sample updated.")
        else:
            return render_template('sequencing/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        # Get names of Labtechs to display along with the sequences they sequenced
        for row in range(len(o.data)):
            u = user()
            u.getById(o.data[row]['LabTech'])
            o.data[row]['LabTech'] = u.data[0]['name']
        # Send object with names to html thing
        return render_template('sequencing/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('sequencing/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('sequencing/manage.html',obj = o)


############ Start OF TAXONOMICAL ROUTES

@app.route('/taxonomy/species/manage',methods=['GET','POST'])
def manage_species():
    if checkSession() == False or (session['user']['role'] == 'LabTech'): 
        return redirect('/login')
    o = species()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['Species'] = request.form.get('Species')
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Species added.")
        else:
            return render_template('taxonomy/species/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['Species'] = request.form.get('Species')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Species updated.")
        else:
            return render_template('taxonomy/species/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        # Send object with names to html thing
        return render_template('taxonomy/species/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('taxonomy/species/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('taxonomy/species/manage.html',obj = o)

@app.route('/taxonomy/genus/manage',methods=['GET','POST'])
def manage_genus():
    if checkSession() == False or (session['user']['role'] == 'LabTech'): 
        return redirect('/login')
    o = genus()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['Genus'] = request.form.get('Genus')
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Genus added.")
        else:
            return render_template('taxonomy/genus/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['Genus'] = request.form.get('Genus')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Genus updated.")
        else:
            return render_template('taxonomy/genus/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        # Send object with names to html thing
        return render_template('taxonomy/genus/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('taxonomy/genus/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('taxonomy/genus/manage.html',obj = o)

@app.route('/taxonomy/phylum/manage',methods=['GET','POST'])
def manage_phylum():
    if checkSession() == False or (session['user']['role'] == 'LabTech'): 
        return redirect('/login')
    o = phylum()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['Phylum'] = request.form.get('Phylum')
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Phylum added.")
        else:
            return render_template('taxonomy/phylum/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['Phylum'] = request.form.get('Phylum')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Phylum updated.")
        else:
            return render_template('taxonomy/phylum/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        # Send object with names to html thing
        return render_template('taxonomy/phylum/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('taxonomy/phylum/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('taxonomy/phylum/manage.html',obj = o)


############ END OF TAXONOMICAL ROUTES

@app.route('/detections/manage',methods=['GET','POST'])
def manage_detections():
    if checkSession() == False: 
        return redirect('/login')
    o = detections()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    # Query all the needed tables and add them in 
    t = user()
    t.getByField('role','Analyst')
    o.users = t
    t = samples()
    t.getAll()
    o.samples = t
    t = sequencing()
    t.getAll()
    o.sequencing = t
    t = species()
    t.getAll()
    o.species = t
    t = genus()
    t.getAll()
    o.genus = t
    t = phylum()
    t.getAll()
    o.phylum = t

    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['SampleID'] = request.form.get('Sample')
        d['SeqID'] = request.form.get('Sequencing')
        d['DateDetected'] = request.form.get('DateDetected')
        d['DetectionMethod'] = request.form.get('DetectionMethod')
        d['DetectionAnalyst'] = request.form.get('Analyst')
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Taxonomical Stuff
        dropdown_species = request.form.get('Species')
        manual_species = request.form.get('new_species')
        if manual_species:
            d['SpeciesID'] = manual_species
        else:
            d['SpeciesID'] = dropdown_species
        dropdown_genus = request.form.get('Genus')
        manual_genus = request.form.get('new_genus')
        if manual_genus:
            d['GenusID'] = manual_genus
        else:
            d['GenusID'] = dropdown_genus
        dropdown_phylum = request.form.get('Phylum')
        manual_phylum = request.form.get('new_phylum')
        if manual_phylum:
            d['PhylumID'] = manual_phylum
        else:
            d['PhylumID'] = dropdown_phylum
        # Verify
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Detection added.")
        else:
            print(f"\n\033[31m{o.errors}\033[0m\n")
            return render_template('detections/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['SampleID'] = request.form.get('SampleID')
        o.data[0]['SeqID'] = request.form.get('SeqID')
        o.data[0]['DateDetected'] = request.form.get('DateDetected')
        o.data[0]['DetectionMethod'] = request.form.get('DetectionMethod')
        o.data[0]['DetectionAnalyst'] = request.form.get('DetectionAnalyst')
        o.data[0]['PhylumID'] = request.form.get('PhylumSearch')
        # Taxonomical Stuff
        dropdown_species = request.form.get('Species')
        manual_species = request.form.get('new_species')
        if manual_species:
            o.data[0]['SpeciesID'] = manual_species
        else:
            o.data[0]['SpeciesID'] = dropdown_species
        dropdown_genus = request.form.get('Genus')
        manual_genus = request.form.get('new_genus')
        if manual_genus:
            o.data[0]['GenusID'] = manual_genus
        else:
            o.data[0]['GenusID'] = dropdown_genus
        # dropdown_phylum = request.form.get('Phylum')
        # manual_phylum = request.form.get('new_phylum')
        # if manual_phylum:
        #     o.data[0]['PhylumID'] = manual_phylum
        # else:
        #     o.data[0]['PhylumID'] = dropdown_phylum
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Detection updated.")
        else:
            return render_template('detections/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        # Send object with names to html thing
        return render_template('detections/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('detections/add.html',obj = o)
    else:
        o.getById(pkval)
        return render_template('detections/manage.html',obj = o)

# Endpoint for searching phylums from dynamic textboxs
@app.route('/searchSpecies', methods=['GET','POST'])
def searchSpecies():
    query = request.args.get('query', '')
    p = species()
    p.getAll()
    results = []
    for row in p.data:
        if query in row['Species']:
            results.append(row['Species'])
    return jsonify(results)

# Endpoint for searching phylums from dynamic textboxs
@app.route('/searchGenus', methods=['GET','POST'])
def searchGenus():
    query = request.args.get('query', '')
    p = genus()
    p.getAll()
    results = []
    for row in p.data:
        if query in row['Genus']:
            results.append(row['Genus'])
    return jsonify(results)

# Endpoint for searching phylums from dynamic textboxs
@app.route('/searchPhylum', methods=['GET','POST'])
def searchPhylum():
    query = request.args.get('query', '')
    p = phylum()
    p.getAll()
    results = []
    for row in p.data:
        if query in row['Phylum']:
            results.append(row['Phylum'])
    return jsonify(results)


# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False      
  
if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   