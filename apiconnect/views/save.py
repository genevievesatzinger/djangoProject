from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ..models import Save_Search, Save_Study
from django.http import HttpResponse
import json


@login_required
def save_study(request):
    if request.method == 'POST':
        nct = request.POST.get('nctId', '')
        if nct:
            study = Save_Study(owner=request.user, nctId=nct)
            study.save()
            response = {'success': True, 'message': 'Study saved successfully!'}
        else:
            response = {'success': False, 'message': 'Query cannot be empty.'}

        return HttpResponse(json.dumps(response), content_type = 'application/json')

@login_required
def saved(request):  
    return render(request, 'apiconnect/saved.html') 

@login_required
def saved_studies(request):
    studies_query = Save_Study.objects.filter(owner=request.user).order_by('-save_date')
    studies = []
    idx = 1
    # Make a lists of results; for each result, make a dictionary
    for result in studies_query:
        result_dict = {
            'idx': idx,
            'nctId': result.nctId,
            'save_date': result.save_date
        }
        studies.append(result_dict)
        idx += 1

    print(studies)
    context = {'singleResults': studies}
    return render(request, 'apiconnect/saved_studies.html', context)
        
@login_required
def save_search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            search = Save_Search(owner=request.user, query=query)
            search.save()
            response_data = {'success': True, 'message': 'Search saved successfully!'}
        else:
            response_data = {'success': False, 'message': 'Query cannot be empty.'}
        
        return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def saved_searches(request):
    searches_query = Save_Search.objects.filter(owner=request.user).order_by('-saved')
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