from ..models import Share_Search, Share_Study
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import uuid
from django.http import HttpResponse
from django.core.mail import send_mail
import json
from django.contrib.sites.shortcuts import get_current_site
from .results import get_data, single_result
import requests
import urllib.parse

from ..models import Share_Search

@login_required
def share_search(request):
    if request.method == 'POST':
        search_uid = str(uuid.uuid4())[:16]
        query = request.POST.get('query', '')
        if query:
            search = Share_Search(owner=request.user, query=query, uid=search_uid)
            search.save()
            response_data = {'success': True, 'message': 'Search shared for test successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}

        email_to = request.POST.get('email', '')
        share_link = get_current_site(request).domain + "/shared_search/search-id=" + search_uid
        print("email_to")
        email_title = "User " + str(request.user) + " has shared a search with you on findmyclinicaltrial.org!"
        email_message = "\nYou're receiving this email because user "
        email_message +=  str(request.user) 
        email_message += " has shared their search with you on findmyclinicaltrial.org!"
        email_message += "\nClick the link below to view this search on our site!\n"
        email_message += share_link
        email_message += "\nThanks for using our Find My Clinical Trial!"
        print(email_message)       
        send_share_email(email_title, email_to, email_message)
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')

def shared_search(request, search_uid):
    if request.method == 'GET':
        url_query = ''
        next_token = ''
        pre_token = False
        page_tokens = ''
        result_rnk = 1
        query_result = []
        idx = 1
        
        if search_uid:
            search_query = Share_Search.objects.filter(owner=request.user, uid=search_uid).order_by('-save_date')
            for result in search_query:
                result_dict = {
                    'idx': idx,
                    'search_query': result.query,
                    'save_date': result.save_date
                }
                idx += 1
                url_query = result.query
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

@login_required
def share_study(request):
    if request.method == 'POST':
        study_uid = str(uuid.uuid4())[:16]
        study_nctID = request.POST.get('nctId', '')
        if study_nctID:
            study = Share_Study(owner=request.user, nctId=study_nctID, uid=study_uid)
            study.save()
            response_data = {'success': True, 'message': 'Study shared for test successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}

        email_to = request.POST.get('email', '')
        share_link = get_current_site(request).domain + "/shared_study/study-id=" + study_uid
        email_title = "User " + str(request.user) + " has shared a study with you on findmyclinicaltrial.org!"
        email_message = "\nYou're receiving this email because user "
        email_message +=  str(request.user) 
        email_message += " has shared a study with you on findmyclinicaltrial.org!"
        email_message += "\nClick the link below to view this study on our site!\n"
        email_message += share_link
        email_message += "\nThanks for using our Find My Clinical Trial!"
        print(email_message)       
        send_share_email(email_title, email_to, email_message)
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')


def shared_study(request, study_uid):
    if study_uid:
        study_query = Share_Study.objects.filter(owner=request.user, uid=study_uid).order_by('-save_date')
        idx = 1
        study_ntcId = ''
        for result in study_query:
            result_dict = {
                'idx': idx,
                'search_query': result.nctId,
                'save_date': result.save_date
            }
            idx += 1
            study_ntcId = result.nctId
        #single_result(request, study_ntcId)
        url_query = "https://clinicaltrials.gov/api/v2/studies/" + study_ntcId 
        fields = "NCTId,BriefTitle,OfficialTitle,Condition,BriefSummary,DetailedDescription,LocationCountry,LocationState,LocationCity"
        url_query += "?fields=" + urllib.parse.quote_plus(fields)
        response_json = get_data(url_query)
        return render(request, 'apiconnect/single_result.html', response_json)

    return HttpResponse("Error!")


def send_share_email(email_title, email_to, email_message):
    send_mail(
    email_title,
    email_message,
    "info@findmyclinicaltrial.org",
    [email_to],
    fail_silently=False
    )

    return