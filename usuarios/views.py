from django.contrib.auth.models import User
from django.contrib.messages import constants, add_message
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Medicos


def sisregoff(request):
    return render(request, 'sisregoff.html') 

def apacoff(request):
    return render(request, 'apacoff.html') 


@login_required
def home(request):
    user = request.user
    if user.first_name.lower() == "paciente":
        return redirect('paciente')
    else:
        return render(request, 'home.html')


def paciente(request):
    return render(request, 'paciente.html') 


def addpac(request):
    return render(request, 'addpac.html') 


def cadastro(request):
    if request.method == 'POST':
        # Obter os dados do formulário
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        matricula = request.POST.get('matricula')
        crm = request.POST.get('crm')
        cns = request.POST.get('cns')
        celular = request.POST.get('celular')
        trak = request.POST.get('trak')
        sisreg = request.POST.get('sisreg')
        sisrep = request.POST.get('sisrep')
        especialidade_id = request.POST.get('especialidade')

        # Criar um novo usuário
        user = User.objects.create_user(username=username, password=password, first_name=first_name, email=email)

        # Criar um novo objeto Dados associado ao usuário criado
        dados = Medicos.objects.create(
            user=user,
            matricula=matricula,
            crm=crm,
            cns=cns,
            celular=celular,
            trak=trak,
            sisreg=sisreg,
            sisrep=sisrep,
            especialidade_id=especialidade_id
        )

        # Autenticar e logar o usuário
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Adicionar mensagem de sucesso
            messages.success(request, 'Cadastro realizado com sucesso! Algumas funções podem não estar disponíveis até a avaliação e aprovação do administrador.')

        # Redirecionar para a página inicial após o cadastro
        return redirect('home')

    # Se o método da requisição não for POST, renderize o formulário de cadastro
    return render(request, 'cadastro.html')
