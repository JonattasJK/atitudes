

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import string
from . import models

## TEM QUE ADICIONAR MAIS REQUISITOS PARA VALIDAR OS CAMPOS
# Quantidade de digitos de CPF e RG
# Digitar apenas números
# Formatar design de escrita  

class signUpForm(forms.Form):

	name = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	phone = forms.CharField(required=True)
	
	def is_valid(self):
		valid = True
		if not super(signUpForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['name'] == '':
			self.add_errors('Você esqueceu de preencher o seu nome.')
			valid = False
		if self.data['email'] == '':
			self.add_errors('Você esqueceu de preencher o seu email.')
			valid = False
		if self.data['phone'] == '':
			self.add_errors('Você esqueceu de preencher o seu telefone/celular.')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class newSchoolForm(forms.Form):

	name = forms.CharField(required=True)
	description = forms.CharField(required=True)
	cnpj = forms.CharField(required=True)
	address = forms.CharField(required=True)
	
	def is_valid(self):
		valid = True
		if not super(newSchoolForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['name'] == '':
			self.add_errors('Você esqueceu de preencher o nome da escola.')
			valid = False
		if self.data['description'] == '':
			self.add_errors('Você precisa adicionar uma descrição para a escola.')
			valid = False
		if self.data['cnpj'] == '':
			self.add_errors('Você precisa informar o CNPJ da escola.')
			valid = False
		if self.data['address'] == '':
			self.add_errors('Por favor, adicione um endereço para a escola.')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class newUserForm(forms.Form):
	username = forms.CharField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=False)
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True)
	password_confirm = forms.CharField(required=True)
	level = forms.IntegerField(required=True) #0-Eu 1-ADM 2-diretor 3-professor 4-aluno 5-cliente
	related_school =  forms.IntegerField(required=False)#ID da escola do usuário
	answerable = forms.IntegerField(required=False) #ID do professor responsável ou de quem fez o cadastro desse usuário
	sponsor_name = forms.CharField(required=False)
	sponsor_relationship = forms.CharField(required=False)
	sponsor_email = forms.EmailField(required=False)
	class_number = forms.CharField(required=False)
	class_year = forms.IntegerField(required=False)
	 
	def is_valid(self):
		valid = True
		if not super(newUserForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['username'] == '':
			self.add_errors('Você esqueceu de preencher o nome de usuário.')
			valid = False
		else:
			if User.objects.filter(username=self.data['username']):
				self.add_errors('Esse nome de usuário já está em uso.')
				valid = False
			if not self.data['username'].isalnum():
				self.add_errors('Não use espaços ou caracteres especiais no nome de login')
				valid = False
		if self.data['first_name'] == '':
			self.add_errors('Você esqueceu de preencher o seu primeiro nome.')
			valid = False
		if self.data['email'] == '':
			self.add_errors('Você esqueceu de preencher o seu e-mail.')
			valid = False
		if self.data['password'] == '':
			self.add_errors('Você esqueceu de preencher a senha.')
			valid = False
		if self.data['password_confirm'] == '':
			self.add_errors('Você esqueceu de confirmar a senha.')
			valid = False
		if self.data['password'] != self.data['password_confirm']:
			self.add_errors('A confirmação de senha precisa ser igual a senha!')
			valid = False
		if self.data['level'] == '5':
			if self.data['sponsor_name'] == '':
				self.add_errors('Você precisa informar o nome de usuário da pessoa responsável pelo seu cadástro.')
				valid = False
			if self.data['sponsor_relationship'] == '':
				self.add_errors('Informe a relação que a pessoa responsável tem com você.')
				valid = False
			if self.data['sponsor_email'] == '':
				self.add_errors('Por favor, informe o e-mail da pessoa responsável.')
				valid = False
		elif self.data['level'] == '4':
			if self.data['related_school'] == '':
				self.add_errors('Identifique a sua escola')
				valid = False
			else:
				if self.data['answerable'] == '':
					self.add_errors('informe o ID do(a) educador(a) responsável por você')
					valid = False
				else:
					profile = models.Profile.objects.filter(id=self.data['answerable'])
					if not profile:
						self.add_errors('O id de educador(a) está errado')
						valid = False
					else:
						school = models.School.objects.filter(id=self.data['related_school'])
						try:
							rSchool_name = profile[0].related_school.name
						except:
							rSchool_name = False
						if rSchool_name != school[0].name:
							self.add_errors('O educador informado não pertence à escola selecionada')
							valid = False
			if self.data['class_number'] == '':
				self.add_errors('Identifique a sua turma. Ex: 6A')
				valid = False
			if self.data['class_year'] == '':
				self.add_errors('Por favor, Informe em qual ano escolar você está.')
				valid = False
		return valid

	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class editUserForm(forms.Form):
	username = forms.CharField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email = forms.EmailField(required=False)
	
	def is_valid(self):
		valid = True
		if not super(editUserForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['username'] != '':
			if User.objects.filter(username=self.data['username']):
				self.add_errors('Esse nome de usuário já está em uso.')
				valid = False
			if not self.data['username'].isalnum():
				self.add_errors('Não use espaços ou caracteres especiais no nome de login')
				valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class editPasswordForm(forms.Form):
	password = forms.CharField(required=True)
	password_confirm = forms.CharField(required=True)
	password_old = forms.CharField(required=True)
	
	def is_valid(self, rUsername):
		valid = True
		if not super(editPasswordForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['password'] == '':
			self.add_errors('Você esqueceu de informar a nova senha')
			valid = False
		elif self.data['password_confirm'] == '':
			self.add_errors('Você esqueceu de confirmar a nova senha')
			valid = False
		elif self.data['password'] != self.data['password_confirm']:
			self.add_errors('A nova senha e a confirmação da senha não conferem')
			valid = False
		if self.data['password_old'] == '':
			self.add_errors('Você não informou a sua senha atual')
			valid = False
		else:
			user = authenticate(username=rUsername, password=self.data['password_old'])
			if user == None:
				self.add_errors('A sua senha atual está incorreta')
				valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class editRelatedForm(forms.Form):
	sponsor_name = forms.CharField(required=False)
	sponsor_relationship = forms.CharField(required=False)
	sponsor_email = forms.EmailField(required=False)
	class_number = forms.CharField(required=False)
	class_year = forms.IntegerField(required=False)
	
	def is_valid(self):
		valid = True
		if not super(editRelatedForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class editChapterForm(forms.Form):
	paragraph = forms.CharField(required=False)
	style = forms.CharField(required=True)
	color = forms.CharField(required=False)
	position = forms.IntegerField(required=False)
	paragraph_id = forms.IntegerField(required=False)
	sticker_submit = forms.CharField(required=False)
	
	def is_valid(self):
		valid = True
		if not super(editChapterForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class questTextForm(forms.Form):
	text = forms.CharField(required=False)
	
	def is_valid(self):
		valid = True
		if not super(questTextForm, self).is_valid():
			valid = False
		return valid
		
class addTitle(forms.Form):
	title = forms.CharField(required=True)
	
	def is_valid(self):
		valid = True
		if not super(addTitle, self).is_valid():
			self.add_errors('Ops! Algo deu errado!')
			valid = False
		if self.data['title'] == '':
			self.add_errors('Você deixou o título em branco!')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)

class addRatingForm(forms.Form):

	testimony = forms.CharField(required=True)
	author = forms.CharField(required=True)
	date = forms.DateField(required=False)
	address = forms.CharField(required=False)
	
	def is_valid(self):
		valid = True
		if not super(addRatingForm, self).is_valid():
			self.add_errors('Ops! Algo deu errado! Confira se você não esqueceu algo.')
			valid = False
		return valid
		
	def add_errors(self, message):
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)
