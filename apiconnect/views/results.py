from django.shortcuts import render,redirect
import requests
from django.http import HttpResponse
import urllib.parse
from ..parseXML import XmlDictConfig
import xml.etree.ElementTree as ET

def card_results(request):

    if request.method == 'POST':
        url_query = ''
        result = ''
        next_token = ''
        pre_token = False
        page_tokens = ''
        result_rnk = 1
        if 'search_dict' in request.POST:
            print()
            url_query = request.POST['search_query']
            result_rnk = int(request.POST['result_rnk']) if 'result_rnk' in request.POST else 1
            next_token = request.POST['next_token'] if 'next_token' in request.POST else ''
            pre_token = True if 'pre_token' in request.POST else False
            page_tokens = request.POST['page_tokens'] if 'page_tokens' in request.POST else ''
        else:
            url_query = create_search(request.POST)

        if next_token :
            result = get_data(url_query + '&pageToken=' + next_token)
            page_tokens += (',' if page_tokens else '') + next_token
        elif pre_token and (',' in page_tokens):
            page_tokens = page_tokens.rsplit(',', 1)[0] if page_tokens else ''
            result = get_data(url_query + '&pageToken=' + page_tokens.split(',')[-1])
        else:
            page_tokens = ''
            result = get_data(url_query)

        
        print(page_tokens)
        result.update({'result_rnk': result_rnk})
        result.update({'search_query': url_query})          
        result.update({'page_tokens': page_tokens})
        if page_tokens :   result.update({'pre_page': 1})
        return render(request, 'apiconnect/card_results.html', result)


    return HttpResponse("Error!")


def single_result(request, ntcId):
    url_query = "https://clinicaltrials.gov/api/v2/studies/" + ntcId 
    fields = "NCTId,BriefTitle,OfficialTitle,Condition,BriefSummary,DetailedDescription,LocationCountry,LocationState,LocationCity"
    url_query += "?fields=" + urllib.parse.quote_plus(fields)
    response_json = get_data(url_query)
    return render(request, 'apiconnect/single_result.html', response_json)

def search_results(request):

    if request.method == 'POST':
        search_dict = ''
        result_rnk = 1
        try:
            search_dict = request.POST['search_dict']
            result_rnk = int(request.POST['result_rnk'])
        except:
            search_dict = create_search(request.POST)
        url_query = create_URL(search_dict.search_query, result_rnk)    
        response_xml = get_data(url_query)
        context = toDict(response_xml)
        context.update({'search_dict': search_dict})
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


def create_search(reqForm):
    
    searchQ = "" # Reset searchQ

    search_dict = {
        'condition': reqForm['conditionSearch'],
        'country': reqForm['countryFilter'],
        'state': reqForm['stateFilter'],
        'city': reqForm['cityFilter'],
        'range': reqForm['rangeFromCity'],
        'ageRange': reqForm['ageRange'],       
    }
    
    ageValues = search_dict['ageRange'].split("-")
    searchQ += "&query.cond=" + urllib.parse.quote_plus(search_dict['condition'])

    locationQ = ''
    if search_dict['country'] or search_dict['state'] or search_dict['city']:
        locationQ += "AREA[LocationCountry]" + search_dict['country'] if search_dict['country'] else ""
        locationQ += " AND " if (search_dict['country'] and (search_dict['state'] or search_dict['city'])) else ""
        locationQ += "AREA[LocationState]" + search_dict['state'] if search_dict['state'] else ""
        locationQ += " AND " if (search_dict['state'] and search_dict['city']) else ""
        locationQ += "AREA[LocationCity]" + search_dict['city'] if (search_dict['state'] and search_dict['city']) else ""
        searchQ += "&query.locn=" + urllib.parse.quote_plus(locationQ)

    # age search
    ageQ = ''
    ageQ += "AREA[MinimumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years]"
    ageQ += " AND AREA[MaximumAge] RANGE[" + ageValues[0] + " years, " + ageValues[1] + " years]"
    searchQ += '&filter.advanced=' + urllib.parse.quote_plus(ageQ)

    query = 'https://clinicaltrials.gov/api/v2/studies?format=json'
    query += searchQ
    query += '&fields=NCTId%2CBriefTitle%2CCondition&countTotal=true'
    
    search_dict.update({'search_query': query})

    return search_dict

    
def create_URL(searchQ, result_rnk):
    query = "https://clinicaltrials.gov/api/v2/studies?format=json&query.cond=" 
    query += urllib.parse.quote_plus(searchQ)
    query += "&fields=NCTId%2CBriefTitle%2CCondition%2CLocationCity%2CLocationState%2CLocationCountry"
    query += "&min_rnk=" + str(result_rnk) + "&max_rnk=" + str(result_rnk+9) + "&fmt=json"
    
    return query
    

def get_data(url):
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