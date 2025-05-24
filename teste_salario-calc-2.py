import pytest
import json
from decimal import Decimal

from funcionarios import (
    Funcionario,
    Estagiario,
    Efetivo,
    Vendedor,
    Freelancer,
    FabricaFuncionario,
    RelatorioTexto,
    RelatorioJSON
)


# Constantes para cálculos
VALOR_HORA_ESTAGIARIO = Decimal('10.00')
BONUS_FERIAS_ESTAGIARIO = Decimal('200.00')
TARIFA_HORA_EFETIVO = Decimal('20.00')
TARIFA_EXTRA_EFETIVO = Decimal('25.00')
HORAS_LIMITE_EFETIVO = 180
BONUS_FERIAS_EFETIVO = Decimal('1000.00')
TARIFA_HORA_VENDEDOR = Decimal('15.00')
TAXA_COMISSAO_VENDEDOR = Decimal('0.05')
BONUS_VENDAS = Decimal('500.00')
LIMITE_BONUS_VENDEDOR = Decimal('10000.00')
BONUS_FERIAS_VENDEDOR = Decimal('800.00')
PAGAMENTO_POR_PROJETO = Decimal('300.00')
BONUS_HORAS_FREELANCER = Decimal('100.00')
BONUS_FERIAS_FREELANCER = Decimal('0.00')


# ---------- Tests Gerais de Validação e Formatação ----------

def test_nome_title_case_e_strip():
    """Verifica que o nome é stripado e convertido para Title Case."""
    est = Estagiario.criar("   joão da silva    ", 10)
    assert est.nome == "João Da Silva"

def test_nome_nao_string():
    """Verifica que nome que não for string lança ValueError."""
    with pytest.raises(ValueError, match="Nome deve ser uma string"):
        Estagiario.criar(123, 10)

def test_horas_float_aceito_como_inteiro():
    """Verifica que horas dadas como float equivalente a inteiro são aceitas."""
    est = Estagiario.criar("Maria", 100.0)
    assert isinstance(est.horas, int)
    assert est.horas == 100

def test_horas_float_nao_inteiro_lanca_erro():
    """Verifica que horas float não inteiro (e.g., 10.5) lança ValueError."""
    with pytest.raises(ValueError, match="Horas trabalhadas deve ser inteiro ou float equivalente a inteiro"):
        Estagiario.criar("Pedro", 10.5)

def test_horas_nao_numerico_lanca_erro():
    """Verifica que horas não numéricas lançam ValueError."""
    with pytest.raises(ValueError, match="Horas trabalhadas deve ser um número inteiro"):
        Estagiario.criar("Ana", "cem")

def test_horas_nao_numerico_em_outra_subclasse():
    """Verifica validação de horas em Efetivo quando for string."""
    with pytest.raises(ValueError, match="Horas trabalhadas deve ser um número inteiro"):
        Efetivo.criar("Ana", "100")

def test_set_ferias_truthy_falsy():
    """Verifica conversão do parâmetro 'ferias' para booleano."""
    est1 = Estagiario.criar("Teste", 10, ferias="qualquerTexto")
    assert est1.ferias is True

    est2 = Estagiario.criar("Teste", 10, ferias=0)
    assert est2.ferias is False


# ---------- Tests de Estagiario ----------

def test_estagiario_salario_sem_ferias():
    horas_trabalhadas = 160
    estagiario = Estagiario.criar("João Silva", horas_trabalhadas)
    salario_esperado = Decimal(horas_trabalhadas) * VALOR_HORA_ESTAGIARIO
    assert estagiario.salario_mensal() == salario_esperado

def test_estagiario_salario_total_com_ferias():
    horas_trabalhadas = 120
    estagiario = Estagiario.criar("Maria Souza", horas_trabalhadas, ferias=True)
    salario_esperado = (Decimal(horas_trabalhadas) * VALOR_HORA_ESTAGIARIO) + BONUS_FERIAS_ESTAGIARIO
    assert estagiario.salario_total() == salario_esperado.quantize(Decimal('0.01'))

