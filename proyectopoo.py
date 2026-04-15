import random

from pokedex import CATALOGO_POKEMON, mostrar_catalogo_disponible


class Pokemon:
    COSTO_ATAQUE = 15
    COSTO_DEFENSA = 5
    RECUPERACION_DESCANSO = 20
    DAÑO_BASE = 15

    def __init__(self, nombre, hp_maximo, energia_maxima):
        self._nombre = nombre
        self._hp_maximo = int(hp_maximo)
        self._energia_maxima = int(energia_maxima)
        self._hp_actual = int(hp_maximo)
        self._energia_actual = int(energia_maxima)
        self._defensa_activa = False
        self._turnos_paralizado = 0

    @property
    def nombre(self):
        return self._nombre

    @property
    def hp_actual(self):
        return self._hp_actual

    @hp_actual.setter
    def hp_actual(self, nuevo_hp):
        hp = int(nuevo_hp)
        if hp < 0:
            hp = 0
        if hp > self._hp_maximo:
            hp = self._hp_maximo
        self._hp_actual = hp

    @property
    def hp_maximo(self):
        return self._hp_maximo

    @property
    def energia_actual(self):
        return self._energia_actual

    @energia_actual.setter
    def energia_actual(self, nueva_energia):
        energia = int(nueva_energia)
        if energia < 0:
            energia = 0
        if energia > self._energia_maxima:
            energia = self._energia_maxima
        self._energia_actual = energia

    @property
    def energia_maxima(self):
        return self._energia_maxima

    @property
    def esta_defendiendo(self):
        return self._defensa_activa

    @property
    def esta_paralizado(self):
        return self._turnos_paralizado > 0

    def esta_fuera_de_combate(self):
        return self.hp_actual == 0

    def iniciar_turno(self):
        if self._turnos_paralizado > 0:
            self._turnos_paralizado -= 1
            return False
        return True

    def recibir_danio(self, danio):
        daño_final = int(danio)
        if self._defensa_activa:
            daño_final = daño_final // 2
            self._defensa_activa = False
        self.hp_actual -= daño_final
        return daño_final

    def defender(self):
        if self.energia_actual < self.COSTO_DEFENSA:
            return False, f"{self.nombre} no tiene energia suficiente para defender."
        self.energia_actual -= self.COSTO_DEFENSA
        self._defensa_activa = True
        return True, f"{self.nombre} adopta una postura defensiva."

    def descansar(self):
        energia_antes = self.energia_actual
        self.energia_actual += self.RECUPERACION_DESCANSO
        recuperado = self.energia_actual - energia_antes
        return True, f"{self.nombre} descansa y recupera {recuperado} EP."

    def calcular_multiplicador(self, oponente):
        return 1

    def atacar(self, oponente):
        if self.energia_actual < self.COSTO_ATAQUE:
            return False, f"{self.nombre} no tiene energia suficiente para atacar.", 0

        self.energia_actual -= self.COSTO_ATAQUE
        multiplicador = self.calcular_multiplicador(oponente)
        daño = int(self.DAÑO_BASE * multiplicador)
        daño_aplicado = oponente.recibir_danio(daño)

        if multiplicador > 1:
            texto_efecto = "Es super efectivo"
        else:
            texto_efecto = "Golpe normal"

        mensaje = (
            f"{self.nombre} ataca a {oponente.nombre}. "
            f"{texto_efecto}: {daño_aplicado} de daño."
        )
        return True, mensaje, daño_aplicado

    def estado(self):
        etiquetas = []
        if self._defensa_activa:
            etiquetas.append("DEF")
        if self._turnos_paralizado > 0:
            etiquetas.append("PAR")
        sufijo = f" [{'|'.join(etiquetas)}]" if etiquetas else ""
        return (
            f"[{self.nombre}] HP: {self.hp_actual}/{self.hp_maximo} | "
            f"EP: {self.energia_actual}/{self.energia_maxima}{sufijo}"
        )


class PokemonAgua(Pokemon):
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonFuego):
            return 2
        return 1


class PokemonFuego(Pokemon):
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonPlanta):
            return 2
        return 1


class PokemonPlanta(Pokemon):
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonAgua):
            return 2
        return 1


class PokemonElectrico(Pokemon):
    PROBABILIDAD_PARALISIS = 0.2

    def atacar(self, oponente):
        exito, mensaje, daño = super().atacar(oponente)
        if not exito:
            return exito, mensaje, daño

        if not oponente.esta_fuera_de_combate() and random.random() < self.PROBABILIDAD_PARALISIS:
            oponente._turnos_paralizado = 1
            mensaje += f" {oponente.nombre} queda paralizado y perdera su proximo turno."
        return exito, mensaje, daño


def crear_pokemon_desde_catalogo(opcion):
    datos = CATALOGO_POKEMON.get(opcion)
    if datos is None:
        return None

    tipo = datos["tipo"]
    nombre = datos["nombre"]
    hp_maximo = datos["hp_maximo"]
    energia_maxima = datos["energia_maxima"]

    if tipo == "Fuego":
        return PokemonFuego(nombre, hp_maximo, energia_maxima)
    if tipo == "Agua":
        return PokemonAgua(nombre, hp_maximo, energia_maxima)
    if tipo == "Planta":
        return PokemonPlanta(nombre, hp_maximo, energia_maxima)
    if tipo == "Electrico":
        return PokemonElectrico(nombre, hp_maximo, energia_maxima)
    return Pokemon(nombre, hp_maximo, energia_maxima)


def main():
    print("=" * 45)
    print("      SIMULADOR DE BATALLAS POKEMON (POO)")
    print("=" * 45)

    mostrar_catalogo_disponible()

    opcion = input("Elige un Pokemon por numero: ").strip()
    pokemon = crear_pokemon_desde_catalogo(opcion)

    if pokemon is None:
        print("Seleccion invalida.")
        return

    print("Pokemon creado correctamente.")
    print(pokemon.estado())


if __name__ == "__main__":
    main()
