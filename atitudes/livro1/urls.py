"""

    URLS LIVRO-1

"""
app_name = 'livro1'
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, logout_then_login

urlpatterns = [
	
	#index
    path('', views.index, name='index'),
    path('Biblioteca/', views.about, name='about'),
    path('Privacy/', views.privacy, name='privacy'),
    path('Suport/', views.suport, name='suport'),
    path('prototyping/', views.prototyping, name='prototyping'),
    path('congrats/', views.congrats, name='congrats'), #congrats pela conclusão da conta. 
	
	#inside
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', logout_then_login, {'login_url' : '/login/'}, name='logout'),
	path('home/', views.home, name='home'),
	path('library/<int:id_user>/', views.library, name='library'),
	path('lesson/<slug:lesson>/<int:page>/', views.lesson, name='lesson'),
	path('discoveryFound/<int:id_discovery>/<slug:lesson>/<int:page>/', views.discoveryFound, name='discoveryFound'),
	path('questConclude/<slug:questNumber>/<int:score>/<slug:lesson>/<int:page>/', views.questConclude, name='questConclude'),
	path('questUndo/<slug:questNumber>/<int:score>/<slug:lesson>/<int:page>/', views.questUndo, name='questUndo'),
	path('finishLesson/<int:lesson>/', views.finishLesson, name='finishLesson'),
	path('Finish/', views.finish, name='finish'),
	path('PrintBook/<int:id_user>/', views.printBook, name="printBook"),
	path('Continues/', views.continues, name="continues"),
	
	path('colorBook/', views.color, name='color'),
	path('recyclingLudo/', views.ludo, name='ludo'),
	path('Movies/<int:id_movie>/', views.movies, name='movies'),
	
	path('iframe/<int:item>/', views.iframe, name='iframe'),

	#book
	path('chapter/<int:lesson>/<int:id_user>/', views.chapter, name='chapter'),
	path('editChapter/<int:lesson>/<int:id_user>/', views.editChapter, name='editChapter'),
	path('getSticker/<int:id_paragraph>/', views.getSticker, name='getSticker'),
	path('buySticker/<int:img>/<int:id_user>/<int:lesson_number>/', views.buySticker, name='buySticker'),
	
	#adm
	path('adm/Panel/', views.admPanel, name='admPanel'),
	path('adm/NewSchool/', views.newSchool, name="newSchool"),
	path('adm/EditSchool/<int:id_school>/', views.editSchool, name="editSchool"),
	path('adm/DeleteSchool/<int:id_school>/', views.deleteSchool, name="deleteSchool"),
	path('adm/School/<int:id_school>/', views.schoolInfo, name='schoolInfo'),
	path('adm/AdmSchool/<int:id_school>/', views.admSchool, name='admSchool'),
	path('adm/NewUser/<int:id_school>/', views.newUser, name='newUser'),
	path('adm/UserList/<int:id_school>/', views.userList, name='userList'),
	path('adm/listInterative/<int:active>/', views.listInterative, name='listInterative'),
	path('adm/addAccession/<int:id_school>/<int:accession>/', views.addAccession, name='addAccession'),
	path('adm/addRating/', views.addRating, name="addRating"),
	path('adm/delRating/<int:id_rating>/', views.delRating, name="delRating"),
	path('adm/saveBook/<int:id_user>/<int:rating>', views.saveBook, name="saveBook"),
	path('premium/', views.payment, name="payment"),
	path('payment_return/<int:id_profile>/<slug:external_ref>/', views.payment_return, name="payment_return"),
	path('payment_notification/', views.payment_notification, name="payment_notification"),
	
	#user
	path('UserInfo/<int:id_user>/', views.userInfo, name='userInfo'),
	path('ResetProfile/<int:id_user>/', views.resetProfile, name='resetProfile'),
	path('adm/ActivateUser/<int:id_user>/', views.activateUser, name='activateUser'),
	path('adm/DeactivateUser/<int:id_user>/', views.deactivateUser, name='deactivateUser'),
	path('user/edit/<int:id_user>/', views.editUser, name='editUser'),
	path('user/editPassword/<int:id_user>/', views.editPassword, name='editPassword'),
	path('user/editRelated/<int:id_user>/', views.editRelated, name='editRelated'),
	path('user/changeAvatar/<int:id_user>/', views.changeAvatar, name='changeAvatar'),
	path('user/setAvatar/<int:id_user>/<int:id_avatar>/<int:id_bg>/<int:price>/', views.setAvatar, name='setAvatar'),
	path('adm/DeleteUser/<int:id_user>/', views.deleteUser, name="deleteUser"),
	
]
