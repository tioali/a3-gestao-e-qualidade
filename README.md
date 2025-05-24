**Sistema de Gestão de Funcionários**
(salario-calc)

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

## Contato
- Autores / RA: 
Matheus Esteves / 3322210957