def test_estagiario_horas_negativas():
    with pytest.raises(ValueError, match="Horas trabalhadas não podem ser negativas"):
        Estagiario.criar("João Silva", -10)

def test_estagiario_to_dict():
    est = Estagiario.criar("João Silva", 100, ferias=False)
    dados = est.to_dict()
    assert dados['nome'] == "João Silva"
    assert dados['horas'] == 100
    assert dados['ferias'] is False
    assert dados['tipo'] == "Estagiario"
    assert dados['valor_hora'] == float(VALOR_HORA_ESTAGIARIO)
    assert isinstance(dados['salario_total'], float)


# ---------- Tests de Efetivo ----------

def test_efetivo_salario_sem_horas_extras():
    horas = HORAS_LIMITE_EFETIVO
    efetivo = Efetivo.criar("Carlos Lima", horas)
    salario_esperado = Decimal(horas) * TARIFA_HORA_EFETIVO
    assert efetivo.salario_mensal() == salario_esperado

def test_efetivo_salario_com_horas_extras():
    horas_extras = 20
    total_horas = HORAS_LIMITE_EFETIVO + horas_extras
    efetivo = Efetivo.criar("Carlos Lima", total_horas)
    salario_esperado = (Decimal(HORAS_LIMITE_EFETIVO) * TARIFA_HORA_EFETIVO) + (Decimal(horas_extras) * TARIFA_EXTRA_EFETIVO)
    assert efetivo.salario_mensal() == salario_esperado

def test_efetivo_salario_total_com_ferias():
    efetivo = Efetivo.criar("Carlos Lima", 100, ferias=True)
    salario_mensal = efetivo.salario_mensal()
    assert efetivo.salario_total() == (salario_mensal + BONUS_FERIAS_EFETIVO).quantize(Decimal('0.01'))

def test_efetivo_horas_zero():
    efetivo = Efetivo.criar("Carlos Lima", 0)
    assert efetivo.salario_mensal() == Decimal('0.00')

def test_efetivo_casos_borda_altas_horas():
    horas_altas = 1000
    efetivo = Efetivo.criar("Carlos Lima", horas_altas)
    extras = horas_altas - HORAS_LIMITE_EFETIVO
    salario_esperado = (Decimal(HORAS_LIMITE_EFETIVO) * TARIFA_HORA_EFETIVO) + (Decimal(extras) * TARIFA_EXTRA_EFETIVO)
    assert efetivo.salario_mensal() == salario_esperado

def test_efetivo_to_dict():
    efetivo = Efetivo.criar("Beatriz Costa", 150, ferias=False)
    dados = efetivo.to_dict()
    assert dados['nome'] == "Beatriz Costa"
    assert dados['horas'] == 150
    assert dados['tipo'] == "Efetivo"
    assert dados['tarifa_hora'] == float(TARIFA_HORA_EFETIVO)
    assert dados['tarifa_extra'] == float(TARIFA_EXTRA_EFETIVO)
    assert dados['horas_limite'] == HORAS_LIMITE_EFETIVO
    assert isinstance(dados['salario_total'], float)


# ---------- Tests de Vendedor ----------

def test_vendedor_salario_sem_bonus_vendas():
    horas_trabalhadas = 40
    vendas = 5000.0  # abaixo do limite de bônus
    vendedor = Vendedor.criar("Ana Silva", horas_trabalhadas, vendas=vendas)
    salario_esperado = (Decimal(horas_trabalhadas) * TARIFA_HORA_VENDEDOR) + (Decimal(str(vendas)) * TAXA_COMISSAO_VENDEDOR)
    assert vendedor.salario_mensal() == salario_esperado

