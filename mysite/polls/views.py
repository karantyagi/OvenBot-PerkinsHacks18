from django.template.response import TemplateResponse



def index(request):
    if request.method == "GET":
            return TemplateResponse(request, 'index.html', {})
    else:
        data= my_response(request.POST.get('text_val'))
        return TemplateResponse(request, 'index.html',data)

def my_response(seq):
    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(seq)
    resp = {'key':'success'}
    return resp
