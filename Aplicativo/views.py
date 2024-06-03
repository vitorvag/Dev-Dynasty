from django.shortcuts import render, redirect
from PIL import Image
import os
from Aplicativo.models import User,Post
from django.contrib import messages
import datetime
from django.http import HttpResponse


# User.objects.all().delete()
# Post.objects.all().delete()

#função que irá excluir as imagens que não estão sendo utilizadas
def excluir_imagem():
    #variável que guarda as imagens que estão sendo utilizadas
    imagens_usuarios = []
    posts = User.objects.all().values()
    #variável que guarda todas imagens da pasta media
    s = os.listdir(f'{os.getcwd()}/media')
    #adiciona as imagens que estão sendo usadas á variável imagens_usuarios
    for i in posts:
        if i['imagem'] not in imagens_usuarios:
            imagens_usuarios.append(i['imagem'])
    #deleta as imagens que não estão sendo usadas: se a imagem não estiver em imagens_usuarios então a delete
    for i in s:
        if i not in imagens_usuarios and i != 'anonimo.png' and i != 'imgs':
            os.remove(f'{os.getcwd()}/media/{i}')
    return

#retorna a hora:minutos dia/mês/ano
def definir_data():
    data_atual = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
    return data_atual
    
#variável que obterá o nome do usúario assim que ele entrar
user2 = []

selecionado = []
selecionado.append('')
def home(request):
    #esse if checa se o usuário já entrou ou não, se não ele retornará a página de login
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    #Salva a imagem com pillow
    '''if request.method == "POST":
        file = request.FILES.get('my_file')
        # img = Image.open(file)
        # path =  os.path.join(settings.BASE_DIR, f'media/{file.name}')
        # print(file.name)
        # img = img.save(path)'''

    dados = {}
    dados['recentes'] = Post.objects.order_by('-id').values()[:3]
    return render(request, 'index.html', dados)


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        file = request.FILES.get('file')
        
        #retornará para a mesma página caso os campos nome e senha estiverem em branco
        if nome == '' or senha == '':
            messages.info(request, "Senha ou nome não podem passar em braco")
            dados = {}
            dados['n'] = nome
            dados['s'] = senha
            return render(request,'cadastro.html', dados)
        
        #retornará para a mesma página caso o usuário já for existente
        for i in User.objects.all().values():
            if i['user'].lower() == nome.lower():
                messages.info(request, "Usuário já existente")
                dados = {}
                #essas variáveis são para retornar os valores que usuário tinha digitado
                dados['n'] = nome
                dados['s'] = senha
                return render(request,'cadastro.html',dados)
            
        #esse try é para se o usuário colocar uma imagem senão a imagem ficrá em branco
        try:
            i = Image.open(file)
            s = os.listdir(f'{os.getcwd()}/media')
            #esse for percorrerá os arquivos existentes, irá transformalos em bytes e fará a checagem com o arquivo escolido pelo usuário
            for arquivos in s:
                #imgs é uma pasta
                if arquivos != 'imgs':
                    abrir = Image.open(f'{os.getcwd()}/media/{arquivos}')
              
                    #se o arquivo escolido já existir o campo 'imagem' receberá um arquivo existente e não um novo
                    if abrir.tobytes("xbm", "rgb") == i.tobytes("xbm", "rgb") and arquivos != 'anonimo.png' and arquivos != 'imgs':
                        u = User(user=nome,senha=senha,imagem=arquivos)
                        u.save()
                        user2.clear()
                        #dizendo á variável user2 que o usuário entrou
                        user2.append(nome)
                        
                        return redirect(home)
            #se o arquivo for inexistente, então o campo 'imagem' receberá um novo arquivo
            
            t = User(user=nome,senha=senha,imagem=file)
            print(6)
            t.save()
            print(7)
            user2.clear()
            #dizendo á variável user2 que o usuário entrou
            user2.append(nome)
            return redirect(home)
        #caso o usuário não escolher uma imagem
        except:
            t = User(user=nome,senha=senha)
            t.save()
            user2.clear()
            user2.append(nome)
            return redirect(home)
        
    else:
        return render(request,'cadastro.html')
    
def login(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        #retornará para a página caso a nome do usuário não existir
        try:
            usuario = User.objects.get(user=nome.lower())
        except:
            messages.info(request, "usuário não encontrado")
            return render(request,'login.html')
        
        #se a senha do usuário estiver correta então vá para o index
        if usuario.senha == senha:
            user2.clear()
            user2.append(usuario.user)
            return redirect(home)
        
        #caso a senha não estiver correta
        messages.info(request, "Algo de errado não está certo")
        return render(request,'login.html')
    else:
         return render(request,'login.html')

def postar(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    if request.method == 'POST':
        post = request.POST.get('post')
        if post == '':
            messages.info(request, "A postagem não pode ter texto em branco")
            return render(request,'postar.html')
        else:
            if len(post) > 140 :
               messages.info(request, "A postagem não pode ter mais do que 140 caracteres")
               return render(request,'postar.html')
            else:
                img = []
                #definirá qual imagem ficará no post, se o campo User.imagem == '' então a imagem no post receberá 'anónimo.png'
                for i in User.objects.filter(user=user2[0]).values():
                    if i['imagem'] != '':
                        img.append(i['imagem'])
                    
                    else:
                        img.append('anonimo.png')
                
                #realiza o post
                p = Post(user=user2[0],post=post,data=definir_data(),imagem=img[0])
                p.save()
                return redirect(posts)

    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'postar.html',dados)

def deletar(request,id):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    #pega o id do usuário a ser deletado
    usuario = Post.objects.filter(id=id).values()
    for i in usuario:
        #se o usuario que realizou o post != do usuario que qer excluílo então retornará uma mensagem e não excluirá o post
        if i['user'].lower() != user2[0].lower():
            messages.info(request, "Você não tem autorização para apagar este post")
            return redirect(posts)
        
    if request.method == 'POST':
        s = request.POST.get('sim')
        n = request.POST.get('nao')
        #se o input checbox 'sim' == 'on' então o post será deletado
        if s == 'on' and n == None:
            t = Post.objects.get(id=id)
            t.delete()
            return redirect(posts)
        #se o input checbox 'nao' == 'on' então o post não será deletado
        elif n == 'on' and s == None:
            return redirect(posts)
        #caso nenhum dos dois inputs terem sido marcados
        else:
            messages.info(request, "Marque uma das opções")
            return render(request,'deletar.html')
    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'deletar.html',dados)
    
