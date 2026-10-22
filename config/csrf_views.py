from django.shortcuts import render

def crsf_failure(request, reason=""):
    #this is called when session/token expired
    return render(request,
                  '403_csrf.html', {
            'reason': reason,
            'messsage': 'your session has expired. please refresh the page or login again to continue.'
                  }, status=403)
