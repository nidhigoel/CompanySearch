from django.shortcuts import render
from django.http import HttpResponse
from DateTime import DateTime
import json
import os
import random
import django
import datetime
import re
#from sentiment_algo_code.f1 import gui1
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter,datestr2num
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib.request, sys
from bs4 import BeautifulSoup
import json
# Create your views here.
def index(request) : 
    return render(request, 'index.html')


# def home(request) :
# 	return render(request, 'home.html')
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def get_company_data(company_name):
    opener = AppURLopener()
    
    #partner_id = 139413
    #Key:    jcO2HtJNdxW    
    #company review
    url3 = "http://api.glassdoor.com/api/api.htm?t.p=139413&t.k=jcO2HtJNdxW&userip=0.0.0.0&useragent=&format=json&v=1&action=employers&q="+company_name+"&l=India"
    #parameter description-https://www.glassdoor.com/developer/companiesApiActions.htm
    response = opener.open(url3)
    soup = BeautifulSoup(response, "html.parser")
    newDictionary=json.loads(str(soup))
    #print(soup)
    
    #print(newDictionary)
    employers = newDictionary['response']['employers']
    print(employers)
    employer = []
    print(company_name)
    for i in range(len(employers)):
        print(employers[i]['name'])
        if employers[i]['name'].lower() == company_name.lower():
            print(employers[i]['name'])
            employer = employers[i]
            
    return(employer)       
#     print(employer['featuredReview']['jobTitle'])
#     print(employer['featuredReview']['pros'])
#     print(employer['featuredReview']['cons'])

#   print(get_company_data("adobe"))


def find_feature_sentiment(feature_name, ow_dict, sentence_text):
#     print("\n\n")
    print(feature_name)
    print(ow_dict)
    print(sentence_text)
    sentence_text =sentence_text.replace(',','')
    is_opw_present_flag = False
    #fpos = sentence_text.find(feature_name)
    if feature_name in ['(','??']:
        return(0)
    try:
        all_fpos_index = [m.start() for m in re.finditer(feature_name, sentence_text)]
    except:
        print("\n\n exception raised from find feature sentiment")
        return(0)
    if(len(all_fpos_index) == 0):
#         print(sentence_text)
#         print(feature_name)
        print("error feature name not present in sentence")
        return(0)
    #print(all_fpos_index)
    #fpos_last_char = fpos + len(feature_name)
    score = 0
    
    for key, value in ow_dict.items():
        #print(value)

        if (value == None):
            continue
        if key != 'sentiment' and key != 'pro' and key!='con':
            #print(key)
            fw_final_position = ''
            ow_final_position = ''
            final_least_distance = len(sentence_text) + 1
            is_opw_present_flag = True
            ow_pos = ''
            all_ow_pos = [m.start() for m in re.finditer(key, sentence_text)] #find list of all indexes
            fw_pos =''   
            least_distance = len(sentence_text) + 1
            for fpos in all_fpos_index:
                #print(fpos)
                fpos_last_char = fpos + len(feature_name)
                #print(fpos_last_char)
                for pos in all_ow_pos:
                    if abs(fpos-pos) <= least_distance:
                        least_distance = abs(fpos-pos)
                        ow_pos = pos
                        fw_pos = fpos
            if least_distance <= final_least_distance:           
                final_least_distance = least_distance
                ow_final_position = ow_pos
                fw_final_position = fw_pos
                #print(ow_pos)
            subsentence = ''
            if fw_final_position + len(feature_name) < ow_final_position:
                subsentence = sentence_text[fw_final_position : ow_final_position]
            elif fw_final_position > ow_final_position:
                subsentence = sentence_text[ow_final_position : fw_final_position]
            else:
                print("dummy being used")
                #subsentence = "dummy"##when opinion word is within the feature name
            print(subsentence)
            distance = len(subsentence.split())
            print(distance)
            if distance == 0:
#                 print(feature_name)
#                 print(key)
#                 print(sentence_text)
                print("distance comes out to be 0")
                distance = 1
                    #print(distance)
                    #print(value)
            score += value/distance
#             print(fw_final_position)
#             print(ow_final_position)
#             print(value)
#             print(distance)
#             print(score)
#     if is_opw_present_flag == False:
#         print("hi")
    if score == 0:
        if 'pro' in ow_dict.keys():
            score += 1
        elif 'con' in ow_dict.keys():
            score += -1
        
    print('score')
    print(score)             
    return(score)


def find_sentence_sentiment(sentence_text,algo_output_dictionary):
    #print(sentence_text)
    #    no_of_features = algo_output_dictionary['no_of_features']
    #print(no_of_features)
    sentence_orientation = 0
    no_of_opinion_words = 0
    print("\n\n")
    print(type("Here"))
    print(type(algo_output_dictionary))
    for key,value in algo_output_dictionary.items():
        if key != 'no_of_features':
            for op_word, op_word_score in value.items():
                if op_word != 'sentiment' and op_word_score != None:
                    #print(op_word_score)
                    no_of_opinion_words += 1
                    sentence_orientation = sentence_orientation + op_word_score
    #print(sentence_orientation)
    if sentence_orientation!=0:
        sentence_orientation = sentence_orientation/no_of_opinion_words
    #print(sentence_orientation)
