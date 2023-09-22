from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ..models import Save_Search, Save_Study
from django.http import HttpResponse
import json
import ast


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
        search_dict = request.POST.get('search_dict', '')
        if query:
            search = Save_Search(owner=request.user, search_dict=search_dict, query=query)
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
        # cond_idx = item.query.find('cond=')
        # ampersand_idx = item.query.find('&filter')
        # search_q = item.query[cond_idx + 5: ampersand_idx] if ampersand_idx != -1 else ''
        search_dict_post = item.search_dict
        search_dict = ast.literal_eval(search_dict_post)
        item_dict = {
            'idx' : idx,
            'search_dict': search_dict,
            'query': item.query,
            'saved': item.saved,
        }
        searches.append(item_dict)
        print(item_dict['query'])
        idx += 1

    context = {'searches': searches}
    return render(request, 'apiconnect/saved_searches.html', context)