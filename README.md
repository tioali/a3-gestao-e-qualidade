**Sistema de Gestão de Funcionários**
(salario-calc)

**Descrição**
Sistema para cálculo de salários de funcionários (Estagiário, Efetivo, Vendedor, Freelancer), com geração de relatórios em texto e JSON. Inclui:
- Validação de dados (horas, vendas, projetos).
- Cálculos precisos usando Decimal.
- Testes unitários robustos (94+ cenários).

**Funcionalidades**
Principais Recursos
- Cálculo Salarial: Salário base, horas extras, comissões, bônus de férias.
- Validações:	Nomes, horas não negativas, formatos numéricos.
- Relatórios:	Texto formatado e JSON para integração.
- Design Patterns:	Factory Method (FabricaFuncionario), Strategy (Relatorio).
  
**Instalação**
Pré-requisitos
- Python 3.8+
- Gerenciador de pacotes pip.

Passos
Clone o repositório:
- git clone https://github.com/seu-usuario/gestao-funcionarios.git
- cd gestao-funcionarios 
Instale as dependências:
- pip install pytest  

Como Usar
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
  
- Saída (JSON formatado):

        {  
          "nome": "João Costa",  
          "horas": 80,  
          "ferias": false,  
          "tipo": "Vendedor",  
          "vendas": 20000.0,  
          "salario_total": 2800.00  
        }  

Testes

- Executar Testes
        pytest test_funcionarios.py -v
  
- Cobertura dos Testes
    Validação de Dados:	Nomes vazios, horas negativas, vendas inválidas.
    Cálculos:	Horas extras, comissões, casos de borda.
    Relatórios:	Formatação de moeda, JSON válido.
    Exceções:	Tipos não registrados, parâmetros faltantes.
  
Estrutura do Projeto
- Arquivos Principais
    funcionarios.py:	Classes Funcionario, Estagiario, Vendedor, etc.
    test_funcionarios.py:	Testes unitários para todas as funcionalidades.
  
- Fluxo do Sistema
    Criação de Funcionário: Via FabricaFuncionario.
    Cálculo Salarial: salario_total() combina salário base e bônus.
    Geração de Relatório: RelatorioTexto ou RelatorioJSON.

Contato
- Autores / RA: 
Matheus Esteves / 3322210957

