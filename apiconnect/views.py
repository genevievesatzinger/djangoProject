from django.shortcuts import render
import requests
from django.http import HttpResponse
import xml.etree.ElementTree as ET


def home(request):
    url = "https://classic.clinicaltrials.gov/api/query/study_fields?expr=heart+attack&fields=NCTId%2CBriefTitle%2CCondition&min_rnk=1&max_rnk=&fmt=xml"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        # Print the response content
        # print(response.text)

    except requests.exceptions.RequestException as e:
    # An error occurred
        print("Error: ", e)
    root = ET.fromstring(response.content)
    content = ''
    for child in root:
        content += child.tag + '  '
    return HttpResponse(content)
    #return render(request, 'apiconnect/home.html')

def results(request):
    return render(request, 'apiconnect/results.html')
