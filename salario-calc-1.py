from abc import ABC, abstractmethod
from typing import Optional

class Funcionario(ABC):
    """Base para diferentes tipos de funcionários."""

    def __init__(self, nome: str, horas: int, ferias: bool = False):
        self.nome = nome
        self.horas = horas
        self.ferias = ferias

    @abstractmethod
    def salario_mensal(self) -> float:
        pass

    def adicional_ferias(self) -> float:
        return 0.0

    def salario_total(self) -> float:
        return self.salario_mensal() + self.adicional_ferias()


class Estagiario(Funcionario):
    VALOR_HORA = 10.0
    BONUS_FERIAS = 200.0

    def salario_mensal(self) -> float:
        return self.horas * self.VALOR_HORA

    def adicional_ferias(self) -> float:
        return self.BONUS_FERIAS if self.ferias else 0.0


class Efetivo(Funcionario):
    TARIFA_HORA = 20.0
    TARIFA_EXTRA = 25.0
    HORAS_LIMITE = 180
    ADICIONAL_FERIAS = 1000.0

    def salario_mensal(self) -> float:
        if self.horas <= self.HORAS_LIMITE:
            return self.horas * self.TARIFA_HORA
        extras = self.horas - self.HORAS_LIMITE
        return (self.HORAS_LIMITE * self.TARIFA_HORA) + (extras * self.TARIFA_EXTRA)

    def adicional_ferias(self) -> float:
        return self.ADICIONAL_FERIAS if self.ferias else 0.0


class Vendedor(Funcionario):
    TARIFA_HORA = 15.0
    TAXA_COMISSAO = 0.05
    BONUS_VENDAS = 500.0
    LIMITE_BONUS = 10000.0
    BONUS_FERIAS = 800.0

    def __init__(self, nome: str, horas: int, vendas: float, ferias: bool = False):
        super().__init__(nome, horas, ferias)
        self.vendas = vendas

    def salario_mensal(self) -> float:
        base = self.horas * self.TARIFA_HORA
        comissao = self.vendas * self.TAXA_COMISSAO
        bonus = self.BONUS_VENDAS if self.vendas > self.LIMITE_BONUS else 0.0
        return base + comissao + bonus

    def adicional_ferias(self) -> float:
        return self.BONUS_FERIAS if self.ferias else 0.0


class Freelancer(Funcionario):
    PAGAMENTO_POR_PROJETO = 300.0
    EXTRA_HORAS = 100.0
    HORAS_BONUS = 100

    def __init__(self, nome: str, horas: int, projetos: int, ferias: bool = False):
        super().__init__(nome, horas, ferias)
        self.projetos = projetos

    def salario_mensal(self) -> float:
        total = self.projetos * self.PAGAMENTO_POR_PROJETO
        if self.horas > self.HORAS_BONUS:
            total += self.EXTRA_HORAS
        return total


class RelatorioSalario:
    """Responsável por gerar relatórios salariais."""

    @staticmethod
    def gerar(func: Funcionario) -> str:
        linhas = [
            f"Nome: {func.nome}",
            f"Cargo: {func.__class__.__name__}",
            f"Horas trabalhadas: {func.horas}",
            f"Férias: {'Sim' if func.ferias else 'Não'}"
        ]

        if isinstance(func, Vendedor):
            linhas.append(f"Vendas: {func.vendas}")
        if isinstance(func, Freelancer):
            linhas.append(f"Projetos: {func.projetos}")

        linhas.append(f"Salário total: R$ {func.salario_total():.2f}")
        linhas.append("-" * 30)
        return "\n".join(linhas)


class CriadorFuncionarios:
    """Fábrica de funcionários baseada em tipo."""

    @staticmethod
    def criar(
        tipo: str,
        nome: str,
        horas: int,
        vendas: Optional[float] = None,
        projetos: Optional[int] = None,
        ferias: bool = False
    ) -> Optional[Funcionario]:

        tipos = {
            'estagiario': lambda: Estagiario(nome, horas, ferias),
            'efetivo': lambda: Efetivo(nome, horas, ferias),
            'vendedor': lambda: Vendedor(nome, horas, vendas or 0.0, ferias),
            'freelancer': lambda: Freelancer(nome, horas, projetos or 0, ferias)
        }

        try:
            return tipos[tipo]()
        except KeyError:
            print(f"Tipo de funcionário inválido: '{tipo}'")
        except Exception as erro:
            print(f"Erro ao criar funcionário '{nome}': {erro}")
        return None


# Exemplo de uso
if __name__ == "__main__":
    lista = [
        CriadorFuncionarios.criar('estagiario', 'João Silva', 160, ferias=True),
        CriadorFuncionarios.criar('efetivo', 'Maria Souza', 200),
        CriadorFuncionarios.criar('vendedor', 'Carlos Lima', 180, vendas=15000.0),
        CriadorFuncionarios.criar('freelancer', 'Ana Costa', 120, projetos=4),
        CriadorFuncionarios.criar('gerente', 'Teste Inválido', 0)
    ]

    for funcionario in lista:
        if funcionario:
            print(RelatorioSalario.gerar(funcionario))
        else:
            print("Erro ao gerar relatório.\n" + "-" * 30)
