from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type, TypeVar
import logging
import json
from decimal import Decimal, ROUND_HALF_UP

# Configuração avançada de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('funcionarios.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

FuncionarioType = TypeVar('FuncionarioType', bound='Funcionario')


class Funcionario(ABC):
    """Classe abstrata base para todos os tipos de funcionários.

    Attributes:
        nome (str): Nome completo do funcionário.
        horas (int): Horas trabalhadas no mês.
        ferias (bool): Indica se o funcionário está em período de férias.
    """

    def __init__(self, nome: str, horas: int, ferias: bool = False):
        # Validação e formatação de nome
        self.nome = nome
        # Aceitar horas como int ou float inteiro
        self.horas = horas
        self.ferias = ferias

    @property
    def nome(self) -> str:
        """Nome do funcionário com formatação padrão (title case)."""
        return self._nome

    @nome.setter
    def nome(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Nome deve ser uma string")
        value_stripped = value.strip()
        if not value_stripped:
            raise ValueError("Nome não pode ser vazio ou conter apenas espaços")
        # Converte cada palavra para Title Case
        self._nome = " ".join(word.capitalize() for word in value_stripped.split())

    @property
    def horas(self) -> int:
        """Horas trabalhadas com validação de valor mínimo."""
        return self._horas

    @horas.setter
    def horas(self, value: Any):
        # Permitir float inteiro
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("Horas trabalhadas deve ser inteiro ou float equivalente a inteiro")
            value = int(value)
        if not isinstance(value, int):
            raise ValueError("Horas trabalhadas deve ser um número inteiro")
        if value < 0:
            raise ValueError("Horas trabalhadas não podem ser negativas")
        self._horas = value

    @property
    def ferias(self) -> bool:
        """Status de férias do funcionário."""
        return self._ferias

    @ferias.setter
    def ferias(self, value: Any):
        self._ferias = bool(value)

    @abstractmethod
    def salario_mensal(self) -> Decimal:
        """Calcula o salário base mensal."""
        pass

    @property
    @abstractmethod
    def _bonus_ferias(self) -> Decimal:
        """Retorna o valor do bônus de férias específico da classe."""
        pass

    def adicional_ferias(self) -> Decimal:
        """Calcula o adicional de férias quando aplicável."""
        return self._bonus_ferias if self.ferias else Decimal('0.00')

    def salario_total(self) -> Decimal:
        """Calcula o salário total com todos os adicionais."""
        total = self.salario_mensal() + self.adicional_ferias()
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def to_dict(self) -> Dict[str, Any]:
        """Serializa os dados do funcionário para dicionário."""
        data: Dict[str, Any] = {
            'nome': self.nome,
            'horas': self.horas,
            'ferias': self.ferias,
            'tipo': self.__class__.__name__,
            'salario_total': float(self.salario_total())
        }
        return data

    @classmethod
    def criar(
        cls: Type[FuncionarioType],
        nome: str,
        horas: Any,
        ferias: bool = False,
        **dados_extra
    ) -> FuncionarioType:
        """Método fábrica para criação de instâncias com validação integrada."""
        return cls(nome=nome, horas=horas, ferias=ferias, **dados_extra)


class Estagiario(Funcionario):
    VALOR_HORA = Decimal('10.00')
    BONUS_FERIAS = Decimal('200.00')

    @property
    def _bonus_ferias(self) -> Decimal:
        return self.BONUS_FERIAS

    def salario_mensal(self) -> Decimal:
        return Decimal(self.horas) * self.VALOR_HORA

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['valor_hora'] = float(self.VALOR_HORA)
        return data


class Efetivo(Funcionario):
    TARIFA_HORA = Decimal('20.00')
    TARIFA_EXTRA = Decimal('25.00')
    HORAS_LIMITE = 180
    BONUS_FERIAS = Decimal('1000.00')

    @property
    def _bonus_ferias(self) -> Decimal:
        return self.BONUS_FERIAS

    def salario_mensal(self) -> Decimal:
        if self.horas <= self.HORAS_LIMITE:
            return Decimal(self.horas) * self.TARIFA_HORA
        extras = Decimal(self.horas - self.HORAS_LIMITE)
        return (Decimal(self.HORAS_LIMITE) * self.TARIFA_HORA) + (extras * self.TARIFA_EXTRA)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'tarifa_hora': float(self.TARIFA_HORA),
            'tarifa_extra': float(self.TARIFA_EXTRA),
            'horas_limite': self.HORAS_LIMITE
        })
        return data


class Vendedor(Funcionario):
    TARIFA_HORA = Decimal('15.00')
    TAXA_COMISSAO = Decimal('0.05')
    BONUS_VENDAS = Decimal('500.00')
    LIMITE_BONUS = Decimal('10000.00')
    BONUS_FERIAS = Decimal('800.00')

    def __init__(self, nome: str, horas: Any, vendas: Any, ferias: bool = False):
        super().__init__(nome, horas, ferias)
        # Converter vendas para Decimal (aceita str, float, int)
        try:
            self.vendas = Decimal(str(vendas))
        except Exception:
            raise ValueError("Valor de vendas deve ser numérico ou string numérica")

    @property
    def vendas(self) -> Decimal:
        return self._vendas

    @vendas.setter
    def vendas(self, value: Any):
        try:
            decimal_val = Decimal(str(value))
        except Exception:
            raise ValueError("Valor de vendas não pode ser convertido para Decimal")
        if decimal_val < Decimal('0'):
            raise ValueError("Valor de vendas não pode ser negativo")
        self._vendas = decimal_val

    @property
    def _bonus_ferias(self) -> Decimal:
        return self.BONUS_FERIAS

    def salario_mensal(self) -> Decimal:
        base = Decimal(self.horas) * self.TARIFA_HORA
        comissao = self.vendas * self.TAXA_COMISSAO
        bonus = self.BONUS_VENDAS if self.vendas > self.LIMITE_BONUS else Decimal('0.00')
        return base + comissao + bonus

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'vendas': float(self.vendas),
            'taxa_comissao': float(self.TAXA_COMISSAO),
            'limite_bonus': float(self.LIMITE_BONUS)
        })
        return data