def test_vendedor_salario_com_bonus_vendas():
    horas_trabalhadas = 40
    vendas = 20000.0  # acima do limite de bônus
    vendedor = Vendedor.criar("Ana Silva", horas_trabalhadas, vendas=vendas)
    salario_esperado = (
        (Decimal(horas_trabalhadas) * TARIFA_HORA_VENDEDOR)
        + (Decimal(str(vendas)) * TAXA_COMISSAO_VENDEDOR)
        + BONUS_VENDAS
    )
    assert vendedor.salario_mensal() == salario_esperado

def test_vendedor_salario_total_com_ferias():
    vendedor = Vendedor.criar("Roberto Carlos", 50, vendas=5000.0, ferias=True)
    salario_mensal = vendedor.salario_mensal()
    assert vendedor.salario_total() == (salario_mensal + BONUS_FERIAS_VENDEDOR).quantize(Decimal('0.01'))

def test_vendedor_vendas_negativas():
    with pytest.raises(ValueError, match="Valor de vendas não pode ser negativo"):
        Vendedor.criar("Ana Silva", 40, vendas=-1000.0)

def test_vendedor_vendas_invalida_string():
    with pytest.raises(ValueError, match="Valor de vendas deve ser numérico ou string numérica"):
        Vendedor.criar("Ana Silva", 40, vendas="abc")

def test_vendedor_to_dict():
    vendedor = Vendedor.criar("Patrícia Lima", 80, vendas=10000.0)
    dados = vendedor.to_dict()
    assert dados['nome'] == "Patrícia Lima"
    assert dados['tipo'] == "Vendedor"
    assert dados['vendas'] == 10000.0
    assert dados['taxa_comissao'] == float(TAXA_COMISSAO_VENDEDOR)
    assert dados['limite_bonus'] == float(LIMITE_BONUS_VENDEDOR)
    assert isinstance(dados['salario_total'], float)


# ---------- Tests de Freelancer ----------

def test_freelancer_salario_sem_bonus_horas():
    projetos = 5
    horas_trabalhadas = 80  # abaixo do limite de bônus
    freelancer = Freelancer.criar("Pedro Rocha", horas_trabalhadas, projetos=projetos)
    salario_esperado = Decimal(projetos) * PAGAMENTO_POR_PROJETO
    assert freelancer.salario_mensal() == salario_esperado

def test_freelancer_salario_com_bonus_horas():
    projetos = 5
    horas_trabalhadas = 120  # acima do limite de 100
    freelancer = Freelancer.criar("Pedro Rocha", horas_trabalhadas, projetos=projetos)
    salario_esperado = (Decimal(projetos) * PAGAMENTO_POR_PROJETO) + BONUS_HORAS_FREELANCER
    assert freelancer.salario_mensal() == salario_esperado

def test_freelancer_salario_total_com_ferias():
    freelancer = Freelancer.criar("Luciana Silva", 120, projetos=3, ferias=True)
    salario_mensal = freelancer.salario_mensal()
    # Freelancer não recebe bônus de férias
    assert freelancer.salario_total() == salario_mensal.quantize(Decimal('0.01'))

def test_freelancer_projetos_negativos():
    with pytest.raises(ValueError, match="Número de projetos não pode ser negativo"):
        Freelancer.criar("Pedro Rocha", 80, projetos=-2)

def test_freelancer_projetos_invalido_string():
    with pytest.raises(ValueError, match="Número de projetos deve ser inteiro"):
        Freelancer.criar("Pedro Rocha", 80, projetos="três")

def test_freelancer_to_dict():
    freelancer = Freelancer.criar("Mariana Sousa", 90, projetos=4)
    dados = freelancer.to_dict()
    assert dados['nome'] == "Mariana Sousa"
    assert dados['tipo'] == "Freelancer"
    assert dados['projetos'] == 4
    assert dados['pagamento_por_projeto'] == float(PAGAMENTO_POR_PROJETO)
    assert dados['bonus_horas'] == float(BONUS_HORAS_FREELANCER)
    assert isinstance(dados['salario_total'], float)


# ---------- Tests de Fábrica de Funcionários ----------

