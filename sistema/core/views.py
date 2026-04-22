from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa, Funcionario
from .forms import EmpresaForm, FuncionarioForm
from django.contrib.auth import login
from .forms import RegistroForm
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta

#CADASTRO/LOGIN
def registrar_usuario(request):
    form = RegistroForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)  # já loga automaticamente
        return redirect('dashboard')

    return render(request, 'auth/registro.html', {'form': form})

# EMPRESAS
@login_required
def lista_empresas(request):
    busca = request.GET.get('q')
    empresas = Empresa.objects.all()

    if busca:
        empresas = empresas.filter(nome__icontains=busca)

    return render(request, 'empresas/lista.html', {'empresas': empresas})


@login_required
def criar_empresa(request):
    form = EmpresaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Empresa criada com sucesso!")
        return redirect('lista_empresas')

    return render(request, 'empresas/form.html', {'form': form})


@login_required
def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    form = EmpresaForm(request.POST or None, instance=empresa)

    if form.is_valid():
        form.save()
        return redirect('lista_empresas')

    return render(request, 'empresas/form.html', {'form': form})


@login_required
def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)

    if request.method == 'POST':
        empresa.delete()
        return redirect('lista_empresas')

    return render(request, 'empresas/confirmar_exclusao.html', {'empresa': empresa})


# FUNCIONÁRIOS
@login_required
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionarios/lista.html', {'funcionarios': funcionarios})


@login_required
def criar_funcionario(request):
    form = FuncionarioForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_funcionarios')

    return render(request, 'funcionarios/form.html', {'form': form})


@login_required
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    form = FuncionarioForm(request.POST or None, instance=funcionario)

    if form.is_valid():
        form.save()
        return redirect('lista_funcionarios')

    return render(request, 'funcionarios/form.html', {'form': form})


@login_required
def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        return redirect('lista_funcionarios')

    return render(request, 'funcionarios/confirmar_exclusao.html', {'funcionario': funcionario})


# DASHBOARD
@login_required
def dashboard(request):
    total_empresas = Empresa.objects.count()
    total_funcionarios = Funcionario.objects.count()

    # Funcionários por empresa
    dados = (
        Funcionario.objects
        .values('empresa__nome')
        .annotate(total=Count('id'))
    )

    nomes_empresas = [d['empresa__nome'] for d in dados]
    qtd_funcionarios = [d['total'] for d in dados]

    # Funcionários últimos 7 dias (simulação se não tiver campo data)
    dias = []
    valores = []

    for i in range(7):
        dia = now().date() - timedelta(days=i)
        dias.append(str(dia))
        valores.append(Funcionario.objects.count())  # simples (pode melhorar depois)

    context = {
        'total_empresas': total_empresas,
        'total_funcionarios': total_funcionarios,
        'nomes_empresas': nomes_empresas,
        'qtd_funcionarios': qtd_funcionarios,
        'dias': dias[::-1],
        'valores': valores[::-1],
    }

    return render(request, 'dashboard.html', context)