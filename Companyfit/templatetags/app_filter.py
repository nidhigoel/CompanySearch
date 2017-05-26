from django  import template
from DateTime import DateTime
import string 
import re
register = template.Library()

@register.filter (name = "get_from_dict")
def keyvalue(dict, key):    
    return dict[key] 

@register.filter(name ="sentiment_filter")
def get_sentiment(sentiment):
	sentiment = float(sentiment)
	print(sentiment)

	if(sentiment < float(-1)):
		return 'Very Negative'

	if (sentiment >= float(-1) and sentiment < float(-0.5)) : 
		return 'Very Negative' 

	if (sentiment >= float(-0.5) and sentiment <float(0)):
		return 'Negative' 
	
	if (sentiment == float(0) ): 
		return 'Neutral' 
	
	if sentiment >= float(0) and sentiment < float(0.5):
		return 'Positive' 
	
	if sentiment >= float(0.5) and sentiment <= float(1):
		return 'Very Positive' 

	if(sentiment > float(+1)):
		return 'Very Positive'
	
	return sentiment	

		


@register.filter(name="date_filter")
def get_date(date):
	date = str(date) 

	if(len(date)==0):
		return "Not Specified"
	x = DateTime(date)
	new_date = ""
	new_date += x.Day() + '  ' + str(x.day()) + '  ' + x.Month()  + '  ' + str(x.year())
	# print("new date is : " + str(new_date))
	return new_date


@register.filter(name="find_one_percent")
def find_one_percent(no_of_sentences):
	
	return(no_of_sentences*0.01)



@register.filter(name = "caps_filter")
def get_caps(word):
	return string.capwords(word) 

@register.filter(name = "replace_punctuation")
def replace_punctuation(url_text):
	print('\n\n')
	exclude = set(string.punctuation)
	filtered_url = ''.join(ch for ch in url_text if ch not in exclude)
	#return str(word.replace(' ','_').replace('/','_').replace('.','_').replace(':','_').replace('|','_'))
	filtered_url = filtered_url.replace('...',' ')
	filtered_url = filtered_url.replace(' ','_')
	print("\n\n\n")
	print("filtered url")
	print(filtered_url.encode('utf-8'))
	filtered_url = filtered_url.replace('\'','_')

	if filtered_url == '':
		filtered_url = '_'
	return str(filtered_url)

@register.filter(name = "remove_quotes")
def remove_quote(word):
	s = re.sub(r'^"*|"*$', '', word)
	return s

@register.filter(name = "debug1")
def debug1(dict):
	print('\n\nDebugging dict\n')
	#print(dict)
	for key,value in dict.items():
		print(key.encode('utf-8'))
		print('\n')
	return dict


@register.filter(name = "remove_and")
def remove_and(word):
	s = re.sub(r'&amp;','&', word)
	return s

