from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import forms, models, functions
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
import mercadopago
import urllib
import json
import re
from django.core.mail import send_mail

@xframe_options_exempt
def iframe(request, item):
	return render(request, 'iframes/forLanding.html', {'item' : item})

def index(request):
	return redirect('livro1:home')
		
	if request.method == 'POST':
		form = forms.signUpForm(request.POST)
		if form.is_valid():
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': '6LePN_4ZAAAAACD-WSuzHC5HUe5b3bI68MVpjKox',
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())

			if result['success']:
				data_form = form.data
				wishingToJoin = models.WishingRegistred()
				wishingToJoin.name = data_form['name']
				wishingToJoin.email = data_form['email']
				wishingToJoin.phone = data_form['phone']
				return redirect('livro1:about')
		return render(request, 'landing1/index.html', {'form' : form})
	return render(request, 'landing1/index.html')
	
def congrats(request):
	return render(request, 'adm/congrats.html')

def about(request):
	ratings = models.Rating.objects.all().order_by('?')[:5]
	books = models.SavedBook.objects.all().order_by('rating', '-id')[:10]
	return render(request, 'landing1/about.html', {'books' : books, 'ratings' : ratings})

def prototyping(request):
	return render(request, 'index/index.html')

@login_required
def continues(request):
	continues = request.user.profile.continues
	lessonName = continues[:-1]
	pageNumber = continues[-1]
	if lessonName == 'finish':
		return redirect('livro1:finish')
	if lessonName == '':
		lessonName = 'abertura'
		pageNumber = '1'
	return redirect('livro1:lesson', lesson = lessonName, page = pageNumber)
	
def privacy(request):
	return render(request, 'privacy.html')
	
def suport(request):
	return render(request, 'suport.html')
    
@login_required
def home(request):
	#send_mail('Subject here','Here is the message.','contato@projetoatitudes.com',['jonataseliask@hotmail.com'],fail_silently=False,)
	stage = request.user.profile.stage
	profile = request.user.profile
	if not profile.active:
		checkouts = profile.checkout.all().order_by('?')
		try:
			sdk = mercadopago.SDK("APP_USR-6199102471644452-052718-40eb8adddafc4ba83af1ad960cc0dccf-765040003")
			for c in checkouts:
				payment = sdk.payment().get(c.paymentID)
				if payment['response']['status'] == "approved":
					c.mp_status = payment['response']['status']
					c.save()
					profile.active = True
					profile.save()
		except:
			for c in checkouts:
				if c.paid:
					profile.active = True
					profile.save()
		if not profile.active:
			return redirect('livro1:payment')	
	return render(request, 'home.html', {'stage':stage})
	
@csrf_exempt
def payment_notification(request):
	#if request.method == 'POST':
	current_path = request.get_full_path() #Pega a string da URL
	payment_id = re.search('payment&id=(.*)', current_path) #Pega o valor do ID de pagamento
	if payment_id == None: #Se não conseguiu encontrar o ID
		return HttpResponse(status=201)
	try: 
		sdk = mercadopago.SDK("APP_USR-6199102471644452-052718-40eb8adddafc4ba83af1ad960cc0dccf-765040003")
		payment = sdk.payment().get(payment_id.group(1)) #Busca os dados do pagamento
		checkout = models.Checkout.objects.filter(paymentID = payment_id.group(1)) #Procura por algum pagamento com esse ID
		if checkout: #Verifica se foi encontrado algum pagamento
			current_checkout = models.Checkout.objects.get(paymentID = payment_id.group(1)) #Pega o pagamento com esse ID
			current_checkout.mp_status = payment['response']['status'] #Atualiza o status do pagamento
			if current_checkout.mp_status == "approved": #Se o pagamento foi aprovado
				current_checkout.paid = True #Define como True, Se não, o default é False mesmo
				profile = current_checkout.profile #Pega o perfil relacionado a esse pagamento
				profile.active = True #Ativa o premium 
				profile.save() #Salva o perfil
			current_checkout.save() #Salva o pagamento
		else: #Se o pagamento não está salvo no banco de dados
			external_ref = "" #Inicializa a variável external_ref
			try: #Tenta resgatar a referência externa do pagamento enviado pelo MP
				external_ref = payment['response']['external_reference'] #Pega a referência externa do MP
			except: #Se não tem referência externa, é engano
				return HttpResponse(status=200) #Retorna um ok e acaba por aqui
			profileID = re.search('(.*?)_R_', external_ref) #Pega o ID contido na external_ref
			if profileID == None: #Se não encontrou a expressão _R_
				return HttpResponse(status=200) #Retorna um ok e acaba por aqui
			try_profile = models.Profile.objects.filter(id=profileID.group(1)) #Tenta encontrar um perfil correspondente
			if try_profile: #Verifica se encontrou
				profile = models.Profile.objects.get(id=profileID.group(1)) #Se sim, pega o perfil em questão
				current_checkout = models.Checkout() #Cria um novo pagamento
				current_checkout.profile = profile#Define o usuário do pagamento
				current_checkout.external_ref = external_ref #Guarda a chave external_ref
				current_checkout.paymentID = payment_id.group(1) #Guarda o ID de pagamento
				current_checkout.mp_status = payment['response']['status'] #Salva o status retornado pelo MP
				if current_checkout.mp_status == "approved": #Se o pagamento foi aprovado
					current_checkout.paid = True #Define como True, Se não, o default é False mesmo
					profile.active = True #Ativa o premium 
					profile.save() #Salva o perfil
				current_checkout.save() #Salva o pagamento
	except:
		return HttpResponse(status=201)
	return HttpResponse(status=200)
	#return redirect('livro1:home')

