import random

from pokedex import CATALOGO_POKEMON, mostrar_catalogo_disponible


class Pokemon:
    COSTO_ATAQUE = 15
    COSTO_DEFENSA = 5
    RECUPERACION_DESCANSO = 20
    DAÑO_BASE = 15
    STATS_BASE = {"attack": 10, "defense": 8, "speed": 5}

    def __init__(self, nombre, hp_maximo, energia_maxima, tipo="Normal", stats=None):
        self._nombre = nombre
        self._tipo = tipo
        self._hp_maximo = int(hp_maximo)
        self._energia_maxima = int(energia_maxima)
        self._hp_actual = int(hp_maximo)
        self._energia_actual = int(energia_maxima)
        self._defensa_activa = False
        self._turnos_paralizado = 0
        self._stats = stats or self.STATS_BASE.copy()

    @property
    def nombre(self):
        return self._nombre

    @property
    def tipo(self):
        return self._tipo

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
    def attack(self):
        return self._stats.get("attack", 10)

    @property
    def defense(self):
        return self._stats.get("defense", 8)

    @property
    def speed(self):
        return self._stats.get("speed", 5)

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
        reduce_defensa = int(self.defense / 2)
        daño_final = max(1, daño_final - reduce_defensa)
        if self._defensa_activa:
            daño_final = int(daño_final * 0.5)
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
        daño = int((self.DAÑO_BASE + self.attack) * multiplicador)
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
        stats_texto = f" | ATK: {self.attack} | DEF: {self.defense} | SPD: {self.speed}"
        return (
            f"[{self.nombre}] HP: {self.hp_actual}/{self.hp_maximo} | "
            f"EP: {self.energia_actual}/{self.energia_maxima}{sufijo}{stats_texto}"
        )


class PokemonAgua(Pokemon):
    STATS_BASE = {"attack": 12, "defense": 11, "speed": 6}
    
    def __init__(self, nombre, hp_maximo, energia_maxima, tipo="Agua"):
        super().__init__(nombre, hp_maximo, energia_maxima, tipo, self.STATS_BASE.copy())
    
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonFuego):
            return 2
        return 1


class PokemonFuego(Pokemon):
    STATS_BASE = {"attack": 14, "defense": 9, "speed": 10}
    
    def __init__(self, nombre, hp_maximo, energia_maxima, tipo="Fuego"):
        super().__init__(nombre, hp_maximo, energia_maxima, tipo, self.STATS_BASE.copy())
    
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonPlanta):
            return 2
        return 1


class PokemonPlanta(Pokemon):
    STATS_BASE = {"attack": 11, "defense": 12, "speed": 7}
    
    def __init__(self, nombre, hp_maximo, energia_maxima, tipo="Planta"):
        super().__init__(nombre, hp_maximo, energia_maxima, tipo, self.STATS_BASE.copy())
    
    def calcular_multiplicador(self, oponente):
        if isinstance(oponente, PokemonAgua):
            return 2
        return 1


class PokemonElectrico(Pokemon):
    STATS_BASE = {"attack": 10, "defense": 9, "speed": 14}
    PROBABILIDAD_PARALISIS = 0.2

    def __init__(self, nombre, hp_maximo, energia_maxima, tipo="Electrico"):
        super().__init__(nombre, hp_maximo, energia_maxima, tipo, self.STATS_BASE.copy())

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
        return PokemonFuego(nombre, hp_maximo, energia_maxima, tipo)
    if tipo == "Agua":
        return PokemonAgua(nombre, hp_maximo, energia_maxima, tipo)
    if tipo == "Planta":
        return PokemonPlanta(nombre, hp_maximo, energia_maxima, tipo)
    if tipo == "Electrico":
        return PokemonElectrico(nombre, hp_maximo, energia_maxima, tipo)
    return Pokemon(nombre, hp_maximo, energia_maxima, tipo)


