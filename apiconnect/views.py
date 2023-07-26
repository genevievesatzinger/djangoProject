from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import urllib.parse
from .parseXML import XmlDictConfig
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required



def login_page(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        # get email and username
        email = request.POST.get('email')
        username = request.POST.get('username').lower()

        # check if user exists
        try:
            user = User.objects.get(username=username)
        except:
            # implement message from django
            messages.error(request, "User does not exist.")
            # add in message syntax to navbar to display message

        # if user exists, check credentials
        # get user object based on email and username
        user = authenticate(request, email=email, username=username)

        # log user in
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email or username does not exist.")

    context = {"page": page}
    return render(request, "apiconnect/login_register.html", context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Saving and freezing form to access user that is created
            # Making sure name is clean (no accidental caps etc.)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Now that user is registered, login and redirect user
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error occurred while creating your account.')

    return render(request, 'apiconnect/login_register.html', {'form':form})

# Code for restricting pages before login
# What pages do we want to restrict while the user is not logged in?
# Or just certain pieces of a page? Like in the results page - "save"
# Add this decorator before url function

# @login_required(login_url='/login')

# if request.user != page.host:
#     return HttpResponse("Login to your account to access this page.")


def home(request):
    return render(request, 'apiconnect/home.html')


def results(request):

    if request.method == 'POST':
        search_query = ''
        result_rnk = 1
        try:
            search_query = request.POST['search_query']
            result_rnk = int(request.POST['result_rnk'])
        except:
            search_query = createSearch(request.POST)
        url_query = createURL(search_query, result_rnk)    
        response_xml = getData(url_query)
        context = toDict(response_xml)
        context.update({'search_query': search_query})
        min_rnk = int(context['MinRank'])
        max_rnk = int(context['MaxRank'])
        num_studies = int(context['NStudiesFound'])
        if min_rnk > 1:           
            context.update({'pre_rank': min_rnk - 10 if min_rnk > 10 else 1})
            print('pre_rank: ', context['pre_rank'])
        if max_rnk < num_studies:                        
            context.update({'next_rank': min_rnk + 10})
            print('next_rank: ', context['next_rank'])
        
        return render(request, 'apiconnect/results.html', context)


    for field in context['StudyFieldsList']['StudyFields']:
        print(field)

    return render(request, 'apiconnect/results.html', context)


def createSearch(reqForm):
    
    searchQ = "" # Reset searchQ

    condition = reqForm['conditionSearch']
    country = reqForm['countryFilter']
    state = reqForm['stateFilter']
    city = reqForm['cityFilter']
    range = reqForm['rangeFromCity']
    ageRange = reqForm['ageRange']
    ageValues = ageRange.split("-");
    
    searchQ += condition;
    if country or state or city:
        searchQ += " AND SEARCH[Location]("
        searchQ += "AREA[LocationCountry]" + country if country else ""
        searchQ += " AND " if (country and (state or city)) else ""
        searchQ += "AREA[LocationState]" + state if state else ""
        searchQ += " AND " if (state and city) else ""
        searchQ += "AREA[LocationCity]" + city if (state and city) else ""
        searchQ += ")"

    # age search
    searchQ += " AND (AREA[MinimumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years]";
    searchQ += " AND AREA[MaximumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years])";

    return searchQ

    
def createURL(searchQ, result_rnk):
    query = "https://clinicaltrials.gov/api/query/study_fields?expr=" 
    query += urllib.parse.quote_plus(searchQ)
    query += "&fields=NCTId%2CBriefTitle%2CCondition%2CLocationCity%2CLocationState%2CLocationCountry%2CMinimumAge%2CMaximumAge"
    query += "&min_rnk=" + str(result_rnk) + "&max_rnk=" + str(result_rnk+9) + "&fmt=xml"
    
    return query
    

def getData(url):
    try:
        print(url)
        xml_response = requests.get(url)
        xml_response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return xml_response.content
        # Print the response content
        # print(response.text)

    except requests.exceptions.RequestException as e:
    # An error occurred
        print("Error: ", e)

def toDict(xml_content):
    root = ET.XML(xml_content)
    xmldict = XmlDictConfig(root)

    return xmldict