#     if sentence_orientation < 0:
#         return(-1)
#     elif sentence_orientation > 0:
#         return(+1)
#     else:
#         return(0)
    return sentence_orientation

 
def traverse_algo_output_json(sentence_id,algo_output):
    #print(algo_output_value)
    dictionary = {}
    if sentence_id in algo_output.keys():
        algo_output_value = algo_output[sentence_id]
        no_of_features = len(algo_output_value)
        #print(no_of_features)
        dictionary['no_of_features'] = no_of_features
        for i in range(0,no_of_features):
            #print("----")
            #print(i)
            feature = algo_output_value[i]
            feature_name = feature[0]
            #print(feature_name)
            feature_opinion_words = feature[1]
            feature_dictionary = {}
            for opinion_word_tuple in feature_opinion_words:
                #print(opinion_word_tuple)
                feature_dictionary[opinion_word_tuple[0]] = opinion_word_tuple[1] ##using actual score instead of normalised score
            feature_dictionary['sentiment'] = 0##this is default value ##sentiment is being calculated when making feature json
            dictionary[feature_name] = feature_dictionary
    #print(dictionary)
    return dictionary


def make_review_sentence_dictionary(review_index,review_time,review_sentence,sentiment_algo_output_dictionary):
    dict_key = review_index
    dict_value = {}
    dict_value['time'] = review_time
    sentence_text = review_sentence
    dict_value['sentence_text'] = sentence_text
    # algo_output_dictionary = sentiment_algo_output_dictionary
    # if(len(algo_output_dictionary.keys())==0):
    #     return("could not process")
#     print('**\n')
#     print(algo_output_dictionary)
#     print(algo_output_dictionary.items())
    #algo_output_dictionary = update_sentiment_of_features(algo_output_dictionary,sentence_text)
    
     
    algo_output_dictionary = traverse_algo_output_json(review_index, sentiment_algo_output_dictionary)

    for key, value in algo_output_dictionary.items():
        if key!='no_of_features':
            print("\n\nheree")
            print(key)
            print(value)
            feature_sentiment = find_feature_sentiment(key, value, review_sentence)
            algo_output_dictionary[key]['sentiment'] = feature_sentiment

    dict_value['features'] = algo_output_dictionary
#    value['sentiment'] = 1         ##add logic->done
    dict_value['sentiment'] = find_sentence_sentiment(review_sentence, algo_output_dictionary)

    dictionary = {}
    dictionary[dict_key] = dict_value
    #print(dictionary)
    return dictionary

def make_company_json_on_fly(company_name):
    
    company_dictionary = {}
    company_dictionary['name'] = company_name
    response_from_glassdoor = get_company_data(company_name)
    #glassdoor_dictionary = response_from_glassdoor
    if 'website' in response_from_glassdoor.keys():
        company_dictionary['website'] = response_from_glassdoor['website']
    #company_dictionary['sectorName'] = glassdoor_dictionary['industry']
    if 'industry' in response_from_glassdoor.keys():
        company_dictionary['industryName'] = response_from_glassdoor['industry']

    print(response_from_glassdoor)
    featuredReview = response_from_glassdoor['featuredReview']

    review_id = "0000"
    review_time = featuredReview['reviewDateTime']
    review_sentence_list = [featuredReview['headline'], featuredReview['pros'], featuredReview['cons']]
    review_sentence = '. '.join(review_sentence_list)

    sentiment_algo_output_dictionary = gui.onFly(review_id,review_sentence)
    # print("\n\nhihihi")
    # print(sentiment_algo_output_dictionary.keys())
    review_sentence_dictionary = make_review_sentence_dictionary(review_id,review_time,review_sentence, sentiment_algo_output_dictionary)
    #print(review_sentence_dictionary)
    #print(review_sentence_dictionary.keys())
    #return(dictionary_onFly)

    company_dictionary['sentences'] = review_sentence_dictionary
    #print(company_dictionary)   
    return(company_dictionary)