def test_fabrica_tipo_invalido_retorna_none(caplog):
    """Fábrica deve retornar None e registrar erro no log quando o tipo não está registrado."""
    caplog.set_level("ERROR")
    resultado = FabricaFuncionario.criar("inexistente", "Nome Teste", 100)
    assert resultado is None
    assert "Tipo de funcionário não registrado" in caplog.text

def test_fabrica_vendedor_sem_vendas_retorna_none(caplog):
    """Fábrica deve retornar None quando vendas não for informado para Vendedor."""
    caplog.set_level("ERROR")
    resultado = FabricaFuncionario.criar("vendedor", "Teste Vendedor", 50)
    assert resultado is None
    assert "É obrigatório informar 'vendas' para Vendedor" in caplog.text

def test_fabrica_freelancer_sem_projetos_retorna_none(caplog):
    """Fábrica deve retornar None quando projetos não for informado para Freelancer."""
    caplog.set_level("ERROR")
    resultado = FabricaFuncionario.criar("freelancer", "Teste Freelancer", 50)
    assert resultado is None
    assert "É obrigatório informar 'projetos' para Freelancer" in caplog.text

def test_fabrica_registrar_tipo_personalizado():
    """Verifica que registrar tipo novo funciona e que a fábrica cria a instância corretamente."""
    class Dummy(Funcionario):
        def __init__(self, nome: str, horas: int, ferias: bool = False):
            super().__init__(nome, horas, ferias)

        @property
        def _bonus_ferias(self) -> Decimal:
            return Decimal('123.00')

        def salario_mensal(self) -> Decimal:
            return Decimal(self.horas) * Decimal('1.00')

    FabricaFuncionario.registrar_tipo("dummy", Dummy)
    instancia = FabricaFuncionario.criar("dummy", "Teste Dummy", 10, ferias=True)
    assert isinstance(instancia, Dummy)
    assert instancia.nome == "Teste Dummy"
    assert instancia.horas == 10
    # salário mensal deve ser 10 * 1.00 = 10.00
    assert instancia.salario_mensal() == Decimal('10.00')
    # salário total inclui bônus de férias 123.00
    assert instancia.salario_total() == (Decimal('10.00') + Decimal('123.00')).quantize(Decimal('0.01'))

def test_fabrica_cria_tipos_nativos_corretamente():
    """Verifica que a fábrica cria instâncias corretas para os tipos padrão."""
    est = FabricaFuncionario.criar("estagiario", "Pedro Teste", 50)
    assert isinstance(est, Estagiario)
    assert est.horas == 50

    efet = FabricaFuncionario.criar("efetivo", "João Exemplo", 200)
    assert isinstance(efet, Efetivo)
    assert efet.horas == 200

    vend = FabricaFuncionario.criar("vendedor", "Ana Teste", 40, vendas=3000)
    assert isinstance(vend, Vendedor)
    assert vend.vendas == Decimal('3000')

    freel = FabricaFuncionario.criar("freelancer", "Bia Teste", 100, projetos=2)
    assert isinstance(freel, Freelancer)
    assert freel.projetos == 2


# ---------- Tests de Relatórios ----------

def test_relatorio_texto_formatacao_estagiario():
    est = Estagiario.criar("João Silva", 80, ferias=True)
    rel = RelatorioTexto().gerar(est)
    assert "RELATÓRIO SALARIAL" in rel
    assert "Nome: João Silva" in rel
    assert "Cargo: Estagiario" in rel
    assert "Horas trabalhadas: 80h" in rel
    assert "Férias: Sim" in rel
    # Verifica formatação de salário total = (80*10) + 200 = 1000
    assert "Salário total: R$ 1.000,00" in rel

