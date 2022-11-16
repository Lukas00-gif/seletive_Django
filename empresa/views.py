from django.http import HttpResponse
from django.shortcuts import render
from .models import Tecnologias, Empresa, Vagas
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def nova_empresa(request):
    if request.method == 'GET':
        techs =  Tecnologias.objects.all()
        return render(request, 'nova_empresa.html', { 'techs': techs})
    elif request.method == 'POST':
        #primeiro vc captura as variaveis e dps tratamos
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        caracteristicas = request.POST.get('caracteristicas')
        tecnologias = request.POST.getlist('tecnologias')
        logo = request.FILES.get('logo')

        #validaçoes
        #strip, tirar os espaços em branco
        if (len(nome.strip()) == 0 or len(email.strip()) == 0 or 
        len(cidade.strip()) == 0 or len(endereco.strip()) == 0 or 
        len(nicho.strip()) == 0 or len(caracteristicas.strip()) == 0 or (not logo)): 
            messages.add_message(request, constants.ERROR, 'Todos os campos sao obrigatorios')
            return redirect('/home/nova_empresa')

        #10MB
        if logo.size > 100_000_000:
            messages.add_message(request, constants.WARNING, 'Sua logo nao pode ter mais de 10MB')
            return redirect('/home/nova_empresa')

        #pega a primeira letra, mais no caso se nao tiver por conta do not
        if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
            messages.add_message(request, constants.WARNING, 'Nicho de mercado invalido')
            return redirect('/home/nova_empresa')
        
        #salvar dados, primeiro 
        empresa = Empresa(logo=logo,
                        nome=nome,
                        email=email,
                        cidade=cidade,
                        endereco=endereco,
                        nicho_mercado=nicho,
                        caracteristica_empresa=caracteristicas)
        empresa.save()
        empresa.tecnologias.add(*tecnologias)
        empresa.save()
        messages.add_message(request, constants.SUCCESS, 'Empresa Cadastrada com Sucesso')
        
        return redirect('/home/nova_empresa')


def empresas(request):
    #variaveis do filtro
    tecnologias_filtrar = request.GET.get('tecnologias')
    nome_filtrar = request.GET.get('nome')
    empresas = Empresa.objects.all()

    #filtros
    if tecnologias_filtrar:
        empresas = empresas.filter(tecnologias=tecnologias_filtrar)
    
    if nome_filtrar:
        #esse icontains e para nome dentro
        empresas = empresas.filter(nome__icontains=nome_filtrar)


    #isso e o terceiro parametro onde envia para o html os dados de empresa quee eu p1eguei
    tecnologias = Tecnologias.objects.all()
    return render(request, 'empresas.html', {'empresas': empresas, 'tecnologias': tecnologias})

def excluir_empresa(request, id):
    #joga na url e captura(get) o id como parametro, esse modo pegando uma unica emmpresa
    empresa = Empresa.objects.get(id=id)    
    empresa.delete()
    messages.add_message(request, constants.INFO, 'Empresa deletada com Sucesso')

    return redirect('/home/empresas')

def empresa(request, id):
    #peque um objeto ou de erro 404 literalmente se n existir ele da um 404
    tecnologias = Tecnologias.objects.all()
    empresa_unica = get_object_or_404(Empresa, id=id)
    empresas = Empresa.objects.all()
    # irei buscas as vagas onde a empresa_id e = a id
    vagas = Vagas.objects.filter(empresa_id=id)
    return render(request, 'empresa_unica.html', {'empresa': empresa_unica, 
                                                'tecnologias': tecnologias,
                                                'empresas': empresas,
                                                'vagas': vagas})


