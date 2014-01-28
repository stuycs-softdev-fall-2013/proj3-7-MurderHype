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
_link = ""

@app.route('/',methods=["POST","GET"])
def home():
        if request.method == 'GET':
                return render_template("index.html",error_message="")
	elif request.method == 'POST':
		if (auth.authen(request.form['user'],request.form['pw'])):
			session['user'] = request.form['user']
			return redirect(url_for('home'))
		else:
			e = "Incorrect username/password combination"
			return render_template('index.html',error_message=e)

@app.route('/home',methods=["POST","GET"])
def home2():
        if request.method == 'GET':
                return render_template("index.html",error_message="You must login first!!!")
	elif request.method == 'POST':
		if (auth.authen(request.form['user'],request.form['pw'])):
			session['user'] = request.form['user']
			return redirect(url_for('home'))
		else:
			e = "Incorrect username/password combination"
			return render_template('index.html',error_message=e)

@app.route('/logout')
def logout():
	session.pop("user",None)
	return redirect(url_for('home'))

@app.route('/leaderbroad',methods=["GET"])
def leaderboard():
	if request.method == 'GET':
		data = posts.getRanking()
		return render_template("leaderboard.html",data=data)

@app.route('/register',methods=["POST","GET"])
def register():
	if 'user' in session:
		return redirect(url_for('home'))
	elif request.method == "GET":
		return render_template("register.html",em="")
	elif request.method == "POST":
		name = request.form['name']
		user = request.form['user']
		pw = request.form['pw']
		detail = request.form['detail']
		if (auth.register(user,pw,name,detail)):
			session['user'] = user
			return redirect(url_for('home'))
		else:
			return render_template('register.html',em="username already registered!")


@app.route('/addkill',methods=["POST","GET"])
def addKill():
	if 'user' not in session:
		return redirect(url_for('home2'))
	elif request.method == "GET":
		return render_template("addkill.html",em="")
	elif request.method == "POST":
		author = session['user']
		victim = request.form['victim']
		way = request.form['method']
		diffi = request.form['diff']
		detail = request.form['detail']
		if (posts.write(author,victim,way,diffi,detail)):
			return redirect(url_for("profile"))
		else:
			return render_template("addkill.html",em="You have already killed this person before!")


@app.route('/profile',methods =["GET"])
def profile():
	if 'user' not in session:
		return redirect(url_for('home2'))
	elif request.method == "GET":
		author = session['user']
		data = posts.getPosts(author)
		return render_template("profile.html",data = data)

@app.route('/addthread',methods=["POST","GET"])
def addthread():
	if 'user' not in session:
		return redirect(url_for('home2'))
	elif request.method=="GET":
		return render_template('addthread.html',em="")
	elif request.method=="POST":
		author = session['user']
		title = request.form['title']
		post = request.form['post']
		if (forum.write(author,title,post)):
			return redirect(url_for('forums'))
		else:
			return render_template('addthread.html',em="Another thread by the same title exists!")

@app.route('/thread',methods=["POST","GET"])
def thread():
	global _link
	topic = _link
	T = forum.getPost(topic)
	C = forum.getResponses(topic)
	if request.method=="GET":
		return render_template('thread.html',OC = T,com=C)
	elif request.method == "POST":
		author = session['user']
		text = request.form['response']
		forum.respond(author,topic,text)
		C = forum.getResponses(topic)
		return render_template('thread.html',OC=T,com=C)

@app.route('/forum',methods=["POST","GET"])
def forums():
	if request.method == "GET":
		data = forum.getTitles()
		return render_template("forums.html",data=data)
	elif request.method == "POST":
		if request.form['btn'] == "new":
			return redirect(url_for("addthread"))
		elif request.form['btn']:
			global _link
			_link = request.form['btn']
			return redirect(url_for('thread'))


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
      
var request = {
location: center
radius: '500'
query: 'park'
};
  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, callback);
}
function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      createMarker(results[i]);
    }
  }
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
        app.run(debug=True, host='0.0.0.0', port =7700)