def payment_return(request, id_profile, external_ref):
	current_path = request.get_full_path() #Pega a string da URL
	payment_id = re.search('payment_id=(.*?)&', current_path)#Tenta pegar o valor do ID de pagamento
	if payment_id == None: #Se não conseguiu encontrar o ID
		return redirect('livro1:payment') #retorna para a página de pagamento
	try: 
		sdk = mercadopago.SDK("APP_USR-6199102471644452-052718-40eb8adddafc4ba83af1ad960cc0dccf-765040003")
		payment = sdk.payment().get(payment_id.group(1)) #Busca os dados do pagamento
		if payment['response']['external_reference'] == external_ref: #Verifica se a referência da compra é a mesma enviada pelo MP
			profile = models.Profile.objects.get(id=id_profile) #Pega o objeto Perfil do usuário
			checkout = profile.checkout.filter(external_ref=external_ref) #Busca por pagamentos salvos no perfil do usuário
			if checkout: #Verifica se foi encontrado algum pagamento
				current_checkout = profile.checkout.get(external_ref=external_ref) #Se sim, busca o pagamento enviado pelo MP
				checkouts = profile.checkout.all() #Busca todos os possíveis pagamentos vinculados ao usuário
				paid = False #Define previamente uma variável de pagamento como False
				for c in checkouts: #inicia uma busca pela lista de pagamentos
					if c.paid: #Verifica se o pagamento foi aprovado
						paid = True #Se sim, define a variável de pagamento como True
						paid_ref = c.external_ref #Resgata o valor da referência do pagamento
				current_checkout.mp_status = payment['response']['status'] #Salva o status retornado pelo MP
				if current_checkout.mp_status == "approved": #Verifica se o pagamento enviado pelo MP está aprovado
					current_checkout.paid = True #Se sim, define o pagamento atual como aprovado (Fim do bloco)
				elif paid: #Se não, verifica se algum pagamento já foi aprovado anteriormente
					if external_ref == paid_ref: #Se sim, verifica se é esse pagamento em questão
						current_checkout.paid = None #Se sim, o pagamento foi extornado
					else: 
						current_checkout.paid = False #Se não, simplesmente define como falso
				current_checkout.save() #Salva o pagamento
			else: #Não foi encontrado nenhum pagamento para esse usuário
				checkout = models.Checkout.objects.filter(external_ref=external_ref) #Busca por pagamento com essa ref em outros usuários
				if checkout: #Se encontrou, ignora a solicitação
					return redirect('livro1:home')
				else: #Se não, então está tudo certo, pode proceguir
					current_checkout = models.Checkout() #Cria um novo pagamento
					current_checkout.profile = profile #Define o usuário do pagamento
					current_checkout.external_ref = external_ref #Guarda a chave external_ref
					current_checkout.paymentID = payment_id.group(1) #Guarda o ID de pagamento
					current_checkout.mp_status = payment['response']['status'] #Salva o status retornado pelo MP
					if current_checkout.mp_status == "approved": #Se o pagamento foi feito
						current_checkout.paid = True #Define como True, Se não, o default é False mesmo
					current_checkout.save() #Salva o pagamento
		checkouts = profile.checkout.filter(paid=True) #Busca por pagamentos aprovados do usuário
		if checkouts:
			profile.active = True #Se encontrou, ativa a conta premium
		else:
			profile.active = False #Se não encontrou, desativa a conta premium como redundância 
		profile.save() #Salva o perfil 
		return render(request, 'adm/paymentNotification.html', {'status': payment['response']['status']}) #renderiza a página
	except:
		return redirect('livro1:payment')

@login_required #Pra fazer a compra do premium precisa estar logado no sistema
def payment(request):
	profile = request.user.profile
	checkouts = profile.checkout.all().order_by('?') #Busca todos os possíveis pagamentos vinculados ao usuário
	try:
		sdk = mercadopago.SDK("APP_USR-6199102471644452-052718-40eb8adddafc4ba83af1ad960cc0dccf-765040003")
		for c in checkouts:
			payment = sdk.payment().get(c.paymentID)
			if payment['response']['status'] == "approved":
				c.mp_status = payment['response']['status']
				c.save()
				profile.active = True
				profile.save()
	except:
		for c in checkouts:
			if c.paid:
				profile.active = True
				profile.save()
	if profile.active:
		return redirect('livro1:home')	
	try: 
		sdk = mercadopago.SDK("APP_USR-6199102471644452-052718-40eb8adddafc4ba83af1ad960cc0dccf-765040003") 
		checkout_N = request.user.profile.checkout.all().count() + 1 #Vai ver o número de compras que uma pessoa já fez e adiciona mais uma
		#Se a pessoa quis pagar por boleto, mas daí desistiu e agora quer pagar pelo cartão, o sistema gera uma referência externa diferente pra cada pagamento que o cliente fizer
		external_reference = str(request.user.profile.id)+"_R_"+str(checkout_N)+"_"+datetime.strftime(timezone.now(), '%Y-%m-%d--%H-%M-%s') #Cria a referência externa
		
		preference_data = { #Gera a preferência
			"items": [ #Os dados do item
				{
					"title": "Projeto Atitudes Premium",
					"quantity": 1,
					"unit_price": 89.80,
					"currency_id": "BRL",
				}
			],
			"back_urls": { #Configua as backurl
				#Não deixei o auto return pq eu estou usando o modo Modal do pagamento pra não precisar sair do meu site pra pagar
				"success": "https://www.play.projetoatitudes.com/index.fcgi/payment_return/"+str(request.user.profile.id)+"/"+str(external_reference)+"/",
				"failure": "https://www.play.projetoatitudes.com/index.fcgi/payment_return/"+str(request.user.profile.id)+"/"+str(external_reference)+"/",
				"pending": "https://www.play.projetoatitudes.com/index.fcgi/payment_return/"+str(request.user.profile.id)+"/"+str(external_reference)+"/"
			},
			"external_reference": external_reference, #Atribui a referência externa
			"auto_return": "approved"
		}
		preference_response = sdk.preference().create(preference_data)
		preference = preference_response["response"]
	except:
		preference = "error" #Se o try falhar, envia a string error, la no template está um tratamento para casos de erro
	orders = profile.checkout.all() #Pega a lista de todos os pagamentos que o usuário fez ou tentou fazer

	return render(request, 'adm/payment.html', {'preference':preference, 'orders' : orders}) #renderiza a página

