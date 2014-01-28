from flask import Flask
from flask import render_template,session,redirect,request,url_for
import urllib2
import method
import api
import auth
import posts
import forum

app=Flask(__name__)
app.secret_key = "MURDER HYPE"

@app.route('/',methods=["POST","GET"])
def home():
        if request.method == 'GET':
                return render_template("index.html",error-message="")
	elif request.method == 'POST':
		if (auth.authen(request.form['user'],request.form['pw'])):
			session['user'] = request.form['user']
			return redirect(url_for('home',error-message=""))
		else:
			return redirect(url_for('home',error-message="Incorrect username/password. Please try again."))

@app.route('/leaderbroad',methods=["GET"])
def leaderboard():
	if request.method == 'GET':
		return render_template("leaderboard.html",data=posts.getRanking())

@app.route('/register',methods=["POST","GET"])
def register():
	if 'user' in session:
		return redirect(url_for('home',error-message=""))
	elif request.method == "GET":
		return render_template("register.html")
	elif request.method == "POST":
		name = request.form['name']
		user = request.form['user']
		pw = request.form['pw']
		detail = request.form['detail']
		if (auth.register(user,pw,name,detail)):
			session['user'] = user
			return redirect(url_for('home',error-message=""))
		else:
			return redirect(url_for('register',em="username already registered!"))

@app.route('/addkill',methods=["POST","GET"])
def addKill():
	if 'user' not in session:
		return redirect(url_for('home',error-message="Please login first!"))
	elif request.method == "GET":
		return render_template("addkill.html",em="")
	elif request.method == "POST":
		author = session['user']
		victim = request.form['victim']
		way = request.form['method']
		diffi = request.form['diff']
		detail = reqeust.form['detail']
		if (posts.write(author,victim,way,diffi,detail)):
			return redirect(url_for("profile"))
		else:
			return redirect(url_for("addKill",em="You have already killed this person before!"))



##################################### From last project ########################
@app.route('/weather',methods=["POST","GET"])
def weather():
        if request.method == 'GET':
                blah = '11209'
                link = 'http://api.wunderground.com/api/01c5e2f1dd1d7086/conditions/q/' + blah + '.json'
                connection = urllib2.urlopen(link)
                response = connection.read()
                a = method.temperature(response)
                b = method.winds(response)
                c = method.rainfall(response)
                d = link[(link.find('conditions') + 13):(link.find('conditions') + 18)]
                link = 'http://api.wunderground.com/api/01c5e2f1dd1d7086/forecast/q/10007.json'
                connection = urllib2.urlopen(link)
                response = connection.read()
                e = method.img(response,1)
                f = method.img(response,3)
                g = method.img(response,5)
                h = method.img(response,7)
                i = method.stat(response,1)
                j = method.stat(response,3)
                k = method.stat(response,5)
                l = method.stat(response,7)
                m = method.today(response)
                n = method.tomorrow(response)
                o = method.datomorrow(response)
                p = method.edtomorrow(response)

                return render_template("Weather.html", temp = a, winds = b, rainfall = c, zips = d, icona = e, iconb = f, iconc = g, icond = h, today = i, tomorrow = j, datomorrow = k, edtomorrow = l, day1 = m, day2 = n, day3 = o, day4 = p)

        else: 
                zipcode = request.form['Zip'].encode('ascii','ignore')
                blah = str(zipcode)
                link = 'http://api.wunderground.com/api/01c5e2f1dd1d7086/conditions/q/' + blah + '.json'
                connection = urllib2.urlopen(link)
                response = connection.read()
                a = method.temperature(response)
                b = method.winds(response)
                c = method.rainfall(response)
                d = link[(link.find('conditions') + 13):(link.find('conditions') + 18)]
                link = 'http://api.wunderground.com/api/01c5e2f1dd1d7086/forecast/q/' + blah + '.json'
                connection = urllib2.urlopen(link)
                response = connection.read()
                e = method.img(response,1)
                f = method.img(response,3)
                g = method.img(response,5)
                h = method.img(response,7)
                i = method.stat(response,1)
                j = method.stat(response,3)
                k = method.stat(response,5)
                l = method.stat(response,7)

                return render_template("Weather.html", temp = a, winds = b, rainfall = c, zips = d, icona = e, iconb = f, iconc = g, icond = h, today = i, tomorrow = j, datomorrow = k, edtomorrow = l)


@app.route('/maps',methods=["POST","GET"])
def maps():
        if request.method == 'GET':
                function = """
 <script type="text/javascript">
          function initialize() {     
      var mapOptions = {
      center: new google.maps.LatLng(40.7179707, -74.01403479999999),
      zoom: 17,
      mapTypeId:google.maps.MapTypeId.HYBRID
      };
      var map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);
      }
      google.maps.event.addDomListener(window, 'load', initialize);
</script>
      """    
                return render_template("Maps.html", jscripts = function)
        else:
                address = request.form['Location'].encode('ascii','ignore')
                address = address.replace(" ", "+")
                link = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&sensor=true'
                connection = urllib2.urlopen(link)
                response = connection.read()
                functionp1 = """
          <script type="text/javascript">
          function initialize() {
          var JSONObject =  """
                functionp2 = """
 ;var lat = JSONObject.results[0].geometry.location.lat
      var lng = JSONObject.results[0].geometry.location.lng
          var mapOptions = {
          center: new google.maps.LatLng(lat, lng),
          zoom: 17,
          mapTypeId:google.maps.MapTypeId.Hybrid
          };
          var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);
          }
          google.maps.event.addDomListener(window, 'load', initialize);
</script>
          """
                function = functionp1 + response + functionp2
                return render_template("Maps.html",jscripts = function)

@app.route('/lawyer',methods=["POST","GET"])
def lawyer():
        if request.method == 'GET':
                return render_template("Lawyer.html")
        if request.method == 'POST':
                address = request.form['Location'].encode('ascii','ignore')
                return render_template('Lawyer.html',
                                       lawyers=api.search_yelp(address)['businesses'])
                
##################################### From last project ########################

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port =7002)
