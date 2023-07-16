from django.shortcuts import render
import requests
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import urllib.parse
from .parseXML import XmlDictConfig


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



