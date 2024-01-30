from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.utils import timezone
import datetime

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #usuario (user auth)
	related_school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, related_name='users') #A qual grupo pertence
	level = models.IntegerField(null=False) #Qual o nível de hierarquia.  0-Eu 1-ADM 2-diretor 3-professor 4-aluno 5-cliente
	active = models.BooleanField(default=False) #Deve ficar ativo quando o pagamento foi efetuado
	answerable = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True) #O perfil que cadastrou o usuaŕio atual
	score = models.IntegerField(null=False, default=0) #pontuação do usuário
	credits = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0) #dinheiro do usuário
	stars = models.IntegerField(null=False, default=0) #medalhas de estrela
	likes = models.IntegerField(null=False, default=0) #troféu joinha
	student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='profile', null=True) #Dados de estudante
	sponsor = models.OneToOneField('Sponsor', on_delete=models.CASCADE, related_name='profile', null=True) #Dados do responsável
	stage = models.IntegerField(null=False, default=1) #Fase do usuário
	bookTitle = models.CharField(max_length=100, null=True) #Título do livro
	continues = models.CharField(max_length=20, null=False, default='abertura1') #Continuar a(ou próxima) lição

class Checkout(models.Model):
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='checkout') #Perfil relacionado
	external_ref = models.CharField(max_length=100, null=False) #Valor da referência do checkout
	paymentID = models.CharField(max_length=100, null=False) #Id do pagamento no mercado pago
	mp_status = models.CharField(max_length=100, null=False, default='refused') #Ultimo status enviado pelo MP
	paid = models.BooleanField(default=False) #Se o pagamento foi efetuado. True - Pago | False - Em espera | None - cancelado

# Pessoas que se inscreveram com interesse em adquirir o produto
class WishingRegistred(models.Model):
	name = models.CharField(max_length=100, null=False) #Nome da pessoa cadastrada
	email = models.EmailField(max_length = 254) #Email da pessoa cadastrada
	phone = models.CharField(max_length=100, null=False) #Telefone da pessoa cadastrada

class SavedBook(models.Model):
	author = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False) #Autor do parágrafo
	rating = models.IntegerField(default=1) #Avaliação. (1 = R	uim | 5 = Bom)

class AvatarHub(models.Model):
	profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='avatar') #Perfil relacionado
	active = models.CharField(max_length=255, default='/img/avatars/default.jpg', null=False) #Avatar atual
	background = models.CharField(max_length=255, default='/img/avatars/0/1.jpg', null=False) #Background atual
	acquired = models.ManyToManyField('Avatar')

class Avatar(models.Model):
	name = models.CharField(max_length=100, null=False) #Nome do avatar
	url = models.CharField(max_length=255, null=False) #endereço do avatar
	price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0) #Valor
	breed = models.IntegerField(null=False, default=0) #Qual o tipo do avatar | 0 = background | >0 = personagem

class School(models.Model):
	name = models.CharField(max_length=255, null=False) #Nome da escola
	description = models.CharField(max_length=255, null=False) #detalhes sobre a escola
	cnpj = models.CharField(max_length=50, null=False) #cnpj da escola
	foundation_date = models.DateTimeField(default=make_aware(datetime.datetime.now())) #data do cadastro
	address = models.CharField(max_length=255, null=False) #endereço da escola
	accession = models.IntegerField(default=0) #acessos disponíveis para novas contas de alunos
	log = models.TextField() #Campo para relatório

class Student(models.Model):
	class_number = models.CharField(max_length=5, null=False) #numero da turma
	class_year = models.IntegerField(null=False) #ano (série)
	
class Sponsor(models.Model):
	name = models.CharField(max_length=255, null=False) #Nome do adulto responsável
	relationship = models.CharField(max_length=255, null=False) #relação com o responsável
	email = models.EmailField(max_length = 254) #Email do responsável

class Book(models.Model):
	paragraph = models.CharField(max_length=255, null=False) #Texto do parágrafo
	chapter = models.IntegerField(null=False, default=0) #A qual capítulo pertence
	style = models.CharField(max_length=10, null=False) #Estilo do texto
	color = models.CharField(max_length=12, null=False) #Cor do texto
	position = models.CharField(max_length=15, null=False) #alinhamento da figurinha
	author = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='paragraphs') #Autor do parágrafo

class StickerBase(models.Model):
	url = models.CharField(max_length=255, null=False) #Texto do parágrafo
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='stickers') #Autor do parágrafo
	
class Discovery(models.Model):
	name = models.CharField(max_length=25, null=False)
	text = models.CharField(max_length=255, null=False)
	sort = models.CharField(max_length=25, null=False) #Glossário, observando, etc (tiop)
	found = models.ManyToManyField(Profile)
	
class QuestConclude(models.Model):
	questNumber = models.CharField(max_length=25, null=False) # X-X  O primeiro número é a lição e o segundo é o número da atividade
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='quests') #usuário
	score = models.IntegerField(null=False, default=0) #pontuação
	credits = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0) #dinheiro
	
class QuestText(models.Model):
	questNumber = models.CharField(max_length=25, null=False) # X-X  O primeiro número é a lição e o segundo é o número da atividade
	profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='questText') #usuário
	text = models.CharField(max_length=255, null=False) #O texto

class Rating(models.Model):
	testimony = models.CharField(max_length=255, null=False)
	author = models.CharField(max_length=50, null=False)
	date = models.DateField(default=make_aware(datetime.datetime.now()))
	address = models.CharField(max_length=100, null=True)
