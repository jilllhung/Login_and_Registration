from django.shortcuts import render, redirect
from login_app.models import User
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    return render(request, "index.html")


def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user" : User.objects.get(id = request.session["user_id"])
        }
        return render(request, "success.html", context)

def register(request):
    print(request.POST)
    #possible errors for register
    errors = User.objects.basic_validator(request.POST)
    if len(request.POST["first_name"]) < 2:
        errors["first_name"] = "First Name should be at least 2 characters"
    if len(request.POST["last_name"]) < 2:
        errors["last_name"] = "Last Name should be at least 2 characters"
    if User.objects.filter(email = request.POST["email"]): #if list not empty
        errors['email_exist'] = "Email already has an associated account"
    if request.POST["password"] != request.POST["confirm_pw"]:
        errors["password_match"] = "Password don't match"
    if request.POST["birthday"] == "":
        errors["birthday_input"] = "Birthday is required" 
    else:
        birthday_datetime = datetime.strptime(request.POST["birthday"], '%Y-%m-%d')
        today_datetime = datetime.today()
        if (today_datetime.year - birthday_datetime.year) < 13:
            errors["birthday"] = "You must be older than 13 to register"
        elif (today_datetime.year - birthday_datetime.year) == 13:
            if (today_datetime.month < birthday_datetime.month):
                errors["birthday"] = "You must be older than 13 to register"
            elif (today_datetime.month == birthday_datetime.month) and (today_datetime.day < birthday_datetime.day):
                errors["birthday"] = "You must be older than 13 to register"

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        #hash password
        hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        #create new user
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            birthday = request.POST["birthday"],
            password = hashed_pw,
        )
        print(new_user)
        #update_session
        request.session['user_id'] = new_user.id
        request.session['which_form'] = "registered"
        return redirect("/success")

def login(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    #confirm user email exist
    user_with_this_email = User.objects.filter(email = request.POST["email"]) #returns an empty list if email not in db
    if user_with_this_email: #if not an empty list
        logged_user = user_with_this_email[0]
        #match password
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            #update_session
            request.session['user_id'] = logged_user.id
            request.session['which_form'] = "logged in"
            return redirect("/success")

    errors["incorrect"] = "The email or password is incorrect."
    for key, value in errors.items():
        messages.error(request, value)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")