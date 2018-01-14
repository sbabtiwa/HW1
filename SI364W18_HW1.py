## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
#None


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
import json 
import api_key_news


app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return "<h1>Welcome to SI 364!</h1>"


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }

@app.route('/movie/<anytitlesearch>')
def movieinfo(anytitlesearch):
	get_movie_info = requests.get(("https://itunes.apple.com/search?term={}").format(anytitlesearch) + "&limit=25&entity=movie")
	movie_dict = json.loads(get_movie_info.text)
	return str(movie_dict)
	

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def receivenumber():
	number_form = """<!DOCTYPE html>
<html>
<body>
<form action="/todouble" method="POST">
  Enter your favorite number:<br>
  <input type="text" name="number" value= " ">
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
	return number_form

@app.route('/todouble', methods = ["GET", "POST"])
def returndouble():
	if request.method == "POST":
		the_input = request.form["number"]
		double_num = 2 * int(the_input)
		return "Double your favorite number is {}!".format(str(double_num))



	
	
	


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)


content_form = """<!DOCTYPE html>
<html>
<body>
<form action="/problem4form" method="POST">
  Enter a search topic:<br> 
  <input type="text" name="topic"> <br>
  <br>
  Enter your preferred news source:<br>
  <br>
  <input type="checkbox" name="news" value= "abc-news"> ABC News <br>
  <input type="checkbox" name="news" value= "bloomberg"> Bloomberg <br>
  <input type="checkbox" name="news" value= "the-new-york-times"> The New York Times <br>
  <input type="checkbox" name="news" value= "techcrunch"> Tech Crunch <br> 
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""

@app.route('/problem4form')
def collectcontent():
	return content_form

@app.route('/problem4form', methods = ["GET", "POST"])
def returnsources():
	if request.method == "POST":
		selected_news = request.form.getlist("news")
		search_topic = request.form["topic"]
		if len(selected_news) > 1:
			return "Please select only one news source." + "<br>" + "<br>" + "<br>" + content_form
		elif len(selected_news) == 0:
			return "Please select a news source." + "<br>" + "<br>" + "<br>" + content_form
		get_sources = requests.get(("https://newsapi.org/v2/everything?sources={}").format(selected_news[0]) 
			+ "&q={}".format(search_topic)
			+ "&apiKey=" 
			+ api_key_news.api_key)
		source_data = json.loads(get_sources.text)
		titles_str = ""
		for element in source_data["articles"]:
			titles_str += str(element["publishedAt"][:10]) + "&emsp;" + str(element["title"]) + "<br>" 		
		return titles_str + "<br>" + "<br>" + "<br>" + content_form

# Points will be assigned for each specification in the problem.

if __name__ == '__main__':
    app.run()


