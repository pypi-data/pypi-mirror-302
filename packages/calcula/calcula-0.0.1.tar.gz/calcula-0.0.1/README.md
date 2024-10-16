# Laboratório de Python: uma calculadora
Laboratório de calculadora python para publicar no Pypi. Handson para o Curso NTT DATA - Engenharia de Dados com Python da plataforma DIO. Este é um script de uma calculadora básica em Python que suporta diversas operações matemáticas, como soma, subtração, multiplicação, divisão, potência, raiz quadrada e raiz cúbica. A função principal é a `calcula`, que recebe como parâmetros a operação a ser realizada e uma lista de números sobre os quais a operação será aplicada.

## Funcionalidades

- **Soma**: Calcula a soma de todos os números da lista.
- **Subtração**: Subtrai todos os números da lista a partir do primeiro.
- **Multiplicação**: Calcula o produto de todos os números da lista.
- **Divisão**: Divide o primeiro número pelo produto dos números restantes.
- **Potência**: Eleva o primeiro número ao segundo número (suporta apenas dois números).
- **Raiz Quadrada**: Calcula a raiz quadrada do primeiro número da lista.
- **Raiz Cúbica**: Calcula a raiz cúbica do primeiro número da lista.

## Uso

### Função `calcula`

```python
def calcula(operacao: str, numeros: list[float]) -> float:
```

#### Parâmetros:
- `operacao` (str): Uma string que define a operação a ser realizada. Pode ser:
  - `"soma"`
  - `"subtracao"`
  - `"multiplicacao"`
  - `"divisao"`
  - `"potencia"`
  - `"raiz_quadrada"`
  - `"raiz_cubica"`
- `numeros` (list[float]): Uma lista de números de ponto flutuante sobre os quais a operação será realizada.

#### Retorno:
- Retorna o resultado da operação como um número de ponto flutuante.

#### Exceções:
- `ValueError`: Lança uma exceção caso a operação seja inválida ou se houver uma divisão por zero.

### Exemplo de Uso

```python
# Realizando a soma de 10, 20 e 30
resultado = calcula("soma", [10.0, 20.0, 30.0])
print(resultado)  # Saída: 60.0

# Realizando a divisão de 10 por 5
resultado = calcula("divisao", [10.0, 5.0])
print(resultado)  # Saída: 2.0
```

## Exceções Tratadas

A função `calcula` trata as seguintes exceções:
- **Divisão por zero**: Gera uma mensagem de erro específica para divisões por zero.
- **Operação inválida**: Retorna um erro se a operação não estiver entre as suportadas.
- **Erro de tipo ou índice**: Caso os parâmetros não correspondam aos esperados para uma operação específica, uma mensagem de erro é gerada.

## Requisitos

A função utiliza o módulo `math` para operações avançadas, como potência e raiz quadrada. Este módulo é parte da biblioteca padrão do Python.

