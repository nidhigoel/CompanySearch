from django.shortcuts import render
from django.http import HttpResponse
from DateTime import DateTime
import json
import os
import random
import django
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter,datestr2num

# Create your views here.
def index(request) : 
    return render(request, 'index.html')


# def home(request) :
# 	return render(request, 'home.html')


def main(request):
    if 'company_name' in request.GET : 
        company_name = request.GET['company_name']

        if company_name.lower() == 'amazon':
            with open('amazon.json' , 'r') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)
        if company_name.lower() == 'adobe':
            with open('adobe.json' , 'r') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)
        else : 
            with open('company_dict1.json' , 'r') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)

    return render(request,'navbar.html')

def main1(request, company_name):
    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
    return render(request , 'main1.html',data)


def reviews(request, company_name):

    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
    return render(request , 'reviews.html',data)

    with open('company_dict1.json' , 'r') as f:
            data = json.load(f)
    return render(request , 'reviews.html',data)



def feature(request,company_name):
    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
    return render(request , 'feature.html',data)


    print ("\n\n\n\ncompany name is : " + company_name)
    # company_name = request.GET['company_name']
    with open('company_dict1.json' , 'r') as f:
        data = json.load(f)
    return render(request , 'feature.html',data)


def specify_sentiment(request,company_name,sentiment_name):
    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
            sentiment_name.replace('_',' ')
            data['specified_sentiment'] = sentiment_name.replace('_',' ')
    return render(request , 'feature_sentiment.html',data)


def chart(request,company_name):
    print ("company name is : " + company_name)
    # company_name = request.GET['company_name']
    with open('data.json' , 'r') as f:
        data = json.load(f)
        data['name' ] = company_name

    print (data)
    return render(request,'charts.html', data)



    
def simple_chart(request,company_name):
    # with open('data.json' , 'r') as f:
    #     data = json.load(f)

    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
    data['name' ] = company_name
    print("\n\n printing \n\n ")
    print(data['temporal_json'])
    fig=Figure(figsize=(11,6))
    ax=fig.add_subplot(1,1,1)
    x=[]
    y=[] 

    interval1 = '1 Aug 2013 to 31 Jan 2014'
    interval2 = '1 Feb 2014 to 31 July 2014'
    interval3 = '1 Aug 2014 to 31 Jan 2015'
    interval4 = '1 Feb 2015 to 31 July 2015'
    interval5 = '1 Aug 2015 to 31 Jan 2016'
    interval6 = '1 Feb 2016 to 31 July 2016'
    interval7 = '1 Aug 2016 to 31 Jan 2017'
    interval8 = '1 Feb 2017 to 31 July 2017'
    interval_keys = [interval1, interval2, interval3, interval4, interval5, interval6, interval7, interval8]
    for interval_key in interval_keys : 
    # for i in data['yearlydata'] : 
        i = interval_key
        print(i + " and " + str(data['temporal_json'][i]['sentiment']))
        # print("\n|n")
        # x.append( datestr2num(i.split('to')[0]))
        y.append(data['temporal_json'][i]['sentiment'])
        #y.append(data['yearlydata'][i]['sentiment'])
        a,b = i.split('to')
        x.append(datestr2num(a))
        #x.append(datestr2num(b))
        # print("printing" + DateTime(data['yearlydata'][i]['sentiment'].split('to')[0]))
        # y.append(i['sentiment'])
    
    # x = [6,2,3,4,5,6,7,8]
    print(x)
    print(y)
    # now=datetime.datetime.now()
    # delta=datetime.timedelta(days=1)
    # for i in range(10):
        # x.append(now)
        # now+=delta
        # y.append(random.randint(0, 1000))
    
    # for  i in range(0,5):
        # print( str(x[i]) + " and " + str(y[i]))
    ax.plot_date(x, y, '-')
    #ax.plot_date(x, y, linewidth = 2)
    ax.set_xlabel('Half Yearly Data')
    ax.set_ylabel('Reviews')
    ax.set_title('Graphical View')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def feature_wise_chart(request, company_name, feature_name):
    # with open('data.json' , 'r') as f:
    #     data = json.load(f)
    #feature_name = 'environment'
    with open( company_name.lower() + '.json' , 'r') as f:
            data = json.load(f)
    data['name' ] = company_name
    print("\n\n printing \n\n ")
    print(data['temporal_json'])
    fig=Figure(figsize=(11,6))
    ax=fig.add_subplot(1,1,1)
    x=[]
    y=[] 

    interval1 = '1 Aug 2013 to 31 Jan 2014'
    interval2 = '1 Feb 2014 to 31 July 2014'
    interval3 = '1 Aug 2014 to 31 Jan 2015'
    interval4 = '1 Feb 2015 to 31 July 2015'
    interval5 = '1 Aug 2015 to 31 Jan 2016'
    interval6 = '1 Feb 2016 to 31 July 2016'
    interval7 = '1 Aug 2016 to 31 Jan 2017'
    interval8 = '1 Feb 2017 to 31 July 2017'
    interval_keys = [interval1, interval2, interval3, interval4, interval5, interval6, interval7, interval8]
    for interval_key in interval_keys : 
    # for i in data['yearlydata'] : 
        i = interval_key
        print(i + " and " + str(data['temporal_json'][i]['sentiment']))
        # print("\n|n")
        # x.append( datestr2num(i.split('to')[0]))
        feature_sentiment = 0
        no_of_occurences = 0
        for sentence_id in data['temporal_json'][i]['sentence_id']:
            print("\n\n")
            print(sentence_id)
            features_in_sentence = data['sentences'][sentence_id]['features']
            if feature_name in features_in_sentence.keys():
                feature_sentiment  += features_in_sentence[feature_name]['sentiment']
                no_of_occurences += 1
        if no_of_occurences != 0:
            feature_sentiment /= no_of_occurences
        y.append(feature_sentiment)
        #y.append(data['yearlydata'][i]['sentiment'])
        a,b = i.split('to')
        x.append(datestr2num(a))
        #x.append(datestr2num(b))
        # print("printing" + DateTime(data['yearlydata'][i]['sentiment'].split('to')[0]))
        # y.append(i['sentiment'])
    
    # x = [6,2,3,4,5,6,7,8]
    print(x)
    print(y)
    # now=datetime.datetime.now()
    # delta=datetime.timedelta(days=1)
    # for i in range(10):
        # x.append(now)
        # now+=delta
        # y.append(random.randint(0, 1000))
    
    # for  i in range(0,5):
        # print( str(x[i]) + " and " + str(y[i]))
    ax.plot_date(x, y, '-')
    #ax.plot_date(x, y, linewidth = 2)
    ax.set_xlabel('Half Yearly Data')
    ax.set_ylabel('Reviews')
    ax.set_title('Graphical View')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response