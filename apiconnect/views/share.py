from ..models import Share_Search, Share_Study
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import uuid
from django.http import HttpResponse
from django.core.mail import send_mail
import json

from ..models import Search

@login_required
def share_search(request):
    if request.method == 'POST':
        search_uid = str(uuid.uuid4())[:8]
        query = request.POST.get('query', '')
        if query:
            search = Search(owner=request.user, query=query)
            search.save()
            response_data = {'success': True, 'message': 'Search shared for test successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}

        email_to = request.POST.get('email', '')
        print("email_to")
        email_title = "User [username] has shared a search with you on findmyclinicaltrial.org!"
        email_message = "You're receiving this email because user [username] has shared their search with you on findmyclinicaltrial.org.\nClick the link below to view this search on our site!\n" + query +".\nThanks for using our Find My Clinical Trial!"
        #send_email(email_title, email_to, email_message)
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    
@login_required
def share_search2(request):
    print("Hello World!")
    search_uid = str(uuid.uuid4())[:8]
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            search = Share_Search(owner=request.user, query=query, uid=search_uid)
            search.save()
            response_data = {'success': True, 'message': 'Search shared successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}
        
        email_to = request.POST.get('email', '')
        email_title = "User " + request.user + " has shared a search with you on findmyclinicaltrial.org!"
        email_message = "You're receiving this email because user "+ request.user + " has shared their search with you on findmyclinicaltrial.org.\nClick the link below to view this search on our site!\n" + query +".\nThanks for using our Find My Clinical Trial!"
        send_email(email_title, email_to, email_message)
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def send_email(email_title, email_to, email_message):
    send_mail(
    email_title,
    email_message,
    "info@findmyclinicaltrial.org",
    [email_to],
    fail_silently=False,
)

@login_required
def share_study(request):
    study_uid = str(uuid.uuid4())[:8]
    return render(request, 'apiconnect/share_study.html')