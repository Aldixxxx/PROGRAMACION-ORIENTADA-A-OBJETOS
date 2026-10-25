"""
Guardians of the Ancient Kingdom
Archivo principal: crea personajes, ejecuta combates y realiza los casos de prueba.
"""

from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def separador(titulo: str):
    print(f"\n{'=' * 15} {titulo} {'=' * 15}")


def probar_creacion_personajes():
    separador("Caso 1: creación correcta de personajes")

    guerrero = Guerrero("Arthas", 100, 30, 20)
    mago = Mago("Gandalf", 80, 40, 10)
    arquero = Arquero("Legolas", 90, 35, 15)

    print(guerrero.mostrar_estado())
    print(mago.mostrar_estado())
    print(arquero.mostrar_estado())

    assert guerrero.vida == 100
    assert mago.ataque == 40
    assert arquero.defensa == 15
    print("Resultado: los tres personajes se crearon correctamente.")


def probar_validaciones():
    separador("Casos 2 a 4: validaciones de creación")

    pruebas = [
        ("Vida mayor a 100", lambda: Guerrero("Error", 120, 30, 20)),
        ("Vida negativa", lambda: Guerrero("Error", -5, 30, 20)),
        ("Nombre vacío", lambda: Mago("   ", 80, 40, 10)),
        ("Ataque inválido", lambda: Mago("Mago", 80, 0, 10)),
        ("Defensa negativa", lambda: Arquero("Arquero", 90, 35, -1)),
    ]

    for descripcion, accion in pruebas:
        try:
            accion()
            print(f"{descripcion}: ERROR, se permitió un valor inválido.")
            assert False, descripcion
        except (ValueError, TypeError) as error:
            print(f"{descripcion}: rechazado correctamente -> {error}")

    print("Resultado: todas las validaciones funcionan.")


def probar_habilidades():
    separador("Casos 5 a 7: habilidades especiales")

    guerrero = Guerrero("Arthas", 100, 30, 20)
    objetivo_guerrero = Guerrero("Enemigo", 100, 20, 10)
    danio_guerrero = guerrero.atacar(objetivo_guerrero)
    assert danio_guerrero == 26  # floor(30 * 1.20) - 10 = 36 - 10
    print(f"Guerrero causó {danio_guerrero} de daño. Esperado: 26.")

    mago = Mago("Gandalf", 80, 40, 10)
    objetivo_mago = Guerrero("Enemigo", 100, 20, 20)
    danio_mago = mago.atacar(objetivo_mago)
    assert danio_mago == 40  # ignora la defensa
    print(f"Mago causó {danio_mago} de daño. Esperado: 40.")

    arquero = Arquero("Legolas", 90, 35, 15)
    objetivo_arquero = Guerrero("Enemigo", 100, 20, 15)
    danio_arquero = arquero.atacar(objetivo_arquero)
    assert danio_arquero == 40  # (35 - 15) * 2
    print(f"Arquero causó {danio_arquero} de daño. Esperado: 40.")

    objetivo_arquero.defensa = 35
    danio_sin_critico = arquero.atacar(objetivo_arquero)
    assert danio_sin_critico == 0
    print(f"Arquero sin superar defensa causó {danio_sin_critico} de daño. Esperado: 0.")


def probar_vida_y_derrota():
    separador("Casos 8 y 9: vida mínima y personaje derrotado")

    personaje = Guerrero("Arthas", 20, 30, 20)
    danio = personaje.recibir_danio(50)
    assert personaje.vida == 0
    assert danio == 20
    assert not personaje.esta_vivo()
    print(f"Recibió 50 de daño, pero su vida quedó en {personaje.vida}.")
    print(f"Daño efectivo recibido: {danio}.")

    try:
        personaje.atacar(Mago("Gandalf", 80, 40, 10))
        assert False
    except ValueError as error:
        print(f"Ataque de personaje derrotado rechazado: {error}")


def probar_combate_completo():
    separador("Casos 10 y 11: combate completo y ganador")

    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)

    combate = Combate(arthas, gandalf)
    ganador = combate.iniciar()

    assert ganador is gandalf
    assert arthas.vida == 0
    assert gandalf.vida > 0
    print(f"Prueba automática: el ganador es {ganador.nombre}.")


def probar_empate_tecnico():
    separador("Caso 12: empate técnico")

    defensor_1 = Guerrero("Tanque 1", 100, 10, 100)
    defensor_2 = Guerrero("Tanque 2", 100, 10, 100)

    combate = Combate(defensor_1, defensor_2)
    ganador = combate.iniciar()

    assert ganador is None
    print("Prueba automática: se produjo un empate técnico correctamente.")


def ejecutar_casos_de_prueba():
    probar_creacion_personajes()
    probar_validaciones()
    probar_habilidades()
    probar_vida_y_derrota()
    probar_combate_completo()
    probar_empate_tecnico()
    separador("TODOS LOS CASOS DE PRUEBA PASARON")


if __name__ == "__main__":
    ejecutar_casos_de_prueba()
