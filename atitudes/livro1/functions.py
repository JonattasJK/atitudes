from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from . import forms, models
import datetime
    
def remove_spaces(word):
	y = ''
	for x in word:
		if x != ' ':
			y += x
	return y

def add_log(school, message):
	now = datetime.datetime.now()
	school.log = ' - ' + message + ' ' + now.strftime('%d-%m-%Y %H:%M') + '\n' + school.log
	school.save()
	
def numbers(string):
	numbers = '0123456789'
	new_string = ''
	for x in string:
		if x in numbers:
			new_string += x
	return new_string

def auth_confirm(password, request_user):
	user = User.objects.get(id=request_user)
	auth = authenticate(username=user.username, password=password)
	if user == auth:
		return True
	return False
	
def lessonName(lesson):
	lessonName = ''
	if lesson == 1 :
		lessonName = 'abertura'
	elif lesson == 2:
		lessonName = 'familia'
	elif lesson == 3:
		lessonName = 'maneiras'
	elif lesson == 4:
		lessonName = 'acordar'
	elif lesson == 5:
		lessonName = 'refeicoes'
	elif lesson == 6:
		lessonName = 'caminho'
	elif lesson == 7:
		lessonName = 'cumprimentos'
	elif lesson == 8:
		lessonName = 'colegas'
	elif lesson == 9:
		lessonName = 'professor'
	elif lesson == 10:
		lessonName = 'sala'
	elif lesson == 11:
		lessonName = 'banheiro'
	elif lesson == 12:
		lessonName = 'livros'
	elif lesson == 13:
		lessonName = 'biblioteca'
	elif lesson == 14:
		lessonName = 'computadores'
	elif lesson == 15:
		lessonName = 'teatro'
	elif lesson == 16:
		lessonName = 'cidade'
	elif lesson == 17:
		lessonName = 'especiais'
	elif lesson == 18:
		lessonName = 'avo'
	elif lesson == 19:
		lessonName = 'finish'
	return lessonName