class Freelancer(Funcionario):
    PAGAMENTO_POR_PROJETO = Decimal('300.00')
    BONUS_HORAS = Decimal('100.00')
    LIMITE_HORAS_BONUS = 100
    BONUS_FERIAS = Decimal('0.00')  # Freelancers não têm bônus de férias

    def __init__(self, nome: str, horas: Any, projetos: Any, ferias: bool = False):
        super().__init__(nome, horas, ferias)
        # Validar projetos como int
        self.projetos = projetos

    @property
    def projetos(self) -> int:
        return self._projetos

    @projetos.setter
    def projetos(self, value: Any):
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("Número de projetos deve ser inteiro")
            value = int(value)
        if not isinstance(value, int):
            raise ValueError("Número de projetos deve ser inteiro")
        if value < 0:
            raise ValueError("Número de projetos não pode ser negativo")
        self._projetos = value

    @property
    def _bonus_ferias(self) -> Decimal:
        return self.BONUS_FERIAS

    def salario_mensal(self) -> Decimal:
        total = Decimal(self.projetos) * self.PAGAMENTO_POR_PROJETO
        if self.horas > self.LIMITE_HORAS_BONUS:
            total += self.BONUS_HORAS
        return total

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'projetos': self.projetos,
            'pagamento_por_projeto': float(self.PAGAMENTO_POR_PROJETO),
            'bonus_horas': float(self.BONUS_HORAS),
            'limite_horas_bonus': self.LIMITE_HORAS_BONUS
        })
        return data


class Relatorio(ABC):
    """Interface para geração de relatórios de funcionários."""

    @abstractmethod
    def gerar(self, funcionario: Funcionario) -> str:
        pass


class RelatorioTexto(Relatorio):
    cabecalho: str = "RELATÓRIO SALARIAL"
    separador: str = "-" * 40
    moeda: str = "R$"

    def _formatar_moeda(self, valor: Decimal) -> str:
        texto = f"{self.moeda} {valor:,.2f}"
        # Trocar separadores para formato brasileiro
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")

    def gerar(self, funcionario: Funcionario) -> str:
        dados = funcionario.to_dict()
        linhas = [
            self.cabecalho,
            f"Nome: {dados['nome']}",
            f"Cargo: {dados['tipo']}",
            f"Horas trabalhadas: {dados['horas']}h",
            f"Férias: {'Sim' if dados['ferias'] else 'Não'}"
        ]

        if isinstance(funcionario, Vendedor):
            linhas.append(f"Vendas: {self._formatar_moeda(Decimal(str(dados['vendas'])))}")

        if isinstance(funcionario, Freelancer):
            linhas.append(f"Projetos concluídos: {dados['projetos']}")

        linhas.append(f"Salário total: {self._formatar_moeda(Decimal(str(dados['salario_total'])))}")
        linhas.append(self.separador)

        return "\n".join(linhas)


class RelatorioJSON(Relatorio):
    indent: int = 2
    ensure_ascii: bool = False

    def gerar(self, funcionario: Funcionario) -> str:
        dados = funcionario.to_dict()
        return json.dumps(dados, indent=self.indent, ensure_ascii=self.ensure_ascii)


class FabricaFuncionario:
    """Fábrica para criação de funcionários com registro dinâmico de tipos."""

    _tipos_registrados: Dict[str, Type[Funcionario]] = {
        'estagiario': Estagiario,
        'efetivo': Efetivo,
        'vendedor': Vendedor,
        'freelancer': Freelancer
    }

    @classmethod
    def registrar_tipo(cls, nome: str, tipo_funcionario: Type[Funcionario]):
        """Registra um novo tipo de funcionário na fábrica."""
        if not issubclass(tipo_funcionario, Funcionario):
            raise ValueError("Tipo deve ser uma subclasse de Funcionario")
        cls._tipos_registrados[nome.lower()] = tipo_funcionario

    @classmethod
    def criar(
        cls,
        tipo: str,
        nome: str,
        horas: Any,
        vendas: Optional[Any] = None,
        projetos: Optional[Any] = None,
        ferias: bool = False
    ) -> Optional[Funcionario]:
        """Cria uma instância do tipo de funcionário especificado."""
        try:
            tipo_lower = tipo.lower()
            if tipo_lower not in cls._tipos_registrados:
                raise ValueError(f"Tipo de funcionário não registrado: '{tipo}'")

            dados_extra: Dict[str, Any] = {'ferias': ferias}

            if tipo_lower == 'vendedor':
                if vendas is None:
                    raise ValueError("É obrigatório informar 'vendas' para Vendedor")
                dados_extra['vendas'] = vendas

            if tipo_lower == 'freelancer':
                if projetos is None:
                    raise ValueError("É obrigatório informar 'projetos' para Freelancer")
                dados_extra['projetos'] = projetos

            return cls._tipos_registrados[tipo_lower].criar(
                nome=nome, horas=horas, **dados_extra
            )

        except ValueError as ve:
            logger.error(f"Erro de validação: {ve}")
        except Exception as e:
            logger.exception(f"Erro inesperado ao criar funcionário: {e}")

        return None
