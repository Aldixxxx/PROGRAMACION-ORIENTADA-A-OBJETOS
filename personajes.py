"""
Guardians of the Ancient Kingdom
Sistema de combate por turnos orientado a objetos.

Este módulo define las clases del sistema:
Personaje (abstracta), Guerrero, Mago, Arquero y Combate.
"""

from abc import ABC, abstractmethod
import math


class Personaje(ABC):
    """Clase abstracta que representa las características comunes de un guardián."""

    def __init__(self, nombre: str, vida: int, ataque: int, defensa: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    # ------------------- Encapsulamiento y validaciones -------------------

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.__nombre = valor.strip()

    @property
    def vida(self) -> int:
        return self.__vida

    @vida.setter
    def vida(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("La vida debe ser un número entero.")
        if valor < 0 or valor > 100:
            raise ValueError("La vida debe estar entre 0 y 100.")
        self.__vida = valor

    @property
    def ataque(self) -> int:
        return self.__ataque

    @ataque.setter
    def ataque(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("El ataque debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El ataque debe ser un entero positivo.")
        self.__ataque = valor

    @property
    def defensa(self) -> int:
        return self.__defensa

    @defensa.setter
    def defensa(self, valor: int):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("La defensa debe ser un número entero.")
        if valor < 0:
            raise ValueError("La defensa no puede ser negativa.")
        self.__defensa = valor

    # ------------------------- Métodos comunes ---------------------------

    def recibir_danio(self, cantidad: int) -> int:
        """Aplica un daño ya calculado. Devuelve el daño efectivamente recibido."""
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise TypeError("El daño debe ser un número entero.")
        if cantidad < 0:
            raise ValueError("El daño no puede ser negativo.")

        vida_antes = self.__vida
        self.__vida = max(0, vida_antes - cantidad)
        return vida_antes - self.__vida

    def esta_vivo(self) -> bool:
        return self.__vida > 0

    def mostrar_estado(self) -> str:
        tipo = type(self).__name__
        return (
            f"{tipo} {self.nombre} | Vida: {self.vida} | "
            f"Ataque: {self.ataque} | Defensa: {self.defensa}"
        )

    @abstractmethod
    def atacar(self, objetivo: "Personaje") -> int:
        """Cada subclase debe definir su propia forma de atacar."""
        pass

    def _validar_ataque(self, objetivo: "Personaje"):
        """Validaciones comunes antes de ejecutar cualquier ataque."""
        if not isinstance(objetivo, Personaje):
            raise TypeError("El objetivo debe ser una instancia de Personaje.")
        if not self.esta_vivo():
            raise ValueError(f"{self.nombre} está derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")


class Guerrero(Personaje):
    """Guerrero: su ataque aumenta 20% antes de descontar la defensa enemiga."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)

        ataque_potenciado = math.floor(self.ataque * 1.20)
        danio = max(0, ataque_potenciado - objetivo.defensa)
        danio_recibido = objetivo.recibir_danio(danio)

        print(
            f"{self.nombre} usa Golpe poderoso contra {objetivo.nombre} "
            f"y causa {danio_recibido} de daño."
        )
        return danio_recibido


class Mago(Personaje):
    """Mago: su hechizo ignora completamente la defensa del objetivo."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)

        danio = self.ataque
        danio_recibido = objetivo.recibir_danio(danio)

        print(
            f"{self.nombre} lanza un Hechizo penetrante contra {objetivo.nombre} "
            f"y causa {danio_recibido} de daño."
        )
        return danio_recibido


class Arquero(Personaje):
    """Arquero: duplica el daño base cuando su ataque supera la defensa enemiga."""

    def atacar(self, objetivo: Personaje) -> int:
        self._validar_ataque(objetivo)

        danio_base = max(0, self.ataque - objetivo.defensa)

        if self.ataque > objetivo.defensa:
            danio = danio_base * 2
            habilidad = "Disparo crítico"
        else:
            danio = 0
            habilidad = "disparo sin efecto"

        danio_recibido = objetivo.recibir_danio(danio)

        print(
            f"{self.nombre} usa {habilidad} contra {objetivo.nombre} "
            f"y causa {danio_recibido} de daño."
        )
        return danio_recibido


class Combate:
    """Administra un enfrentamiento por turnos entre dos personajes."""

    MAX_RONDAS = 50

    def __init__(self, personaje_1: Personaje, personaje_2: Personaje):
        if not isinstance(personaje_1, Personaje) or not isinstance(personaje_2, Personaje):
            raise TypeError("Ambos participantes deben ser instancias de Personaje.")
        if personaje_1 is personaje_2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")

        self.__personaje_1 = personaje_1
        self.__personaje_2 = personaje_2
        self.__atacante = personaje_1
        self.__defensor = personaje_2
        self.__ronda = 1
        self.__rondas_sin_danio = 0
        self.__ganador = None
        self.__empate_tecnico = False

    @property
    def ganador(self):
        return self.__ganador

    def cambiar_turno(self):
        self.__atacante, self.__defensor = self.__defensor, self.__atacante

    def verificar_ganador(self):
        if not self.__personaje_1.esta_vivo():
            self.__ganador = self.__personaje_2
        elif not self.__personaje_2.esta_vivo():
            self.__ganador = self.__personaje_1
        return self.__ganador

    def mostrar_resultado(self):
        print("\n===== RESULTADO FINAL =====")
        print(self.__personaje_1.mostrar_estado())
        print(self.__personaje_2.mostrar_estado())

        if self.__ganador:
            print(f"\nGanador: {self.__ganador.nombre}")
        elif self.__empate_tecnico:
            print("\nResultado: Empate técnico por falta de daño.")
        else:
            print("\nResultado: Empate por límite de 50 rondas.")

    def iniciar(self):
        print("\n===== INICIO DEL COMBATE =====")
        print(self.__personaje_1.mostrar_estado())
        print(self.__personaje_2.mostrar_estado())

        while self.__ronda <= self.MAX_RONDAS:
            print(f"\n--- Ronda {self.__ronda} ---")

            danio = self.__atacante.atacar(self.__defensor)

            if danio == 0:
                self.__rondas_sin_danio += 1
            else:
                self.__rondas_sin_danio = 0

            print(self.__personaje_1.mostrar_estado())
            print(self.__personaje_2.mostrar_estado())

            if self.verificar_ganador():
                break

            if self.__rondas_sin_danio >= 2:
                self.__empate_tecnico = True
                break

            self.cambiar_turno()

            if self.__atacante is self.__personaje_1:
                self.__ronda += 1

        self.mostrar_resultado()
        return self.__ganador
