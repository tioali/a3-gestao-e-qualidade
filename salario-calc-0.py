def calc_salario(nome, tipo, horas, vendas=0, projetos=0, ferias=False):
    if tipo == 'estagiario':
        salario = horas * 10
        if ferias:
            salario += 200
    elif tipo == 'efetivo':
        salario = horas * 20
        if horas > 180:
            salario += (horas - 180) * 25
        if ferias:
            salario += 1000
    elif tipo == 'vendedor':
        salario = horas * 15
        bonus_venda = vendas * 0.05
        salario += bonus_venda
        if vendas > 10000:
            salario += 500
        if ferias:
            salario += 800
    elif tipo == 'freelancer':
        salario = projetos * 300
        if horas > 100:
            salario += 100
    else:
        salario = 0

    print("Funcionário:", nome)
    print("Tipo:", tipo)
    print("Horas trabalhadas:", horas)
    print("Vendas:", vendas)
    print("Projetos:", projetos)
    print("Férias:", "Sim" if ferias else "Não")
    print("Salário final:", salario)
    print("--------------")