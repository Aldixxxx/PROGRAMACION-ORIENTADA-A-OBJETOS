"""
Pruebas automatizadas para Guardians of the Ancient Kingdom.
Ejecutar con: pytest -v test_personajes.py
"""

import pytest
from personajes import Guerrero, Mago, Arquero, Combate, Personaje


def test_creacion_guerrero():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    assert guerrero.nombre == "Arthas"
    assert guerrero.vida == 100
    assert guerrero.ataque == 30
    assert guerrero.defensa == 20


def test_creacion_mago():
    mago = Mago("Gandalf", 80, 40, 10)
    assert mago.vida == 80
    assert mago.ataque == 40
    assert mago.defensa == 10


def test_creacion_arquero():
    arquero = Arquero("Legolas", 90, 35, 15)
    assert arquero.vida == 90
    assert arquero.ataque == 35
    assert arquero.defensa == 15


def test_no_se_puede_instanciar_personaje_abstracto():
    with pytest.raises(TypeError):
        Personaje("Generico", 100, 30, 20)


@pytest.mark.parametrize("vida", [101, -1])
def test_vida_invalida(vida):
    with pytest.raises(ValueError):
        Guerrero("Error", vida, 30, 20)


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Mago("   ", 80, 40, 10)


@pytest.mark.parametrize("ataque", [0, -10])
def test_ataque_invalido(ataque):
    with pytest.raises(ValueError):
        Mago("Mago", 80, ataque, 10)


def test_defensa_negativa():
    with pytest.raises(ValueError):
        Arquero("Arquero", 90, 35, -1)


def test_ataque_guerrero():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    objetivo = Guerrero("Enemigo", 100, 20, 10)
    assert guerrero.atacar(objetivo) == 26
    assert objetivo.vida == 74


def test_ataque_mago_ignora_defensa():
    mago = Mago("Gandalf", 80, 40, 10)
    objetivo = Guerrero("Enemigo", 100, 20, 20)
    assert mago.atacar(objetivo) == 40
    assert objetivo.vida == 60


def test_disparo_critico_arquero():
    arquero = Arquero("Legolas", 90, 35, 15)
    objetivo = Guerrero("Enemigo", 100, 20, 15)
    assert arquero.atacar(objetivo) == 40
    assert objetivo.vida == 60


def test_arquero_sin_critico():
    arquero = Arquero("Legolas", 90, 35, 15)
    objetivo = Guerrero("Enemigo", 100, 20, 35)
    assert arquero.atacar(objetivo) == 0
    assert objetivo.vida == 100


def test_vida_nunca_negativa():
    personaje = Guerrero("Arthas", 20, 30, 20)
    danio = personaje.recibir_danio(50)
    assert personaje.vida == 0
    assert danio == 20


def test_danio_negativo_rechazado():
    personaje = Guerrero("Arthas", 100, 30, 20)
    with pytest.raises(ValueError):
        personaje.recibir_danio(-10)


def test_personaje_derrotado_no_puede_atacar():
    derrotado = Guerrero("Arthas", 0, 30, 20)
    objetivo = Mago("Gandalf", 80, 40, 10)
    with pytest.raises(ValueError):
        derrotado.atacar(objetivo)


def test_objetivo_invalido():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    with pytest.raises(TypeError):
        guerrero.atacar("Gandalf")


def test_combate_gandalf_gana():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)
    ganador = combate.iniciar()
    assert ganador is gandalf
    assert arthas.vida == 0
    assert gandalf.esta_vivo()


def test_empate_tecnico():
    tanque_1 = Guerrero("Tanque 1", 100, 10, 100)
    tanque_2 = Guerrero("Tanque 2", 100, 10, 100)
    combate = Combate(tanque_1, tanque_2)
    ganador = combate.iniciar()
    assert ganador is None
    assert tanque_1.esta_vivo()
    assert tanque_2.esta_vivo()