@login_required
def library(request, id_user):
	stage = request.user.profile.stage
	profile = models.Profile.objects.get(id=id_user)
	chapter = [profile.paragraphs.filter(chapter=1).order_by('id'), profile.paragraphs.filter(chapter=2).order_by('id'), profile.paragraphs.filter(chapter=3).order_by('id'), profile.paragraphs.filter(chapter=4).order_by('id'),
		 profile.paragraphs.filter(chapter=5).order_by('id'), profile.paragraphs.filter(chapter=6).order_by('id'), profile.paragraphs.filter(chapter=7).order_by('id'), profile.paragraphs.filter(chapter=8).order_by('id'),
		 profile.paragraphs.filter(chapter=9).order_by('id'), profile.paragraphs.filter(chapter=10).order_by('id'), profile.paragraphs.filter(chapter=11).order_by('id'), profile.paragraphs.filter(chapter=12).order_by('id'),
		 profile.paragraphs.filter(chapter=13).order_by('id'), profile.paragraphs.filter(chapter=14).order_by('id'), profile.paragraphs.filter(chapter=15).order_by('id'), profile.paragraphs.filter(chapter=16).order_by('id'),
		 profile.paragraphs.filter(chapter=17).order_by('id'), profile.paragraphs.filter(chapter=18).order_by('id')]
	return render(request, 'library.html', {'stage':stage, 'chapter':chapter, 'title':profile.bookTitle})
	
@login_required
def color(request):
	stage = request.user.profile.stage
	return render(request, 'games/color.html', {'stage':stage})
@login_required
def ludo(request):
	stage = request.user.profile.stage
	return render(request, 'games/ludo.html', {'stage':stage})
@login_required
def movies(request, id_movie):
	movie = ''
	if id_movie == 1:
		movie = None
	return render(request, 'games/movies.html', {'movie':movie})

