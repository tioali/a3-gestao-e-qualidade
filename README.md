# Sistema de Gestão de Funcionários

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Testes](https://img.shields.io/badge/Testes-Pytest-brightgreen)](https://docs.pytest.org/)

Sistema para cálculo de salários, geração de relatórios e gestão de funcionários (Estagiário, Efetivo, Vendedor, Freelancer), com testes unitários robustos.

---

## Funcionalidades

- **Cálculos Automatizados**:
  - Salário base, horas extras, comissões e bônus de férias.
  - Precisão monetária com `Decimal` para evitar erros de arredondamento.
- **Validações**:
  - Nomes, horas trabalhadas, vendas e projetos.
  - Tratamento de erros e logs detalhados em `funcionarios.log`.
- **Relatórios**:
  - **Texto**: Formatação legível (ex: `R$ 1.000,00`).
  - **JSON**: Pronto para integração com APIs externas.
- **Padrões de Projeto**:
  - **Factory Method**: Criação dinâmica de funcionários via `FabricaFuncionario`.
  - **Strategy**: Geração flexível de relatórios (`RelatorioTexto` e `RelatorioJSON`).

---

## Instalação

1. **Pré-requisitos**:
   - Python 3.8 ou superior.
   - Gerenciador de pacotes `pip`.

2. **Clonar Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/gestao-funcionarios.git
   cd gestao-funcionarios

**Passos**
Clone o repositório:
- git clone https://github.com/seu-usuario/gestao-funcionarios.git
- cd gestao-funcionarios 
Instale as dependências:
- pip install pytest  

## Como Usar
- Exemplo 1: Criar Funcionário
  
        from funcionarios import FabricaFuncionario  
        # Criar um estagiário  
        estagiario = FabricaFuncionario.criar(  
            tipo="estagiario",  
            nome="Maria Silva",  
            horas=160  
        )  
      # Calcular salário total  
      print(f"Salário Total: R$ {estagiario.salario_total()}")  
  - Saída:
        Salário Total: R$ 1.600,00

- Exemplo 2: Gerar Relatório em JSON

      from funcionarios import RelatorioJSON  
      vendedor = FabricaFuncionario.criar(  
            tipo="vendedor",  
            nome="João Costa",  
            horas=80,  
            vendas=20000.0  
        )  

      relatorio_json = RelatorioJSON().gerar(vendedor)  
      print(relatorio_json)
  
-   Saída (JSON formatado):

        {  
          "nome": "João Costa",  
          "horas": 80,  
          "ferias": false,  
          "tipo": "Vendedor",  
          "vendas": 20000.0,  
          "salario_total": 2800.00  
        }  

## Teste
**Execute todos os Testes com:**
        
        pytest test_funcionarios.py -v
  
- Cobertura dos Testes
    Validação de Dados:	Nomes vazios, horas negativas, vendas inválidas.
    Cálculos:	Horas extras, comissões, casos de borda.
    Relatórios:	Formatação de moeda, JSON válido.
    Exceções:	Tipos não registrados, parâmetros faltantes.
  
**Estrutura do Projeto**

- Arquivos Principais
    funcionarios.py:	Classes Funcionario, Estagiario, Vendedor, etc.
    test_funcionarios.py:	Testes unitários para todas as funcionalidades.
  
- Fluxo do Sistema
    Criação de Funcionário: Via FabricaFuncionario.
    Cálculo Salarial: salario_total() combina salário base e bônus.
    Geração de Relatório: RelatorioTexto ou RelatorioJSON.

## Implantação
  Logs: Todos os erros são registrados em funcionarios.log.
  Personalização: Para adicionar novos tipos de funcionários:
  Crie uma subclass de Funcionario.

- Registre-a na fábrica:

      FabricaFuncionario.registrar_tipo("novo_tipo", NovoFuncionario)

## Construído com
- Python - Linguagem principal
- pytest - Framework de testes
- Decimal (módulo padrão) - Precisão monetária
- logging (módulo padrão) - Gestão de logs

## Desenvolvedores
- Autores / RA: 
Matheus Esteves / 3322210957

