import hashlib
from django.shortcuts import render, redirect
from .models import Usuario

def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def login(request):
    if request.session.get('usuario'):
        return redirect('/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    usuario = Usuario.objects.filter(email = email) # Verificar se existem usuários com email cadastrado

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=1')
    
    if len(nome.strip()) == 0:
        return redirect('/auth/cadastro/?status=2')
    
    if len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=3')
    
    if len(senha) < 8 or len(senha) > 12:
        return redirect('/auth/cadastro/?status=4')
    
    try:
        senha = hashlib.sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome,
                          email = email,
                          senha = senha) # O campo nome definido no models tem que ser igual ao do formulário
        usuario.save()
        return redirect('/auth/login/?status=0')
    except:
        return redirect('/auth/cadastro/?status=5')
    
def valida_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha = hashlib.sha256(senha.encode()).hexdigest() # Como no cadastrado utilizamos hash para criptografar senha, então aqui antes de filtrar os usuários, deve chamar a hash
        usuarios = Usuario.objects.filter(email = email).filter(senha = senha) # Verificar se existem usuários com email e senha cadastrado

        if not usuarios.exists():
            return redirect('/auth/login/?status=1')
        
        request.session['usuario'] = usuarios[0].id # session global
        return redirect('/home/')
    
    return redirect('/auth/login/')
    
def sair(request):
    request.session.flush()
    return redirect('/auth/login/')