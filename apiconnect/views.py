from django.shortcuts import render,redirect
import requests
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import urllib.parse
from .parseXML import XmlDictConfig
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Search

@login_required
def save_search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            search = Search(owner=request.user, query=query)
            search.save()
            response_data = {'success': True, 'message': 'Search saved successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required  
def saved_searches(request):
    searches_query = Search.objects.filter(owner=request.user).order_by('-saved')
    searches = []
    idx = 1
    for item in searches_query:
        cond_idx = item.query.find('cond=')
        ampersand_idx = item.query.find('&filter')
        search_q = item.query[cond_idx + 5: ampersand_idx] if ampersand_idx != -1 else ''
        print(search_q)
        item_dict = {
            'idx' : idx,
            'search': search_q,
            'query': item.query,
            'saved': item.saved,
        }
        searches.append(item_dict)
        idx += 1

    print(searches)
    context = {'searches': searches}
    return render(request, 'apiconnect/saved_searches.html', context)


def home(request):
    return render(request, 'apiconnect/home.html')

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist!')

    context = {'page': page}
    return render(request, 'apiconnect/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registeration')

    return render(request, 'apiconnect/login_register.html', {'form': form})


def cardResults(request):

    if request.method == 'POST':
        url_query = ''
        result = ''
        next_token = ''
        pre_token = False
        page_tokens = ''
        result_rnk = 1
        if 'search_query' in request.POST:
            url_query = request.POST['search_query']
            result_rnk = int(request.POST['result_rnk']) if 'result_rnk' in request.POST else 1
            next_token = request.POST['next_token'] if 'next_token' in request.POST else ''
            pre_token = True if 'pre_token' in request.POST else False
            page_tokens = request.POST['page_tokens'] if 'page_tokens' in request.POST else ''
        else:
            url_query = createSearch(request.POST)

        if next_token :
            result = getData(url_query + '&pageToken=' + next_token)
            page_tokens += (',' if page_tokens else '') + next_token
        elif pre_token and (',' in page_tokens):
            page_tokens = page_tokens.rsplit(',', 1)[0] if page_tokens else ''
            result = getData(url_query + '&pageToken=' + page_tokens.split(',')[-1])
        else:
            page_tokens = ''
            result = getData(url_query)

        
        print(page_tokens)
        result.update({'result_rnk': result_rnk})
        result.update({'search_query': url_query})          
        result.update({'page_tokens': page_tokens})
        if page_tokens :   result.update({'pre_page': 1})
        return render(request, 'apiconnect/cardResults.html', result)


    return HttpResponse("Error!")


def singleResult(request, ntcId):
    url_query = "https://clinicaltrials.gov/api/v2/studies/" + ntcId 
    fields = "NCTId,BriefTitle,OfficialTitle,Condition,BriefSummary,DetailedDescription,LocationCountry,LocationState,LocationCity"
    url_query += "?fields=" + urllib.parse.quote_plus(fields)
    response_json = getData(url_query)
    return render(request, 'apiconnect/singleResult.html', response_json)

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
    
    searchQ += "&query.cond=" + urllib.parse.quote_plus(condition)

    locationQ = ''
    if country or state or city:
        locationQ += "AREA[LocationCountry]" + country if country else ""
        locationQ += " AND " if (country and (state or city)) else ""
        locationQ += "AREA[LocationState]" + state if state else ""
        locationQ += " AND " if (state and city) else ""
        locationQ += "AREA[LocationCity]" + city if (state and city) else ""
        searchQ += "&query.locn=" + urllib.parse.quote_plus(locationQ)

    # age search
    ageQ = ''
    ageQ += "AREA[MinimumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years]"
    ageQ += " AND AREA[MaximumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years]"
    searchQ += '&filter.advanced=' + urllib.parse.quote_plus(ageQ)

    query = 'https://clinicaltrials.gov/api/v2/studies?format=json'
    query += searchQ
    query += '&fields=NCTId%2CBriefTitle%2CCondition&countTotal=true'
    
    return query

    
def createURL(searchQ, result_rnk):
    query = "https://clinicaltrials.gov/api/v2/studies?format=json&query.cond=" 
    query += urllib.parse.quote_plus(searchQ)
    query += "&fields=NCTId%2CBriefTitle%2CCondition%2CLocationCity%2CLocationState%2CLocationCountry"
    query += "&min_rnk=" + str(result_rnk) + "&max_rnk=" + str(result_rnk+9) + "&fmt=json"
    
    return query
    

def getData(url):
    try:
        json_response = requests.get(url)
        json_response.raise_for_status()  # Raise an exception if the request was unsuccessful
        json_context = json_response.json()
        return json_context
        # Print the response content
        # print(response.text)

    except requests.exceptions.RequestException as e:
    # An error occurred
        print("Error: ", e)

def toDict(xml_content):
    root = ET.XML(xml_content)
    xmldict = XmlDictConfig(root)

    return xmldict



