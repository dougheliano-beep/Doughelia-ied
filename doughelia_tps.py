# ============================================================
# DOUGHELIA IED — TSP Solver (DEMO PÚBLICA BLINDADA)
# Instituto Doughel · UNEG
# DOI TSP: 10.5281/zenodo.23840024
# ============================================================
# AVISO EPISTEMOLÓGICO:
# Fuerza bruta exacta para N <= 5 ciudades.
# NO es un solver de TSP para producción.
# NO certifica el grado SAG del Instituto Doughel.
# ============================================================

import hashlib
import hmac
import os
import time

__all__ = ["DougheliaTSPSolver"]

MAX_CIUDADES = 5
_SIGNING_KEY = os.environ.get("DOUGHELIA_SIGNING_KEY", "").encode() or None


class DougheliaTSPSolver:
    """
    Doughelia IED — Solver exacto de TSP por fuerza bruta (versión pública).

    Límites:
      - N <= 5 ciudades
      - Matriz cuadrada NxN, no negativa, diagonal cero
      - Resultado sellado (inmutable) tras ejecutar_analisis()
    """

    def __init__(self, matriz):
        if not isinstance(matriz, (list, tuple)):
            raise TypeError("La matriz debe ser una lista de listas.")
        n = len(matriz)
        if n == 0:
            raise ValueError("La matriz no puede estar vacía.")
        if n > MAX_CIUDADES:
            raise ValueError(
                f"Límite de la versión pública: N <= {MAX_CIUDADES}. "
                f"Para más ciudades, contacte al Instituto Doughel."
            )
        for fila in matriz:
            if not isinstance(fila, (list, tuple)) or len(fila) != n:
                raise ValueError("La matriz debe ser cuadrada NxN.")
        for i in range(n):
            for j in range(n):
                v = matriz[i][j]
                if not isinstance(v, (int, float)):
                    raise TypeError(f"matriz[{i}][{j}] no es numérico.")
                if v < 0:
                    raise ValueError(f"matriz[{i}][{j}] es negativo.")
            if matriz[i][i] != 0:
                raise ValueError(f"matriz[{i}][{i}] debe ser 0.")

        self.n = n
        self.matriz = tuple(tuple(f) for f in matriz)  # inmutable
        self._mejor_ruta = None
        self._mejor_costo = None
        self._sellado = False
        self._truncado = False  # reservado para futura poda

    @property
    def mejor_ruta(self):
        return self._mejor_ruta

    @property
    def mejor_costo(self):
        return self._mejor_costo

    def __costo_ruta(self, ruta):
        total = 0
        for i in range(self.n - 1):
            total += self.matriz[ruta[i]][ruta[i + 1]]
        total += self.matriz[ruta[-1]][ruta[0]]  # ciclo cerrado
        return total

    def __permutar(self, elementos):
        """Generador de permutaciones. Privado (name-mangling)."""
        if len(elementos) <= 1:
            yield tuple(elementos)
            return
        for i in range(len(elementos)):
            resto = elementos[:i] + elementos[i + 1:]
            for p in self.__permutar(resto):
                yield (elementos[i],) + p

    def _payload_reproducible(self):
        ruta_str = ",".join(str(x) for x in self._mejor_ruta) if self._mejor_ruta else "none"
        costo_str = f"{self._mejor_costo:.6f}" if self._mejor_costo is not None else "none"
        matriz_str = ";".join(",".join(f"{v:g}" for v in fila) for fila in self.matriz)
        return f"v:public|n:{self.n}|m:{matriz_str}|ruta:{ruta_str}|costo:{costo_str}"

    def _firmar(self, payload: str):
        hash_hex = hashlib.sha256(payload.encode()).hexdigest()[:16]
        if _SIGNING_KEY:
            firma = hmac.new(_SIGNING_KEY, payload.encode(), hashlib.sha256).hexdigest()[:32]
        else:
            firma = None
        return hash_hex, firma

    def ejecutar_analisis(self):
        if self._sellado:
            raise RuntimeError("Este solver ya fue ejecutado y sellado. Cree una nueva instancia.")

        print("\n🚀 DOUGHELIA IED — TSP EXACTO (FUERZA BRUTA ACOTADA)")
        print("=" * 65)
        print(f"  Ciudades (N): {self.n}")

        inicio = time.time()
        # Fijamos la ciudad 0 como origen para romper simetría cíclica
        mejor_ruta = None
        mejor_costo = None
        for perm in self.__permutar(tuple(range(1, self.n))):
            ruta = (0,) + perm
            costo = self.__costo_ruta(ruta)
            if mejor_costo is None or costo < mejor_costo:
                mejor_costo = costo
                mejor_ruta = ruta
        tiempo_total = time.time() - inicio

        self._mejor_ruta = mejor_ruta
        self._mejor_costo = mejor_costo
        self._sellado = True

        print(f"  Mejor ruta: {' -> '.join(map(str, mejor_ruta))} -> {mejor_ruta[0]}")
        print(f"  Costo óptimo: {mejor_costo}")
        print(f"  Tiempo: {tiempo_total:.4f} segundos")

        payload = self._payload_reproducible()
        hash_hex, firma = self._firmar(payload)
        print(f"\n🔐 Hash SHA-256 reproducible: {hash_hex}")
        if firma:
            print(f"🖋️  Firma HMAC del Instituto: {firma}")
        else:
            print("ℹ️  Modo público: sin firma (DOUGHELIA_SIGNING_KEY no definida).")
        print("=" * 65)


if __name__ == "__main__":
    print("--- Panel de Control Doughelia IED — Demo Pública (TSP) ---")
    try:
        n = int(input(f"Número de ciudades (N <= {MAX_CIUDADES}): "))
        if n <= 0 or n > MAX_CIUDADES:
            raise ValueError(f"N fuera de rango (1..{MAX_CIUDADES}).")
        print("Introduce la matriz de distancias (filas separadas por ';', valores por ',').")
        print("Ejemplo: 0,2,9,10;1,0,6,4;15,7,0,8;6,3,12,0")
        raw = input("Matriz: ").strip()
        matriz = []
        for fila in raw.split(";"):
            matriz.append([float(x) if "." in x else int(x) for x in fila.split(",")])
        solver = DougheliaTSPSolver(matriz)
        solver.ejecutar_analisis()
    except (ValueError, TypeError) as e:
        print(f"❌ {e}")
