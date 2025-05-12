from abc import ABC, abstractmethod
import math
from typing import Union

class Shape(ABC):
    """Classe abstrata base para todas as formas geométricas."""
    
    @abstractmethod
    def area(self) -> float:
        """Calcula a área da forma geométrica.
        
        Returns:
            float: Área calculada da forma
        """
        pass

class Square(Shape):
    """Representa um quadrado e calcula sua área."""
    
    def __init__(self, side: float):
        """Inicializa o quadrado com seu lado.
        
        Args:
            side (float): Comprimento do lado do quadrado
        """
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2

class Rectangle(Shape):
    """Representa um retângulo e calcula sua área."""
    
    def __init__(self, length: float, width: float):
        """Inicializa o retângulo com comprimento e largura.
        
        Args:
            length (float): Comprimento do retângulo
            width (float): Largura do retângulo
        """
        self.length = length
        self.width = width
    
    def area(self) -> float:
        return self.length * self.width

class Circle(Shape):
    """Representa um círculo e calcula sua área."""
    
    def __init__(self, radius: float):
        """Inicializa o círculo com seu raio.
        
        Args:
            radius (float): Raio do círculo
        """
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * (self.radius ** 2)

class ShapeFactory:
    """Factory para criação de objetos Shape."""
    
    @staticmethod
    def create_shape(shape_type: str, *args) -> Union[Shape, None]:
        """Cria uma instância de Shape baseada no tipo e parâmetros fornecidos.
        
        Args:
            shape_type (str): Tipo da forma ('quadrado', 'retangulo', 'circulo')
            *args: Argumentos necessários para a forma específica
            
        Returns:
            Union[Shape, None]: Instância da forma ou None se tipo não for reconhecido
        """
        shape_types = {
            'quadrado': Square,
            'retangulo': Rectangle,
            'circulo': Circle
        }
        
        shape_class = shape_types.get(shape_type.lower())
        if not shape_class:
            return None
            
        try:
            return shape_class(*args)
        except TypeError:
            raise ValueError(f"Argumentos inválidos para o tipo {shape_type}")

# Exemplo de uso
if __name__ == "__main__":
    shapes = [
        ShapeFactory.create_shape('quadrado', 4),
        ShapeFactory.create_shape('retangulo', 4, 5),
        ShapeFactory.create_shape('circulo', 3),
        ShapeFactory.create_shape('triangulo', 4, 5)
    ]
    
    for shape in shapes:
        if shape:
            print(f"Área de {shape.__class__.__name__}: {shape.area():.2f}")
        else:
            print("Tipo de forma não reconhecido")