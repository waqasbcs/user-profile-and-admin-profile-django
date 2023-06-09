from django.shortcuts import render,HttpResponseRedirect
from . forms import signupform, edituserprofileform,editadminprofileform
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        fm=signupform(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'user has been register.')
    else:
     fm=signupform()
    return render(request,'enroll/signup.html',{'form':fm})

# user login fuction
def user_login(request):
    if request.method =="POST":
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,'logged in successfully !!!')
                return HttpResponseRedirect('/profile/')
    else:
      fm = AuthenticationForm()
    return render(request,'enroll/userlogin.html',{'form':fm})
  
#profile
def user_profile(request):
  if request.user.is_authenticated:
    if request.method == "POST":
       if request.user.is_superuser== True:
          fm =editadminprofileform(request.POST,instance=request.user)
          users = User.objects.all()
       else:   
        fm = edituserprofileform(request.POST,instance=request.user)
        users = None
       if fm.is_valid():
          messages.success(request,'profile has been updated successfully!!!')
          fm.save()
    else:
      if request.user.is_superuser ==True:
         fm = editadminprofileform(instance=request.user)
         users = User.objects.all()  
      else:                    
        fm=edituserprofileform(instance=request.user)
        users = None
    return render(request,'enroll/profile.html',{'name':request.user,'form':fm,'users':users})
  else:
     return HttpResponseRedirect('/login/')
     

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

#password change with old password

def user_changepass(request):
     if request.user.is_authenticated:
      if request.method == "POST":
         fm=PasswordChangeForm(user=request.user,data=request.POST)
         if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'password change successfully')
            return HttpResponseRedirect('/profile/')
      else:           
        fm = PasswordChangeForm(user=request.user)
      return render(request,'enroll/changepass.html',{'form':fm})
     else:
       return HttpResponseRedirect('/login/')
   
   
#password change without old password

def user_changepass1(request):
     if request.user.is_authenticated:
      if request.method == "POST":
         fm=SetPasswordForm(user=request.user,data=request.POST)
         if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'password change successfully')
            return HttpResponseRedirect('/profile/')
      else:           
        fm = SetPasswordForm(user=request.user)
      return render(request,'enroll/changepass.html',{'form':fm})
     else:
       return HttpResponseRedirect('/login/')
     
    #user detail
    
def user_detail(request,id):
    if request.user.is_authenticated:
     pi = User.objects.get(pk=id)
     fm = editadminprofileform(instance=pi)
     return render(request,'enroll/userdetail.html', {'form':fm})
    else:
     return HttpResponseRedirect('/login/')
  

