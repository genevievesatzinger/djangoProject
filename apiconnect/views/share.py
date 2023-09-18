from ..models import Share_Search, Share_Study
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import uuid
from django.http import HttpResponse
from django.core.mail import send_mail
import json
from django.contrib.sites.shortcuts import get_current_site
from .results import get_data
import requests

from ..models import Search

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
        share_link = get_current_site(request).domain + "/show_shared_search/search-id=" + search_uid
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


def send_share_email(email_title, email_to, email_message):
    from django.core.mail import get_connection
    from django.core.mail.message import EmailMessage

    connection = get_connection(use_tls=True, host='smtp.mailersend.net', port=587,username='MS_5BWAP5@findmyclinicaltrial.org', password='JYeRGCZr1WZUtHYi')
    # EmailMessage('test', 'test', 'info@findmyclinicaltrial.org', [email_to], connection=connection).send()
    send_mail(
    email_title,
    email_message,
    "info@findmyclinicaltrial.org",
    [email_to],
    fail_silently=False,
    connection=connection
    )


def show_shared_search(request, search_uid):
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
    study_uid = str(uuid.uuid4())[:8]
    return render(request, 'apiconnect/share_study.html')