def atualizar(request,id):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    x = Post.objects.filter(id=id).values()
    for i in x:
        #se o usuario que realizou o post != do usuario que quer atualizaló então retornará uma mensagem e não atualizará o post
        if i['user'].lower() != user2[0].lower():
            messages.info(request, "Você não tem autorização para editar este post")
            return redirect(posts)
        
    if request.method == 'POST':
        #variável que comtém a atualização
        atualizacao = request.POST.get('atualizacao')
        if atualizacao == '':
            messages.info(request, "A postagem não pode ter texto em branco")
            return render(request,'atualizar.html')
        else:
            if len(atualizacao) > 140 :
               messages.info(request, "A postagem não pode ter mais do que 140 caracteres")
               return render(request,'atualizar.html')
            else:
                post_a_ser_atualizado = Post.objects.get(id=id)
                post_a_ser_atualizado.post = atualizacao
                post_a_ser_atualizado.data = definir_data()
                post_a_ser_atualizado.save()
                return redirect(posts)
    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'atualizar.html',dados)

def mudar_imagem(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    def mudar_imagem_dos_posts(x):
        #pegará todos os posts do usuário 
        posts = Post.objects.filter(user=user2[0])
        #caso a imagem != '' irá salvar a nova imagem
        if x != '':
            for post in posts:
                post.imagem = x
                post.save()
        #caso a imagem == '' irá salvar a imagem 'anonimo.png' como imagem do post
        elif x == '':
            for post in posts:
                post.imagem = 'anonimo.png'
                post.save()
        return
    if request.method == 'POST':
        f = request.FILES.get('file')
        deixar_anonima = request.POST.get('img')
        user = User.objects.get(user=user2[0])
        #se o input checbox for clicado então a imagem ficará anônima
        if deixar_anonima == 'on':
            user.imagem = ''
            user.save()
            mudar_imagem_dos_posts(user.imagem)
            excluir_imagem()
            return redirect(posts)
        else:
            #se nenhuma imagem for escolida então retornará para o index
            if f == '':
                return redirect(posts)
            else:
                img = Image.open(f)
                try:
                 imagem_usuario = Image.open(user.imagem, mode='r')
                except:
                    imagem_usuario = Image.open(f'{os.getcwd()}/media/anonimo.png')
                #Retornar imagem como um objeto de bytes
                if img.tobytes("xbm", "rgb") == imagem_usuario.tobytes("xbm", "rgb"):
                    img.close()
                    imagem_usuario.close()
                    excluir_imagem()
                    return redirect(posts)
                else:
                    pasta_media = os.listdir(f'{os.getcwd()}/media')
                    for arquivos in pasta_media:
                            if os.path.isdir(f'{os.getcwd()}/media/{arquivos}') == False:
                                arquivos_media_abertos = Image.open(f'{os.getcwd()}/media/{arquivos}')
                                if arquivos_media_abertos.tobytes("xbm", "rgb") == img.tobytes("xbm", "rgb") and arquivos != 'anonimo.png':
                                    user.imagem = arquivos
                                    user.save()
                                    arquivos_media_abertos.close()
                                    img.close()
                                    imagem_usuario.close()
                                    mudar_imagem_dos_posts(user.imagem)
                                    excluir_imagem()
                                    return redirect(posts)
                                arquivos_media_abertos.close()
                    #s = os.remove(f'{os.getcwd()}/media/{u.imagem}')
                    user.imagem = f
                    user.save()
                    mudar_imagem_dos_posts(user.imagem)
                    img.close()
                    imagem_usuario.close()
                    excluir_imagem()
                    return redirect(posts)
                #u.save()
                

    else:
        return render(request, 'mudar_imagem.html')

def sair(request):
    user2.clear()
    return redirect(login)

def about(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    return render(request,'about.html')

def posts(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    dados = {}
    def meus(dados):
        dados['tabela'] = Post.objects.filter(user=user2[0]).order_by('-id').values()
        selecionado.clear()
        selecionado.append('meus')
        dados['meus'] = 'selected' 
    
    def recentes(dados):
        dados['tabela'] = Post.objects.order_by('-id').values()[:3]
        selecionado.clear()
        selecionado.append('recentes')
        dados['recentes'] = 'selected' 
    
    def todos(dados):
        dados['tabela'] = Post.objects.all().order_by('-id').values()
        selecionado.clear()
        selecionado.append('todos')
        dados['todos'] = 'selected' 
        
    if request.method == 'POST':
        select = request.POST.get('select')
        if select == 'meus':
            meus(dados)
        elif select == 'todos' or select == '':
            todos(dados)
        elif select == 'recentes':
            recentes(dados)
        return render(request,'blogs.html',dados)
    else:
        if selecionado[0] == 'meus':
            meus(dados)
        elif selecionado[0] == 'todos' or selecionado[0] == '':
            todos(dados)
        elif selecionado[0] == 'recentes':
            recentes(dados)
        return render(request,'blogs.html',dados)