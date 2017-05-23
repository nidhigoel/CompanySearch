from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request) :
	return HttpResponse("hello")

def test(request) :
	Context = {'polarity':'positive','name':'Nidhi','type':'string'}
	return render(request, 'review.html', Context)

# def home(request) :
# 	return render(request, 'home.html')

def company_search(request) :
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            message = 'You searched for: %r' % request.GET['q']
            return HttpResponse(message)
    return render(request, 'home.html', {'error': error})
	# if 'q' in request.GET:
	# 	message = 'You searched for: %r' % request.GET['q']
	# else:
	#     message = 'You submitted an empty form.'
	# return HttpResponse(message)
#return render(request, 'comapany_search.html')