from pokedex import CATALOGO_POKEMON, mostrar_catalogo_disponible


class Pokemon:
    def __init__(self, nombre, hp_maximo, energia_maxima):
        self._nombre = nombre
        self._hp_maximo = int(hp_maximo)
        self._energia_maxima = int(energia_maxima)
        self._hp_actual = int(hp_maximo)
        self._energia_actual = int(energia_maxima)

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

    def esta_fuera_de_combate(self):
        return self.hp_actual == 0

    def estado(self):
        return f"[{self.nombre}] HP: {self.hp_actual}/{self.hp_maximo} | EP: {self.energia_actual}/{self.energia_maxima}"


def crear_pokemon_base_desde_catalogo(opcion):
    datos = CATALOGO_POKEMON.get(opcion)
    if datos is None:
        return None
    return Pokemon(datos["nombre"], datos["hp_maximo"], datos["energia_maxima"])


def main():
    print("=" * 45)
    print("      SIMULADOR DE BATALLAS POKEMON (POO)")
    print("=" * 45)

    mostrar_catalogo_disponible()

    opcion = input("Elige un Pokemon por numero: ").strip()
    pokemon = crear_pokemon_base_desde_catalogo(opcion)

    if pokemon is None:
        print("Seleccion invalida.")
        return

    print("Pokemon creado correctamente.")
    print(pokemon.estado())


if __name__ == "__main__":
    main()