def test_relatorio_texto_formatacao_efetivo():
    efet = Efetivo.criar("Carlos Lima", 100, ferias=False)
    rel = RelatorioTexto().gerar(efet)
    assert "RELATÓRIO SALARIAL" in rel
    assert "Nome: Carlos Lima" in rel
    assert "Cargo: Efetivo" in rel
    assert "Horas trabalhadas: 100h" in rel
    assert "Férias: Não" in rel
    # Sem vendas/projetos extras, apenas salário base: 100 * 20 = 2000
    assert "Salário total: R$ 2.000,00" in rel

def test_relatorio_texto_formatacao_vendedor():
    vend = Vendedor.criar("Ana Silva", 80, vendas=5000.0)
    rel = RelatorioTexto().gerar(vend)
    assert "RELATÓRIO SALARIAL" in rel
    assert "Nome: Ana Silva" in rel
    assert "Cargo: Vendedor" in rel
    assert "Vendas: R$ 5.000,00" in rel
    # Comprovando valor completo: (80 * 15) + (5000 * 0.05) = 1200 + 250 = 1450
    assert "Salário total: R$ 1.450,00" in rel

def test_relatorio_texto_formatacao_freelancer():
    freel = Freelancer.criar("Maria Oliveira", 120, projetos=3)
    rel = RelatorioTexto().gerar(freel)
    assert "RELATÓRIO SALARIAL" in rel
    assert "Nome: Maria Oliveira" in rel
    assert "Cargo: Freelancer" in rel
    assert "Projetos concluídos: 3" in rel
    # Freelancer com 120h tem bônus de horas => (3*300) + 100 = 1000
    assert "Salário total: R$ 1.000,00" in rel

def test_formatacao_moeda_multiplos_milhares():
    """Garante que a formatação de moeda lida corretamente com milhares múltiplos."""
    rel = RelatorioTexto()
    resultado = rel._formatar_moeda(Decimal('1234567.89'))
    assert resultado == "R$ 1.234.567,89"

def test_relatorio_json_efetivo_valido():
    efet = Efetivo.criar("Beatriz Costa", 150, ferias=True)
    texto_json = RelatorioJSON().gerar(efet)
    dados = json.loads(texto_json)
    assert dados['nome'] == "Beatriz Costa"
    assert dados['tipo'] == "Efetivo"
    assert dados['horas'] == 150
    assert dados['ferias'] is True
    # Verifica chaves específicas de Efetivo
    assert dados['tarifa_hora'] == float(TARIFA_HORA_EFETIVO)
    assert dados['tarifa_extra'] == float(TARIFA_EXTRA_EFETIVO)
    assert dados['horas_limite'] == HORAS_LIMITE_EFETIVO
    assert 'salario_total' in dados

def test_relatorio_json_vendedor_valido():
    vend = Vendedor.criar("Patrícia Lima", 50, vendas=2000.0, ferias=False)
    texto_json = RelatorioJSON().gerar(vend)
    dados = json.loads(texto_json)
    assert dados['nome'] == "Patrícia Lima"
    assert dados['tipo'] == "Vendedor"
    assert dados['vendas'] == 2000.0
    assert dados['taxa_comissao'] == float(TAXA_COMISSAO_VENDEDOR)
    assert dados['limite_bonus'] == float(LIMITE_BONUS_VENDEDOR)
    assert 'salario_total' in dados

def test_relatorio_json_freelancer_valido():
    freel = Freelancer.criar("Mariana Sousa", 90, projetos=4, ferias=False)
    texto_json = RelatorioJSON().gerar(freel)
    dados = json.loads(texto_json)
    assert dados['nome'] == "Mariana Sousa"
    assert dados['tipo'] == "Freelancer"
    assert dados['projetos'] == 4
    assert dados['pagamento_por_projeto'] == float(PAGAMENTO_POR_PROJETO)
    assert dados['bonus_horas'] == float(BONUS_HORAS_FREELANCER)
    assert dados['ferias'] is False
    assert 'salario_total' in dados


# ---------- Tests de Métodos Abstratos ----------

def test_instanciar_funcionario_direto_lanca_type_error():
    with pytest.raises(TypeError):
        Funcionario("Nome Teste", 100)