@login_required
def lesson(request, lesson, page):
	profile = request.user.profile
	profile.continues = lesson + str(page)
	profile.save()
	found = found2 = found3 = found4 = found5 =False
	if request.method == 'POST':
		form = forms.questTextForm(request.POST)
		if form.is_valid():
			text_itens = form.data['text'].split()
			try:
				qText = request.user.profile.questText.get(questNumber=text_itens[0])
			except:
				qText = models.QuestText()
			qText.profile = profile
			qText.questNumber = text_itens[0]
			qText.text = text_itens[1].replace("+", " ").replace("_", " | ").replace("#", " # ").replace("&", " & ")
			qText.save()
			return redirect('livro1:questConclude', questNumber = qText.questNumber, score = text_itens[2], lesson = lesson, page = page)
			print(qText.text)
	if lesson == 'abertura': #//////////////////////////Lição1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Sucesso')
		if profile in discovery.found.all():
			found = True
		try:
			quest1 = profile.quests.get(questNumber='1-1')
		except:
			quest1 = False
		itens = [discovery,found, quest1]	
	elif lesson == 'maneiras': #/////////////////////////Lição2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Obrigado')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Gratidão')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Sempre')
		if profile in discovery3.found.all():
			found3 = True
		discovery4 = models.Discovery.objects.get(name='Interpessoal')
		if profile in discovery4.found.all():
			found4 = True
		try:
			quest1 = profile.quests.get(questNumber='2-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='2-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='2-3')
		except:
			quest3 = False
		try:
			quest4 = profile.quests.get(questNumber='2-4')
		except:
			quest4 = False
		try:
			quest5 = profile.quests.get(questNumber='2-5')
		except:
			quest5 = False
		itens = [discovery,found,discovery2,found2,discovery3,found3,discovery4,found4, quest1,quest2,quest3,quest4,quest5]	
	elif lesson == 'familia': #/////////////////////////Lição3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Organização')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Acróstico')
		if profile in discovery2.found.all():
			found2 = True
		try:
			quest1 = profile.quests.get(questNumber='3-1')
			qText1 = profile.questText.get(questNumber='3-1').text.split()
		except:
			quest1 = False
			qText1 = False
		try:
			quest2 = profile.quests.get(questNumber='3-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='3-3')
		except:
			quest3 = False
		try:
			quest4 = profile.quests.get(questNumber='3-4')
		except:
			quest4 = False
		try:
			quest5 = profile.quests.get(questNumber='3-5')
		except:
			quest5 = False
		itens = [discovery,found, discovery2, found2, quest1, qText1, quest2, quest3, quest4, quest5]
	elif lesson == 'acordar': #/////////////////////////Lição4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Bocejar')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Cama')
		if profile in discovery2.found.all():
			found2 = True
		try:
			quest1 = profile.quests.get(questNumber='4-1')
			qText1 = profile.questText.get(questNumber='4-1').text.split()
		except:
			quest1 = False
			qText1 = False
		try:
			quest2 = profile.quests.get(questNumber='4-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='4-3')
		except:
			quest3 = False
		try:
			quest4 = profile.quests.get(questNumber='4-4')
		except:
			quest4 = False
		try:
			quest5 = profile.quests.get(questNumber='4-5')
		except:
			quest5 = False
		try:
			quest6 = profile.quests.get(questNumber='4-6')
		except:
			quest6 = False
		itens = [discovery,found,discovery2,found2, quest1, qText1, quest2, quest3, quest4, quest5, quest6]
	elif lesson == 'refeicoes': #/////////////////////////Lição5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Educação')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Refeições')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Cortesia')
		if profile in discovery3.found.all():
			found3 = True
		discovery4 = models.Discovery.objects.get(name='Palito')
		if profile in discovery4.found.all():
			found4 = True
		discovery5 = models.Discovery.objects.get(name='Buffet')
		if profile in discovery5.found.all():
			found5 = True
		try:
			quest1 = profile.quests.get(questNumber='5-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='5-2')
		except:
			quest2 = False
		itens = [discovery,found,discovery2,found2, discovery3, found3, discovery4, found4, discovery5, found5, quest1, quest2]
	elif lesson == 'caminho': #/////////////////////////Lição6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Vandalize')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Oscilação')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Principais')
		if profile in discovery3.found.all():
			found3 = True
		try:
			quest1 = profile.quests.get(questNumber='6-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='6-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='6-3')
		except:
			quest3 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, quest1, quest2, quest3]
	elif lesson == 'cumprimentos': #/////////////////////////Lição7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Curiosidade')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Cumprimento')
		if profile in discovery2.found.all():
			found2 = True
		try:
			quest1 = profile.quests.get(questNumber='7-1')
		except:
			quest1 = False
		itens = [discovery,found, discovery2, found2, quest1]
	elif lesson == 'colegas': #/////////////////////////Lição8\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Bullying')
		if profile in discovery.found.all():
			found = True
		try:
			quest1 = profile.quests.get(questNumber='8-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='8-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='8-3')
		except:
			quest3 = False
		try:
			quest4 = profile.quests.get(questNumber='8-4')
		except:
			quest4 = False
		itens = [discovery,found, quest1, quest2, quest3, quest4]
	elif lesson == 'professor': #/////////////////////////Lição9\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Vez')
		if profile in discovery.found.all():
			found = True
		try:
			quest1 = profile.quests.get(questNumber='9-1')
			qText1 = profile.questText.get(questNumber='9-1').text
		except:
			quest1 = False
			qText1 = False
		try:
			quest2 = profile.quests.get(questNumber='9-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='9-3')
		except:
			quest3 = False
		try:
			quest4 = profile.quests.get(questNumber='9-4')
			qText4 = profile.questText.get(questNumber='9-4').text
		except:
			quest4 = False
			qText4 = False
		try:
			quest5 = profile.quests.get(questNumber='9-5')
			qText5 = profile.questText.get(questNumber='9-5').text
		except:
			quest5 = False
			qText5 = False
		itens = [discovery,found,quest1,quest2,quest3,quest4,qText4,qText1,quest5,qText5]
	elif lesson == 'sala': #/////////////////////////Lição10\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Mútuo')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Funcionar')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Participe')
		if profile in discovery3.found.all():
			found3 = True
		try:
			quest1 = profile.quests.get(questNumber='10-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='10-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='10-3')
		except:
			quest3 = False
		itens = [discovery,found,discovery2,found2,discovery3,found3,quest1,quest2,quest3]
	elif lesson == 'banheiro': #/////////////////////////Lição11\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Despercebido')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Detritos')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Alheio')
		if profile in discovery3.found.all():
			found3 = True
		try:
			quest1 = profile.quests.get(questNumber='11-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='11-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='11-3')
		except:
			quest3 = False
		itens = [discovery,found,discovery2,found2,discovery3,found3,quest1,quest2,quest3]
	elif lesson == 'livros': #/////////////////////////Lição12\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Ficcional')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Micro-organismo')
		if profile in discovery2.found.all():
			found2 = True
		try:
			quest1 = profile.quests.get(questNumber='12-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='12-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='12-3')
		except:
			quest3 = False
		itens = [discovery,found, discovery2, found2 ,quest1,quest2,quest3]
	elif lesson == 'biblioteca': #/////////////////////////Lição13\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Variações')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Estatuto')
		if profile in discovery2.found.all():
			found2 = True
		try:
			quest1 = profile.quests.get(questNumber='13-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='13-2')
		except:
			quest2 = False
		itens = [discovery,found, discovery2, found2, quest1, quest2]
	elif lesson == 'computadores': #/////////////////////////Lição14\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Software')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Deletar')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Respeito-Online')
		if profile in discovery3.found.all():
			found3 = True
		try:
			quest1 = profile.quests.get(questNumber='14-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='14-2')
		except:
			quest2 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, quest1, quest2]
	elif lesson == 'teatro': #/////////////////////////Lição15\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Anfiteatro')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Proscênio')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Preservar')
		if profile in discovery3.found.all():
			found3 = True
		discovery4 = models.Discovery.objects.get(name='Aplausos')
		if profile in discovery4.found.all():
			found4 = True
		discovery5 = models.Discovery.objects.get(name='Ao_Vivo')
		if profile in discovery5.found.all():
			found5 = True
		try:
			quest1 = profile.quests.get(questNumber='15-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='15-2')
			qText2 = profile.questText.get(questNumber='15-2').text.split()
		except:
			quest2 = False
			qText2 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, discovery4, found4, discovery5, found5, quest1, quest2, qText2]
	elif lesson == 'cidade': #/////////////////////////Lição16\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Usufruir')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Atenção_na_rua')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Cidadão_responsável')
		if profile in discovery3.found.all():
			found3 = True
		try:
			quest1 = profile.quests.get(questNumber='16-1')
		except:
			quest1 = False
		try:
			quest2 = profile.quests.get(questNumber='16-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='16-3')
		except:
			quest3 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, quest1,quest2,quest3]
	elif lesson == 'especiais': #/////////////////////////Lição17\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Cumprimentos')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Cordial')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Naturalidade')
		if profile in discovery3.found.all():
			found3 = True
		discovery4 = models.Discovery.objects.get(name='Não_impor')
		if profile in discovery4.found.all():
			found4 = True
		discovery5 = models.Discovery.objects.get(name='Comunicação')
		if profile in discovery5.found.all():
			found5 = True
		try:
			quest1 = profile.quests.get(questNumber='17-1')
			qText1 = profile.questText.get(questNumber='17-1').text
		except:
			quest1 = False
			qText1 = False
		try:
			quest2 = profile.quests.get(questNumber='17-2')
		except:
			quest2 = False
		try:
			quest3 = profile.quests.get(questNumber='17-3')
		except:
			quest3 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, discovery4, found4, discovery5, found5, quest1, qText1, quest2, quest3]
	elif lesson == 'avo': #/////////////////////////Lição18\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
		discovery = models.Discovery.objects.get(name='Idoso_saudável')
		if profile in discovery.found.all():
			found = True
		discovery2 = models.Discovery.objects.get(name='Árvore_genealógica')
		if profile in discovery2.found.all():
			found2 = True
		discovery3 = models.Discovery.objects.get(name='Sancionado')
		if profile in discovery3.found.all():
			found3 = True
		discovery4 = models.Discovery.objects.get(name='Retribuir')
		if profile in discovery4.found.all():
			found4 = True
		try:
			quest1 = profile.quests.get(questNumber='18-1')
			qText1 = profile.questText.get(questNumber='18-1').text.split()
		except:
			quest1 = False
			qText1 = False
		try:
			quest2 = profile.quests.get(questNumber='18-2')
		except:
			quest2 = False
		itens = [discovery,found, discovery2, found2, discovery3, found3, discovery4, found4, quest1, qText1, quest2]
	url = 'lessons/' + lesson + '/' + str(page) + '.html'
	return render(request, url,{'itens' : itens})

@login_required
def discoveryFound(request, id_discovery, lesson, page):
	profile = request.user.profile
	discovery = models.Discovery.objects.get(id=id_discovery)
	if profile not in discovery.found.all():
		discovery.found.add(profile)
		profile.score += 30
		profile.credits += 30
		profile.stars += 1
		profile.save()
	discovery.save()
	return redirect('livro1:lesson', lesson = lesson, page = page)

@login_required
def questConclude(request, questNumber, score, lesson, page):
	profile = request.user.profile
	sticker = models.StickerBase()
	sticker.url = ''
	if questNumber == '1-1':
		sticker.url = 'img/stickers/14.png'
	if questNumber == '2-1':
		sticker.url = 'img/stickers/26.png'
	if questNumber == '2-4':
		sticker.url = 'img/stickers/16.png'
	if questNumber == '3-5':
		sticker.url = 'img/stickers/1.png'
	if questNumber == '5-2':
		sticker.url = 'img/stickers/4.png'
	if questNumber == '6-1':
		sticker.url = 'img/stickers/11.png'
	if questNumber == '9-4':
		sticker.url = 'img/stickers/13.png'
	if questNumber == '11-3':
		sticker.url = 'img/stickers/6.png'
	if questNumber == '14-1':
		sticker.url = 'img/stickers/22.png'
	if questNumber == '15-1':
		sticker.url = 'img/stickers/21.png'
	if sticker.url != '':
		sticker.profile = profile
		sticker.save()
	try:
		quest = request.user.profile.quests.get(questNumber=questNumber)
	except:
		quest = models.QuestConclude()
	quest.profile = profile
	quest.questNumber = questNumber
	quest.score = score
	quest.credits = score
	quest.save()
	profile.score += score
	profile.credits += score
	profile.likes += 1
	profile.save()
	return redirect('livro1:lesson', lesson = lesson, page = page)
	
@login_required	
def questUndo(request, questNumber, score, lesson, page):
	profile = request.user.profile
	if profile.credits < score:
		return redirect('livro1:lesson', lesson = lesson, page = page)	
	profile.score -= score
	profile.credits -= score
	profile.likes -= 1
	profile.save()
	quest = profile.quests.get(questNumber=questNumber)
	quest.delete()
	try:
		qText = profile.questText.get(questNumber=questNumber)
		qText.delete()
	except:
		qText = None
	return redirect('livro1:lesson', lesson = lesson, page = page)

@login_required	
def finishLesson(request, lesson):
	profile = request.user.profile
	if profile.stage == lesson:
		profile.stage += 1
		profile.continues = functions.lessonName(lesson+1) + '1'
		profile.save()
	return redirect('livro1:home')

@login_required
def chapter(request, lesson, id_user):
	lessonName = functions.lessonName(lesson)
	profile = models.Profile.objects.get(id=id_user)
	chapter = profile.paragraphs.filter(chapter=lesson).order_by('id')
	words = 0
	for p in chapter:
		words += len(p.paragraph)
	return render(request, 'chapter.html', {'chapter' : chapter, 'profile' : profile, 'lesson' : lesson, 'lessonName' : lessonName, 'words' : words})

@login_required
def editChapter(request, lesson, id_user):
	form = forms.editChapterForm(request.GET)
	profile = models.Profile.objects.get(id=id_user)
	if request.user.id != profile.user.id and request.user.profile.level < 3:
		return redirect('livro1:chapter', lesson = lesson, id_user = id_user)
	chapter = profile.paragraphs.filter(chapter=lesson).order_by('id')
	stickers = profile.stickers.all()	
	if request.method == 'POST':
		form = forms.editChapterForm(request.POST)
		if form.is_valid():
			data_form = form.data
			paragraph = ''
			if data_form['paragraph_id'] == '':
				paragraph = models.Book()
			else:
				paragraph = models.Book.objects.get(id=data_form['paragraph_id'])
			if 'delete_submit' in data_form:
				paragraph.delete()
			else:
				if 'sticker_submit' in data_form:
					sticker = models.StickerBase.objects.get(id=data_form['sticker_submit'])
					paragraph.paragraph = sticker.url
					paragraph.style = 'img'
					nmbr = re.search('stickers/(.*).png', sticker.url)
					paragraph.color = nmbr.group(1)
					sticker.delete()
				else:
					if data_form['paragraph'] == '':
						form.add_errors('Você precisa escrever alguma coisa antes de tentar salvar o parágrafo.')
						return render(request, 'editChapter.html', {'chapter' : chapter, 'profile' : profile, 'lesson' : lesson, 'stickers' : stickers, 'form' : form})
					paragraph.paragraph = data_form['paragraph']
					paragraph.style = data_form['style']
					paragraph.color = data_form['color']
				paragraph.chapter = lesson
				if data_form['position'] == '0':
					paragraph.position = 'sticker-left'
				else:
					paragraph.position = 'sticker-right'
				paragraph.author = profile
				paragraph.save()
			return redirect('livro1:editChapter', lesson = lesson, id_user = id_user)
	words = 0
	for p in chapter:
		words += len(p.paragraph)
	return render(request, 'editChapter.html', {'chapter' : chapter, 'profile' : profile, 'lesson' : lesson, 'stickers' : stickers, 'form' : form, 'words' : words})

@login_required
def getSticker(request, id_paragraph):
	paragraph = models.Book.objects.get(id=id_paragraph)
	profile = paragraph.author
	lesson_number = paragraph.chapter
	if request.user.id != profile.user.id and request.user.profile.level < 3:
		return redirect('livro1:chapter', lesson = lesson_number, id_user = profile.id)
	sticker = models.StickerBase()
	sticker.url = paragraph.paragraph
	sticker.profile = profile
	sticker.save()
	paragraph.delete()
	return redirect('livro1:editChapter', lesson = lesson_number, id_user = profile.id)
	
@login_required
def buySticker(request, img, id_user ,lesson_number):
	profile = models.Profile.objects.get(id=id_user)
	rProfile = request.user.profile
	if rProfile.id != profile.id and request.user.profile.level < 3:
		return redirect('livro1:chapter', lesson = lesson_number, id_user = profile.id)
	if rProfile.credits < 50:
		return redirect('livro1:chapter', lesson = lesson_number, id_user = profile.id)
	sticker = models.StickerBase()
	sticker.url = 'img/stickers/' + str(img) + '.png'
	sticker.profile = profile
	sticker.save()
	rProfile.credits -= 50
	rProfile.save()
	return redirect('livro1:editChapter', lesson = lesson_number, id_user = profile.id)

@login_required 
def admPanel(request):
	if request.user.profile.level > 3:
		return redirect('livro1:home')
	profile = request.user.profile
	school = profile.related_school
	pupils = ''
	if school:
		pupils = school.users.filter(level__gte=4)
	else:
		pupils = models.Profile.objects.filter(level=5,related_school=None)
	schools = ''
	if profile.level <= 1:
		schools = models.School.objects.all()
	return render(request, 'adm/panel.html', {'schools' : schools, 'school' : school, 'pupils' : pupils})

@login_required   
def newSchool(request):
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')	
	if request.method == 'POST':
		form = forms.newSchoolForm(request.POST)
		if form.is_valid():
			data_form = form.data
			school_exists = models.School.objects.filter(cnpj=data_form['cnpj'])
			if school_exists:
				form.add_errors('Já existe uma escola com esse CNPJ')
				return render(request, 'adm/newSchool.html', {'form' : form})
			school = models.School()
			school.name = data_form['name']
			school.description = data_form['description']
			school.cnpj = data_form['cnpj']
			school.address = data_form['address']
			school.accession = 0
			school.save()
			functions.add_log(school, 'A escola ' + school.name + ' foi cadastrada por ' + request.user.username)
			return redirect('livro1:schoolInfo', id_school = school.id)
		return render(request, 'adm/newSchool.html', {'form' : form})
	return render(request, 'adm/newSchool.html')

@login_required 
def editSchool(request, id_school):
	if request.user.profile.level > 2:
		return redirect('livro1:admPanel')	
	school = models.School.objects.get(id=id_school)
	if request.method == 'POST':
		form = forms.newSchoolForm(request.POST)
		if form.is_valid():
			data_form = form.data
			school.name = data_form['name']
			school.description = data_form['description']
			school.cnpj = data_form['cnpj']
			school.address = data_form['address']
			school.save()
			functions.add_log(school, 'A escola ' + school.name + ' foi editada por ' + request.user.username)
			return redirect('livro1:schoolInfo', id_school = school.id)
		return render(request, 'adm/newSchool.html', {'form' : form})
	return render(request, 'adm/newSchool.html', {'school' : school})
		
@login_required 	
def deleteSchool(request, id_school):
	if request.user.profile.level > 2:
		return redirect('livro1:admPanel')	
	school = models.School.objects.get(id=id_school)
	profiles = models.Profile.objects.filter(related_school = school)
	for p in profiles:
		if p.level <= 1:
			p.related_school = None
			p.save()
		else:
			user = p.user
			savedBook = models.SavedBook.objects.filter(author=p)
			if not savedBook:
				user.delete()
	school.delete()
	return redirect('livro1:admPanel')

@login_required 
def schoolInfo(request, id_school):
	school = models.School.objects.get(id=id_school)
	users = school.users.filter(level__lte = 3)
	pupils = school.users.filter(level__gte=4)
	return render(request, 'adm/schoolInfo.html', {'school' : school, 'users' : users, 'pupils': pupils})
	
@login_required
def admSchool(request, id_school):
	profile = request.user.profile
	if profile.level <= 1:
		school = models.School.objects.get(id=id_school)
		if profile.related_school == school:
			profile.related_school = None
		else:
			profile.related_school = school
		profile.save()
	return redirect('livro1:schoolInfo', id_school = id_school)

def newUser(request, id_school):
	schools = school = ''
	user = request.user
	if user.username == '':
		schools = models.School.objects.order_by('name')
	else:
		if user.profile.level > 3:
			return redirect('livro1:home')
		if id_school == 0:
			school = user.profile.related_school
		else:
			school = models.School.objects.get(id=id_school)
	if request.method == 'POST':
		form = forms.newUserForm(request.POST)
		if form.is_valid():
			data_form = form.data
			newProfile = models.Profile()
			newProfile.level = int(data_form['level'])
			if newProfile.level <= 3 & newProfile.level > 1:
				if school.accession <= 0:
					form.add_errors('Essa escola não tem acessos disponíveis. Compre mais acessos para cadastrar novos usuários')
					return render(request, 'adm/newUser.html', {'schools' : schools, 'school' : school, 'form' : form})
				else:
					newProfile.active = True;
					school.accession -= 1;
					school.save()
			newUser = User.objects.create_user(data_form['username'], data_form['email'], data_form['password'])
			newUser.first_name = data_form['first_name']
			newUser.last_name = data_form['last_name']
			newUser.save()
			newProfile.user = newUser
			if newProfile.level < 5:
				if user.username == '':
					newProfile.related_school = models.School.objects.get(id=data_form['related_school'])
					newProfile.answerable = models.Profile.objects.get(id=data_form['answerable'])
				else:
					newProfile.related_school = school
					newProfile.answerable = user.profile
				if newProfile.level == 4:
					newStudent = models.Student()
					newStudent.class_number = data_form['class_number']
					newStudent.class_year = data_form['class_year']
					newStudent.save()
					newProfile.student = newStudent
			else:
				newSponsor = models.Sponsor()
				newSponsor.name = data_form['sponsor_name']
				newSponsor.relationship = data_form['sponsor_relationship']
				newSponsor.email = data_form['sponsor_email']
				newSponsor.save()
				newProfile.sponsor = newSponsor
			newProfile.save()
			avatar = models.AvatarHub()
			avatar.profile = newProfile
			avatar.save()
			if newProfile.level < 5 & newProfile.level > 1:
				if user.username == '':
					functions.add_log(newProfile.related_school, newProfile.user.first_name + ' Acabou de se cadastrar na escola')
				else:
					functions.add_log(newProfile.related_school, user.first_name + ' Acabou de cadastrar ' + newProfile.user.first_name + ' na escola')
				if newProfile.level == 4:
					functions.add_log(newProfile.related_school, newProfile.user.first_name + ' precisa ter sua conta ativada pelo educador responsável')
			#return redirect('livro1:profileInfo', id_profile = newProfile.id)
			if user.username == '':
				return redirect('livro1:congrats')
			return redirect('livro1:userInfo', id_user = newProfile.id)
		return render(request, 'adm/newUser.html', {'schools' : schools, 'school' : school, 'form' : form})
	return render(request, 'adm/newUser.html', {'schools' : schools, 'school' : school})

@login_required 	
def userInfo(request, id_user): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	return render(request, 'user/info.html', {'profile' : profile})

@login_required
def saveBook(request, id_user, rating): 
	print('TO AQUI Ó')
	profile = models.Profile.objects.get(id=id_user)
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')
	if profile.stage == 21:
		print('21 aqui ó rapá, ma vai perder lvl')
		savedBook = models.SavedBook.objects.filter(author=profile)
		if savedBook:
			delBook = models.SavedBook.objects.get(author=profile)
			delBook.delete()
			profile.stage = 20
	elif profile.stage == 20:
		print('20 aqui ó rapá, ma vai ganhar lvl')
		savedBook = models.SavedBook.objects.filter(author=profile)
		if not savedBook:
			newSavedBook = models.SavedBook()
			newSavedBook.author = profile
			newSavedBook.rating
			newSavedBook.save()
			profile.stage = 21
	profile.save()
	return redirect('livro1:userInfo', id_user = id_user)
	
@login_required	
def activateUser(request, id_user): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	if request.user.profile.level <= 3:
		school = profile.related_school
		if school:
			if school.accession > 0:
				school.accession -=1
				profile.active = True
				school.save()
				profile.save()
		else:
			if request.user.profile.level <= 1:
				profile.active = True
				profile.save()
	return redirect('livro1:userInfo', id_user = id_user)

@login_required 	
def deleteUser(request, id_user):
	profile = models.Profile.objects.get(id=id_user)
	if request.user.profile.level > 2 and profile != request.user.profile:
		return redirect('livro1:home')	
	user = profile.user
	user.delete()
	return redirect('livro1:home')

@login_required 
def changeAvatar(request, id_user): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	avatars = models.Avatar.objects.filter(breed__gt=0).order_by('breed', 'price')
	backgrounds = models.Avatar.objects.filter(breed=0)
	acquired = profile.avatar.acquired.all()
	return render(request, 'user/changeAvatar.html', {'profile' : profile, 'avatars' : avatars, 'backgrounds' : backgrounds, 'acquired' : acquired})
	
@login_required 
def setAvatar(request, id_user, id_avatar, id_bg, price): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	if request.user.profile != profile and request.user.profile.level > 3:
		return redirect('livro1:changeAvatar', id_user = id_user) 
	profile_avatar = profile.avatar
	if id_avatar == 0:
		profile_avatar.active = 'img/avatars/default.jpg'
	else:
		avatar = models.Avatar.objects.get(id=id_avatar)
		profile_avatar.active = avatar.url
		if avatar not in profile_avatar.acquired.all():
			profile_avatar.acquired.add(avatar)
	if id_bg == 0:
		profile_avatar.background = 'img/avatars/0/1.jpg'
	else:
		background = models.Avatar.objects.get(id=id_bg)
		profile_avatar.background = background.url
		if background not in profile_avatar.acquired.all():
			profile_avatar.acquired.add(background)
	profile.credits -= price
	profile.save()
	
	
	profile_avatar.save()
	return redirect('livro1:changeAvatar', id_user = id_user) 
	
@login_required
def deactivateUser(request, id_user): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	if request.user.profile.level <= 3:
		profile.active = False
		profile.save()
	return redirect('livro1:userInfo', id_user = id_user)
	
@login_required
def editUser(request, id_user): #id_user = profile.user.id
	user = User.objects.get(id=id_user)
	if request.method == 'POST':
		form = forms.editUserForm(request.POST)
		if form.is_valid():
			data_form = form.data
			if data_form['username'] != '':
				user.username = data_form['username']
			if data_form['first_name'] != '':
				user.first_name = data_form['first_name']
			if data_form['last_name'] != '':
				user.last_name = data_form['last_name']
			if data_form['email'] != '':
				user.email = data_form['email']
			user.save()
			return redirect('livro1:userInfo', id_user = user.profile.id)
		return render(request, 'user/editUser.html', {'user' : user, 'form' : form})
	return render(request, 'user/editUser.html', {'user' : user})
	
@login_required
def editPassword(request, id_user): #id_user = profile.user.id
	user = User.objects.get(id=id_user)
	if request.method == 'POST':
		form = forms.editPasswordForm(request.POST)
		if form.is_valid(request.user.username):
			data_form = form.data
			user.set_password(data_form['password'])
			user.save()
			return redirect('livro1:userInfo', id_user = user.profile.id)
		return render(request, 'user/editPassword.html', {'user' : user, 'form' : form})
	return render(request, 'user/editPassword.html', {'user' : user})
	
@login_required
def editRelated(request, id_user): #id_user = profile.id
	profile = models.Profile.objects.get(id=id_user)
	if request.method == 'POST':
		form = forms.editRelatedForm(request.POST)
		if form.is_valid():
			data_form = form.data
			if profile.related_school:
				student = profile.student
				if data_form['class_number'] != '':
					student.class_number = data_form['class_number']
				if data_form['class_year'] != '':
					student.class_year = data_form['class_year']
				student.save()
			else:
				sponsor = profile.sponsor
				if data_form['sponsor_name'] != '':
					sponsor.name = data_form['sponsor_name']
				if data_form['sponsor_relationship'] != '':
					sponsor.relationship = data_form['sponsor_relationship']
				if data_form['sponsor_email'] != '':
					sponsor.email = data_form['sponsor_email']
				sponsor.save()
			return redirect('livro1:userInfo', id_user = id_user)
		return render(request, 'user/editRelated.html', {'profile' : profile, 'form' : form})
	return render(request, 'user/editRelated.html', {'profile' : profile})
	
@login_required
def userList(request,id_school): 
	profile = request.user.profile
	users = school = pupils = False
	if profile.level > 1:
		return redirect('livro1:admPanel')
	schools = models.School.objects.all()
	if id_school == 0:
		users = models.Profile.objects.filter(level__lte=1,related_school=None)
	else:
		school = models.School.objects.get(id=id_school)
		users = models.Profile.objects.filter(level__lte=1, related_school=school)
	if school:
		pupils = school.users.filter(level__gte=4)
	else:
		pupils = models.Profile.objects.filter(level=5,related_school=None)
	return render(request, 'adm/userList.html', {'users' : users, 'school' : school, 'pupils' : pupils, 'schools' : schools})
	
@login_required
def listInterative(request, active): 
	profiles = None
	users = school = pupils = False
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')
	if active != 0:
		profiles = models.Profile.objects.filter(stage__gte=20)
	else:
		profiles = models.Profile.objects.filter(active=False).order_by('id')
	return render(request, 'adm/listInterative.html', {'profiles' : profiles})
	
@login_required
def addAccession(request,id_school, accession): 
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')
	school = models.School.objects.get(id=id_school)
	school.accession += accession
	school.save()
	return redirect('livro1:schoolInfo', id_school = id_school)

@login_required	
def finish(request):
	if request.user.profile.stage < 19:
		return redirect('livro1:home')
	profile = request.user.profile
	profile.continues = 'finish1'
	profile.save()
	if request.method == 'POST':
		form = forms.addTitle(request.POST)
		if form.is_valid():
			data_form = form.data
			profile.bookTitle = data_form['title']
			profile.save()
			return redirect('livro1:finish')
		return render(request, 'finish.html', {'form' : form})
	return render(request, 'finish.html')

def printBook(request, id_user):
	profile = models.Profile.objects.get(id=id_user)
	chapter = [profile.paragraphs.filter(chapter=1).order_by('id'), profile.paragraphs.filter(chapter=2).order_by('id'), profile.paragraphs.filter(chapter=3).order_by('id'), profile.paragraphs.filter(chapter=4).order_by('id'),
		 profile.paragraphs.filter(chapter=5).order_by('id'), profile.paragraphs.filter(chapter=6).order_by('id'), profile.paragraphs.filter(chapter=7).order_by('id'), profile.paragraphs.filter(chapter=8).order_by('id'),
		 profile.paragraphs.filter(chapter=9).order_by('id'), profile.paragraphs.filter(chapter=10).order_by('id'), profile.paragraphs.filter(chapter=11).order_by('id'), profile.paragraphs.filter(chapter=12).order_by('id'),
		 profile.paragraphs.filter(chapter=13).order_by('id'), profile.paragraphs.filter(chapter=14).order_by('id'), profile.paragraphs.filter(chapter=15).order_by('id'), profile.paragraphs.filter(chapter=16).order_by('id'),
		 profile.paragraphs.filter(chapter=17).order_by('id'), profile.paragraphs.filter(chapter=18).order_by('id')]
	return render(request, 'library2pdf.html', {'profile':profile, 'chapter':chapter})

@login_required   
def addRating(request):
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')
	ratings = models.Rating.objects.all().order_by('-id')
	if request.method == 'POST':
		form = forms.addRatingForm(request.POST)
		if form.is_valid():
			data_form = form.data
			rating = models.Rating()
			rating.testimony = data_form['testimony']
			rating.author = data_form['author']
			rating.date = data_form['date']
			rating.address = data_form['address']
			rating.save()
			return redirect('livro1:addRating')
		return render(request, 'adm/addRating.html', {'ratings' : ratings, 'form' : form})
	return render(request, 'adm/addRating.html', {'ratings' : ratings})
	
@login_required   
def delRating(request, id_rating):
	if request.user.profile.level > 1:
		return redirect('livro1:admPanel')	
	try:
		rating = models.Rating.objects.get(id=id_rating)
		rating.delete()
	except:
		pass
	return redirect('livro1:addRating')

@login_required 	
def resetProfile(request, id_user): #id_user = profile.id
	if request.user.profile.level > 1:
		return redirect('livro1:home')
	profile = models.Profile.objects.get(id=id_user)
	quests = profile.quests.all()
	for q in quests:
		q.delete()
	qText = profile.questText.all()
	for qt in qText:
		qt.delete()
	profile.stage = 1
	profile.save()
	return redirect('livro1:userInfo', id_user = id_user)