def solicitar_opcion_valida(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print("Entrada invalida. Intenta de nuevo.")


def determinar_primer_atacante(pokemon_1, pokemon_2):
    """Retorna True si pokemon_1 ataca primero, False si pokemon_2."""
    if pokemon_1.speed != pokemon_2.speed:
        return pokemon_1.speed > pokemon_2.speed
    return random.choice([True, False])


def seleccionar_pokemon_jugador(etiqueta_jugador):
    print(f"\n{etiqueta_jugador}, elige tu Pokemon:")
    opcion = solicitar_opcion_valida(
        "Numero de Pokemon: ",
        CATALOGO_POKEMON.keys(),
    )
    pokemon = crear_pokemon_desde_catalogo(opcion)
    print(f"{etiqueta_jugador} selecciono a {pokemon.nombre} ({pokemon.tipo}).")
    return pokemon


def seleccionar_pokemon_cpu():
    opcion = random.choice(list(CATALOGO_POKEMON.keys()))
    pokemon = crear_pokemon_desde_catalogo(opcion)
    print(f"La computadora selecciono a {pokemon.nombre} ({pokemon.tipo}).")
    return pokemon


def mostrar_menu_acciones(jugador, pokemon):
    print(f"\nTURNO DE {pokemon.nombre.upper()} ({jugador})")
    print(pokemon.estado())
    print("1. Atacar (Costo: 15 EP)")
    print("2. Defender (Costo: 5 EP)")
    print("3. Descansar (Recupera: 20 EP)")


def elegir_accion_jugador(jugador, pokemon):
    mostrar_menu_acciones(jugador, pokemon)
    return solicitar_opcion_valida("Opcion: ", {"1", "2", "3"})


def elegir_accion_computadora(pokemon):
    opciones = []
    if pokemon.energia_actual >= Pokemon.COSTO_ATAQUE:
        opciones.extend(["1", "1", "1"])
    if pokemon.energia_actual >= Pokemon.COSTO_DEFENSA:
        opciones.extend(["2", "2"])
    opciones.append("3")
    return random.choice(opciones)


def ejecutar_accion(pokemon_activo, pokemon_objetivo, accion):
    if accion == "1":
        _, mensaje, _ = pokemon_activo.atacar(pokemon_objetivo)
        return mensaje
    if accion == "2":
        _, mensaje = pokemon_activo.defender()
        return mensaje
    _, mensaje = pokemon_activo.descansar()
    return mensaje


def jugar_turno(nombre_jugador, pokemon_activo, pokemon_objetivo, es_cpu=False):
    if not pokemon_activo.iniciar_turno():
        print(f"{pokemon_activo.nombre} esta paralizado y pierde su turno.")
        return

    if es_cpu:
        accion = elegir_accion_computadora(pokemon_activo)
        nombre_accion = {"1": "Atacar", "2": "Defender", "3": "Descansar"}[accion]
        print(f"\nLa computadora elige: {nombre_accion}")
    else:
        accion = elegir_accion_jugador(nombre_jugador, pokemon_activo)

    resultado = ejecutar_accion(pokemon_activo, pokemon_objetivo, accion)
    print(resultado)


def mostrar_estado_batalla(pokemon_1, pokemon_2):
    print("\nESTADO ACTUAL")
    print(pokemon_1.estado())
    print(pokemon_2.estado())


def ejecutar_batalla(nombre_1, pokemon_1, nombre_2, pokemon_2, jugador_2_es_cpu=False):
    print("\nCOMIENZA LA BATALLA")
    print(f"{pokemon_1.nombre} ({pokemon_1.tipo}) vs {pokemon_2.nombre} ({pokemon_2.tipo})")
    print(f"Velocidades: {pokemon_1.nombre} (SPD: {pokemon_1.speed}) vs {pokemon_2.nombre} (SPD: {pokemon_2.speed})")
    
    ataca_primero_1 = determinar_primer_atacante(pokemon_1, pokemon_2)
    if ataca_primero_1:
        print(f"{pokemon_1.nombre} ataca primero por tener mayor velocidad.")
    else:
        print(f"{pokemon_2.nombre} ataca primero por tener mayor velocidad.")

    turno_jugador_1 = ataca_primero_1
    while not pokemon_1.esta_fuera_de_combate() and not pokemon_2.esta_fuera_de_combate():
        if turno_jugador_1:
            jugar_turno(nombre_1, pokemon_1, pokemon_2)
        else:
            jugar_turno(nombre_2, pokemon_2, pokemon_1, es_cpu=jugador_2_es_cpu)

        mostrar_estado_batalla(pokemon_1, pokemon_2)
        turno_jugador_1 = not turno_jugador_1

    print("\nFIN DEL COMBATE")
    if pokemon_1.esta_fuera_de_combate() and pokemon_2.esta_fuera_de_combate():
        print("Empate: ambos Pokemon cayeron al mismo tiempo.")
    elif pokemon_2.esta_fuera_de_combate():
        print(f"Gana {nombre_1} con {pokemon_1.nombre}.")
    else:
        print(f"Gana {nombre_2} con {pokemon_2.nombre}.")


def main():
    print("=" * 45)
    print("      SIMULADOR DE BATALLAS POKEMON (POO)")
    print("=" * 45)

    print("Selecciona el modo de juego:")
    print("1. Jugador vs Jugador")
    print("2. Jugador vs Computadora")
    modo = solicitar_opcion_valida("Opcion: ", {"1", "2"})

    mostrar_catalogo_disponible()

    pokemon_jugador_1 = seleccionar_pokemon_jugador("Jugador 1")

    if modo == "1":
        pokemon_jugador_2 = seleccionar_pokemon_jugador("Jugador 2")
        ejecutar_batalla(
            "Jugador 1",
            pokemon_jugador_1,
            "Jugador 2",
            pokemon_jugador_2,
            jugador_2_es_cpu=False,
        )
        return

    print("\nComputadora seleccionando combatiente...")
    pokemon_computadora = seleccionar_pokemon_cpu()
    ejecutar_batalla(
        "Jugador",
        pokemon_jugador_1,
        "Computadora",
        pokemon_computadora,
        jugador_2_es_cpu=True,
    )


if __name__ == "__main__":
    main()
