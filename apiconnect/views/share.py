from ..models import Share_Search, Share_Study
import uuid

def share_search(request):
    search_unique_id = str(uuid.uuid4())[:8]

def share_study(request):
    study_unique_id = str(uuid.uuid4())[:8]