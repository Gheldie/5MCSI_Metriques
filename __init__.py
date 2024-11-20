from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)    

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route('/commits/')
def commits():
  
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits_data = response.json()

    commit_minutes = []
    for commit in commits_data:
        commit_date = commit.get('commit', {}).get('author', {}).get('date')
        if commit_date:
            minute = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
            commit_minutes.append(minute)
    commit_counts = Counter(commit_minutes)
    commit_data = [{"minute": minute, "count": count} for minute, count in commit_counts.items()]

    return render_template('commits.html')


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("Histogramme.html")
  
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
  
if __name__ == "__main__":
  app.run(debug=True)
