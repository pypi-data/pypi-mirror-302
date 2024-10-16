def calcula(operacao: str, numeros: list[float]) -> float:
    """
    Executa uma operação matemática sobre uma lista de números.

    Parâmetros:
    - operacao: str - a operação matemática a ser realizada (soma, subtração, divisão, multiplicação, potência, raiz quadrada ou raiz cúbica).
    - numeros: list[float] - uma lista de números de ponto flutuante.

    Retorna:
    - float - o resultado da operação.

    Exceções:
    - ValueError: para operações inválidas ou divisão por zero.
    """
    import math

    # Dicionário de operações suportadas
    operacoes = {
        "soma": sum,
        "subtracao": lambda nums: nums[0] - sum(nums[1:]),
        "multiplicacao": lambda nums: math.prod(nums),
        "divisao": lambda nums: nums[0] / math.prod(nums[1:]) if 0 not in nums[1:] else float('inf'),
        "potencia": lambda nums: math.pow(nums[0], nums[1]),
        "raiz_quadrada": lambda nums: math.sqrt(nums[0]),
        "raiz_cubica": lambda nums: nums[0] ** (1/3)
    }
    
    # Verificar se a operação é suportada
    if operacao not in operacoes:
        raise ValueError(f"Operação '{operacao}' não é suportada.")
    
    # Tentar executar a operação e retornar o resultado
    try:
        resultado = operacoes[operacao](numeros)
    except ZeroDivisionError:
        raise ValueError("Divisão por zero não permitida.")
    except (TypeError, IndexError):
        raise ValueError("Entrada inválida para a operação.")

    return resultado

# Exemplo de chamada para testar a função refatorada
operacao = "soma"
numeros = [10.0, 20.0, 30.0]
resultado = calcula(operacao, numeros)
print("O resultado da operação e:", resultado)  # Imprime o resultado
