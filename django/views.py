from django.shortcuts import render, redirect
from django.http import HttpResponse
import pickle
import pandas as pd
import os
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge


# Create your views here.

class RegresionModel(object):
	model = None

	@staticmethod
	def getModel():
		if RegresionModel.model is None:
			module_dir = os.path.dirname(__file__)
			model_path = os.path.join(module_dir, "model_full.pkl")
			with open(model_path, "rb") as f:
				RegresionModel.model = pickle.load(f)
			return RegresionModel.model
		else:
			return RegresionModel.model

def index(request):
    return render(request, 'index.html', locals())

def result(request):
	if request.method == 'POST':

		#length = request.POST['length']
		try:
			length = float(request.POST.get('length', 0))
		except:
			length = 0.0

		if request.POST['director'] == 'steven':
			steven = 1.0
		else:
			steven = 0.0

		if request.POST['director'] == 'anthony':
			anthony = 1.0
		else:
			anthony = 0.0

		if request.POST['director'] == 'cecil':
			cecil_d = 1.0
		else:
			cecil_d = 0.0

		if request.POST['director'] == 'woody':
			woody_d = 1.0
		else:
			woody_d = 0.0

		if request.POST['director'] == 'john':
			john_d = 1.0
		else:
			john_d = 0.0

		if request.POST['director'] == 'ken':
			ken = 1.0
		else:
			ken = 0.0

		if request.POST['director'] == 'clint':
			clint = 1.0
		else:
			clint = 0.0

		if request.POST['director'] == 'busby':
			busby = 1.0
		else:
			busby = 0.0

		if request.POST['writer'] == 'stephen':
			stephen = 1.0
		else:
			stephen = 0.0
		
		if request.POST['writer'] == 'david':
			david = 1.0
		else:
			david = 0.0

		if request.POST['writer'] == 'cecil':
			cecil_w = 1.0
		else:
			cecil_w = 0.0

		if request.POST['writer'] == 'john':
			john_w = 1.0
		else:
			john_w = 0.0

		if request.POST['writer'] == 'woody':
			woody_w = 1.0
		else:
			woody_w = 0.0

		if request.POST['writer'] == 'dennis':
			dennis = 1.0
		else:
			dennis = 0.0

		if request.POST['writer'] == 'elmore':
			elmore = 1.0
		else:
			elmore = 0.0

		if request.POST['writer'] == 'william':
			william = 1.0
		else:
			william = 0.0

		if request.POST['company'] == 'warner':
			warner = 1.0
		else:
			warner = 0.0

		if request.POST['company'] == 'new':
			new = 1.0
		else:
			new = 0.0

		if request.POST['company'] == 'columbia':
			columbia = 1.0
		else:
			columbia = 0.0

		if request.POST['company'] == 'universal':
			universal = 1.0
		else:
			universal = 0.0

		if request.POST['company'] == 'touchstone':
			touchstone = 1.0
		else:
			touchstone = 0.0

		if request.POST['company'] == 'metro':
			metro = 1.0
		else:
			metro = 0.0

		if request.POST['company'] == 'paramount':
			paramount = 1.0
		else:
			paramount = 0.0

		if request.POST['company'] == 'twentieth':
			twentieth = 1.0
		else:
			twentieth = 0.0

		#sport = 0.0
		#sport = request.POST['sport']
		sport = float(request.POST.get('sport', 0.0))

		#musical = 0.0
		#musical = request.POST['musical']
		musical = float(request.POST.get('musical', 0.0))

		#family = 0.0
		#family = request.POST['family']
		family = float(request.POST.get('family', 0.0))

		#mystery = 0.0
		#mystery = request.POST['mystery']
		mystery = float(request.POST.get('mystery', 0.0))

		#history = 0.0
		#history = request.POST['history']
		history = float(request.POST.get('history', 0.0))

		#crime = 0.0
		#crime = request.POST['crime']
		crime = float(request.POST.get('crime', 0.0))

		#drama = 0.0
		#drama = request.POST['drama']
		drama = float(request.POST.get('drama', 0.0))

		#music = 0.0
		#music = request.POST['music']
		music = float(request.POST.get('music', 0.0))

		#adult = 0.0
		#adult = request.POST['adult']
		adult = float(request.POST.get('adult', 0.0))

		#news = 0.0
		#news = request.POST['news']
		news = float(request.POST.get('news', 0.0))

		#xn = 0.0
		#xn = request.POST['xn']
		xn = float(request.POST.get('xn', 0.0))

		#fantasy = 0.0
		#fantasy = request.POST['fantasy']
		fantasy = float(request.POST.get('fantasy', 0.0))

		romance = float(request.POST.get('romance', 0.0))

		war = float(request.POST.get('war', 0.0))

		action = float(request.POST.get('action', 0.0))

		adventure = float(request.POST.get('adventure', 0.0))

		horror = float(request.POST.get('horror', 0.0))

		sci_fi = float(request.POST.get('sci_fi', 0.0))

		comedy = float(request.POST.get('comedy', 0.0))

		western = float(request.POST.get('western', 0.0))

		thriller = float(request.POST.get('thriller', 0.0))

		animation = float(request.POST.get('animation', 0.0))

		bio = float(request.POST.get('bio', 0.0))

		noir = float(request.POST.get('noir', 0.0))

		doc = float(request.POST.get('doc', 0.0))

		month = request.POST['month']

		cr = RegresionModel.getModel()
		cube = PolynomialFeatures(degree=3)
		#cube_Ridge = Ridge(alpha = 100000)

		XX_test = pd.DataFrame([[length, sport, musical, family, mystery, history, crime, drama, music, bio, adult, adventure, news, xn, fantasy, romance, war, action, horror, thriller, animation, doc, western, sci_fi, comedy, noir, month, steven, anthony, cecil_d, woody_d, john_d, ken, clint, busby, stephen, david, cecil_w, john_w, woody_w, dennis, elmore, william, warner, new, columbia, universal, touchstone, metro, paramount, twentieth]])		

		X_cube = cube.fit_transform(XX_test)

		y_cube_pred = cr.predict(X_cube)
		y = round(y_cube_pred[0],2)

		
		return render(request, 'result.html', locals())

	else:
		return redirect('index/')
