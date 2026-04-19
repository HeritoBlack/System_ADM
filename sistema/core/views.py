from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa, Funcionario
from .forms import EmpresaForm, FuncionarioForm

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
    funcionarios_recentes = Funcionario.objects.order_by('-id')[:5]

    return render(request, 'dashboard.html', {
        'total_empresas': total_empresas,
        'total_funcionarios': total_funcionarios,
        'funcionarios_recentes': funcionarios_recentes
    })