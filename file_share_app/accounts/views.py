from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.forms import StudentForm
from accounts.models import *
from django.contrib.auth.decorators import login_required
from accounts.models import Filedb
import requests 
import os
import mimetypes
import io
from django.http import FileResponse



# Create your views here.

def home_view(request):
	return render(request, 'accounts/home.html')


def login_view(request):
	if request.method == 'POST':
		user = auth.authenticate(username = request.POST['username'], password= request.POST['password'])
		if user is not None:
			auth.login(request, user)
			return redirect('book_list_view')
		else:
			return render(request, 'accounts/login.html', {'error':'usrname or password is incorrect'})

	else:

		return render(request, "accounts/login.html")


def signup_view(request):
	if request.method == 'POST':
		if request.POST['password'] == request.POST['confirm_password']:
			try:
				User.objects.get(username=request.POST['username'])  # id user not exists it will raise exception
				return render(request,'accounts/signup.html', {'error':'user already exists'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
				auth.login(request, user)
				return redirect('book_list_view')
		else:
			return render(request,'accounts/signup.html', {'error' : 'password does not match'})	

	else:
		return render(request, "accounts/signup.html")

def logout_view(request):
	if request.method == 'POST':
		auth.logout(request)
		return redirect('home_view')


@login_required(login_url='/login')
def upload_view(request):
	if request.method == 'POST':
		if request.POST.get('title') and len(request.FILES)!=0:
			user_form = StudentForm(request.POST, request.FILES)
			if user_form.is_valid():
				
				file_type = request.POST.get('description')
				print("description2..",request.FILES['file'].name)
				file_name  = request.FILES['file'].name
				file_extention = file_name.split('.')
				print("file_extention",file_extention)
				print("file_type",file_type)
				msg2 = ""
				if len(file_extention) == 1 and file_type != 'file':
					print("single")
					msg2 = "File is without extension. So try to upload with file type"
				elif( len(file_extention) > 1 and (file_extention[1] == 'mp4' or file_extention[1] == '3gp') and file_type != 'video'):
					print("video")
					msg2 = "check the file type field and type of  file that you want to upload "	
				elif(len(file_extention) > 1 and file_extention[1]  in ['txt','zip','tar','py','c','csv','java','cpp','png','jpg','gif','jpeg'] and file_type !='file' ):
					print("txet")
					msg2 = "check the file type field and type of  file that you want to upload "	
				elif(len(file_extention) > 1 and file_extention[1] in ['mp3'] and file_type != 'mp3'):
					print("mp3")
					msg2 = "check the file type field and type of  file that you want to upload "	
				elif(len(file_extention) > 1 and file_extention[1] in ['pdf'] and file_type != 'pdf'):
					print("pdf")
					msg2 = "check the file type field and type of  file that you want to upload "	
				if not msg2:
					user_form_instance = user_form.save(commit=False)
					user_form_instance.user = request.user
					user_form_instance.save()
					form = StudentForm()
					msg1 = {
					"form":form,
					"msg":"file upload successfully",}
					return render(request, 'accounts/upload.html',msg1) 
				else:
					form = StudentForm()
					msg1 = {
					"form":form,
					"msg":msg2,}
					return render(request, 'accounts/upload.html',msg1) 
		else:
			form = StudentForm()
			msg1 = {
			    "form":form,
				"msg":"please fill the title and author and file   are mendetory",}
			return render(request,"accounts/upload.html",msg1)
	else:
		form = StudentForm()
		return render(request,"accounts/upload.html",{"form":form})
		# return HttpResponse("satish failes")


@login_required(login_url='/login')
def book_list_view(request):
    books = Filedb.objects.all()
    return render(request, 'accounts/book_list.html', {
        'books': books
    })

@login_required(login_url='/login')
def book_list_view_by_other(request):
    books = Filedb.objects.exclude(user = request.user)
    return render(request, 'accounts/book_list.html', {
        'books': books
    })

@login_required(login_url='/login')
def book_list_view_by_u(request):
    books = Filedb.objects.filter(user = request.user)
    return render(request, 'accounts/book_list.html', {
        'books': books
    })


@login_required(login_url='/login')
def delete_view(request, pk):
	if request.method == 'POST':
		book = Filedb.objects.get(pk=pk)
		book.delete()
		return redirect('book_list_view')

def pdfdownloader_view(request, file_name):
	response = HttpResponse(content_type='application/pdf')
	response['content_type'] = 'application/pdf'
	response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
	path = "/home/satish/satish_education/django/file_share_app/file_share_app/file_share_project/media/books/pdfs/" + file_name
	print(path)
	with open(path, 'rb') as pdf:
		response = HttpResponse(pdf.read())
		response['content_type'] = 'application/pdf'
		response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
		return response

def mp3downloader_view(request,filename):
    path='/home/satish/satish_education/django/file_share_app/file_share_app/file_share_project/media/books/pdfs/' + filename
    f = open(path,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/mpeg'
    response['Content-Length'] =os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


def mp4downloader_view(request, filename):
    path = "/home/satish/satish_education/django/file_share_app/file_share_app/file_share_project/media/books/pdfs/" + filename
    f = open(path,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='video/mp4'
    response['Content-Length'] =os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename=filename.mp4'
    return response

def imagedownloader_view(request, filename):
    path = "/home/satish/satish_education/django/file_share_app/file_share_app/file_share_project/media/books/pdfs/" + filename
    f = open(path,"rb") 
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='image/jpeg'
    response['Content-Length'] =os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response

def all_downloader_view(request, filename):
    path = "/home/satish/django_file_share_app/File_Share_Application/file_share_app/media/books/pdfs/" + filename
    f = open(path,"rb") 
    print("path",path)
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] =mimetypes.guess_type(filename)[0]
    response['Content-Length'] =os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


def getFile(request):
	if request.method == 'POST':
		f_name1 = request.session.get('f_name1')
		if not f_name1:
			f_name1 = request.POST['name']
		request.session['f_name1'] = f_name1
		print("name",request.session.get('f_name1'))
		return HttpResponse("kk")
	else:
		f_name1 = request.session.get('f_name1')
		f_name1 = f_name1.split('/')[-1]
		print("file_name",f_name1)
		pdf_file_name = f_name1
		res = all_downloader_view(request,pdf_file_name)
		del request.session['f_name1']
		return res

	



