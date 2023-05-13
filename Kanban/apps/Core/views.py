from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FeedbackReport

# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def sobre(request):
    return render(request, 'core/sobre.html')

def suporte(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST['title']
            subject = request.POST['subject']
            content = request.POST['content']
            report = FeedbackReport(user=request.user, title=title, subject=subject, content=content)
            report.save()
            messages.success(request, 'Muito obrigado pelo seu feedback! Estamos sempre à disposição caso precise de algo.')
            return redirect('index')
        else:
            messages.error(request, 'Você precisa estar logado para enviar um feedback!')
            return redirect('suporte')
    else:
        return render(request, 'core/help.html')