def main(request):
    if 'company_name' in request.GET : 
        company_name = request.GET['company_name']
        print('Company name')
        print(company_name)
        if company_name.lower() == 'amazon':
            with open('amazon.json' , 'r',encoding  = 'utf-8') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)
        if company_name.lower() == 'adobe':
            with open('adobe.json' , 'r',encoding  = 'utf-8') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)
        if company_name.lower() == 'google':
            with open('google.json' , 'r',encoding  = 'utf-8') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)
        if company_name.lower() == 'maq software':
            with open('maq-software.json' , 'r',encoding  = 'utf-8') as f:
                data = json.load(f)
            data['name'] = "maq-software"
            return render(request , 'main1.html',data)
        if company_name.lower() not in ['amazon','google']:
            company_json_on_fly = make_company_json_on_fly(company_name.lower())
            # print("\n\nhelllooooooooo")
            # print(data.keys())
            # print(data)
            # dictionary = {}
            # dictionary['name'] = data["0000"]
            return render(request,'main2.html', company_json_on_fly)
            #return HttpResponse(data)

        else:
            with open('company_dict1.json' , 'r',encoding  = 'utf-8') as f:
                data = json.load(f)
            return render(request , 'main1.html',data)

    return render(request,'navbar.html')

def main1(request, company_name):
    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
    return render(request , 'main1.html',data)

def reviews(request, company_name):

    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
    #return render(request , 'reviews.html',data)


    if 'page' in request.GET : 
        page_no = request.GET['page'] 
    else:
        page_no = '1'

    print("i am here")
    for x in data['sentences'].items():
        print(x)
        break;
    
    t = tuple(data['sentences'].items())
    print("page inumber is : " + page_no)
    print(type(page_no))
    paginator = Paginator(t, 10)

    # return render(request , 'feature_test.html',data)
    try:
        users = paginator.page(int(page_no))
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    data = {}
    data['name'] = company_name
    temp_data = {}
    for x in users:
        print (x[0])
        temp_data[x[0]] = x[1]

    data['sentences'] = temp_data
    data['users'] = users


    index = int(page_no) - 1
    max_index = len(paginator.page_range) 
    print(index)
    if (index >=9) :
        start_index = index - 9
    else  : 
        start_index = 0
    end_index = index + 9 if index <= max_index - 9 else max_index

    page_range = paginator.page_range[start_index:end_index]

    data['page_range'] = page_range
     
    print( "range is : " + str(start_index ) + " and " + str(end_index))


    return render(request, 'reviews.html' , data )


    with open('company_dict1.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
    return render(request , 'reviews.html',data)

def feature(request,company_name):
    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
    return render(request , 'feature.html',data)


    print ("\n\n\n\ncompany name is : " + company_name)
    # company_name = request.GET['company_name']
    with open('company_dict1.json' , 'r',encoding  = 'utf-8') as f:
        data = json.load(f)
    return render(request , 'feature.html',data)

def specify_sentiment(request,company_name,sentiment_name):
    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
            sentiment_name.replace('_',' ')
            data['specified_sentiment'] = sentiment_name.replace('_',' ')
    return render(request , 'feature_sentiment.html',data)


def find_rating(score):
    # if(score == -1):
    #     return(0)
    # if(score > -1 and score <= -0.75):
    #     return(1)
    # if(score > -0.75 and score <= -0.5):
    #     return(1.5)
    # if(score > -0.5 and score <= -0.25):
    #     return(2)
    # if(score > 0.25 and score < 0):
    #     return(2.5)
    return((score*2)+3)



def simple_chart(request,company_name):
    # with open('data.json' , 'r',encoding  = 'utf-8') as f:
    #     data = json.load(f)

    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
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
        y.append(find_rating(data['temporal_json'][i]['sentiment']))
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
    ax.set_ylim([1,5])
    ax.plot_date(x, y, '-')
    #ax.plot_date(x, y, linewidth = 2)
    ax.set_xlabel('Half Yearly Data')
    ax.set_ylabel('Rating')
    ax.set_title('Graphical View')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def detail_chart(request,company_name):
    # with open('data.json' , 'r',encoding  = 'utf-8') as f:
    #     data = json.load(f)
    print("\r\ndetail chart")
    print(company_name)
    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
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
        y.append(find_rating(data['temporal_json'][i]['sentiment']))
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
    ax.set_ylabel('Rating')
    ax.set_title('Graphical View')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def feature_wise_chart(request, company_name, feature_name):
    # with open('data.json' , 'r',encoding  = 'utf-8') as f:
    #     data = json.load(f)
    #feature_name = 'environment'
    with open( company_name.lower() + '.json' , 'r',encoding  = 'utf-8') as f:
            data = json.load(f)
    data['name' ] = company_name
    print("\n\n printing \n\n ")
    print(data['temporal_json'])
    fig=Figure(figsize=(11,6))
    ax=fig.add_subplot(1,1,1)
    x=[]
    y=[] 

    feature_name = feature_name.replace('_',' ')

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
        print("\n\n-------------")
        print(feature_name)
        print(feature_sentiment)
        print("------------\n\n")
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
    ax.set_ylim([-1,1])
    ax.plot_date(x, y, '-')
    #ax.plot_date(x, y, linewidth = 2)
    ax.set_xlabel('Half Yearly Data')
    ax.set_ylabel('Score')
    ax.set_title('Graphical View')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response