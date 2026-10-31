# ============================================================
# DOUGHELIA IED — N-Queens Solver (DEMO PÚBLICA BLINDADA)
# Instituto Doughel · UNEG
# DOI Base: 10.5281/zenodo.23826318
# ============================================================
# AVISO EPISTEMOLÓGICO:
# Este script es una DEMOSTRACIÓN de validación estructural.
# NO certifica el grado SAG del Instituto Doughel (requiere clave privada).
# NO debe usarse como solver genérico de N-Queens en producción.
# ============================================================

import hashlib
import hmac
import os
import time

__all__ = ["DougheliaNQueensSolver"]

# ---- Límites duros de la versión pública ----
MAX_N = 12
MAX_SOLUCIONES = 92  # Tope de memoria: se detiene al alcanzar este número

# ---- Clave de firma (solo el Instituto la tiene en producción) ----
_SIGNING_KEY = os.environ.get("DOUGHELIA_SIGNING_KEY", "").encode() or None


class DougheliaNQueensSolver:
    """
    Doughelia IED - Solucionador Estructural para el Problema de las N Damas.

    Versión pública blindada. Límites:
      - N <= 12
      - Máximo 92 soluciones acumuladas en memoria

    El hash de verificación es reproducible (no incluye tiempo).
    Si DOUGHELIA_SIGNING_KEY está definida, se emite además una firma HMAC
    que solo el Instituto Doughel puede regenerar.
    """

    def __init__(self, n):
        if not isinstance(n, int):
            raise TypeError("N debe ser un entero.")
        if n <= 0:
            raise ValueError("El tamaño del tablero debe ser mayor a 0.")
        if n > MAX_N:
            raise ValueError(
                f"Límite de la versión pública: N <= {MAX_N}. "
                f"Para N mayores, contacte al Instituto Doughel."
            )
        self.n = n
        self.soluciones = []
        self._truncado = False
        self.tablero = [-1] * n

    def __es_posicion_valida(self, fila, col):
        """Validación estructural en O(fila). Privado (name-mangling)."""
        for i in range(fila):
            if self.tablero[i] == col:
                return False
            if abs(self.tablero[i] - col) == abs(i - fila):
                return False
        return True

    def __resolver_mrei(self, fila):
        """Núcleo recursivo del MREI. Privado (name-mangling)."""
        if fila == self.n:
            self.soluciones.append(list(self.tablero))
            if len(self.soluciones) >= MAX_SOLUCIONES:
                self._truncado = True
            return

        for col in range(self.n):
            if self._truncado:
                return
            if self.__es_posicion_valida(fila, col):
                self.tablero[fila] = col
                self.__resolver_mrei(fila + 1)

    def _payload_reproducible(self, total, truncado):
        """Payload determinista (sin tiempo) para hash reproducible."""
        return f"v:public|n:{self.n}|soluciones:{total}|truncado:{int(truncado)}"

    def _firmar(self, payload: str):
        """Devuelve (hash_reproducible, firma_hmac_o_None)."""
        hash_hex = hashlib.sha256(payload.encode()).hexdigest()[:16]
        if _SIGNING_KEY:
            firma = hmac.new(_SIGNING_KEY, payload.encode(), hashlib.sha256).hexdigest()[:32]
        else:
            firma = None
        return hash_hex, firma

    def ejecutar_analisis(self):
        """Ejecuta el análisis y emite el reporte auditable."""
        print(f"\n🚀 DOUGHELIA IED — RESOLUCIÓN EXACTA (MREI) PARA {self.n} DAMAS")
        print("=" * 65)

        inicio_tiempo = time.time()
        self.__resolver_mrei(0)
        tiempo_total = time.time() - inicio_tiempo

        total_soluciones = len(self.soluciones)
        print(f"  Tamaño del Tablero (N): {self.n} x {self.n}")
        print(f"  Configuraciones Exactas Encontradas: {total_soluciones}"
              f"{' (tope alcanzado)' if self._truncado else ''}")
        print(f"  Tiempo de Procesamiento: {tiempo_total:.4f} segundos")

        if total_soluciones > 0:
            print(f"\n  Primera Estructura de Alineación: {self.soluciones[0]}")
            print("  Representación Visual:")
            for fila in range(self.n):
                linea = [" . "] * self.n
                linea[self.soluciones[0][fila]] = " 👑 "
                print(f"    {''.join(linea)}")
        else:
            print("\n⚠️ No existen soluciones válidas para este tamaño de tablero.")

        payload = self._payload_reproducible(total_soluciones, self._truncado)
        hash_hex, firma = self._firmar(payload)
        print(f"\n🔐 Hash SHA-256 reproducible: {hash_hex}")
        if firma:
            print(f"🖋️  Firma HMAC del Instituto: {firma}")
        else:
            print("ℹ️  Modo público: sin firma (DOUGHELIA_SIGNING_KEY no definida).")
        print("=" * 65)


if __name__ == "__main__":
    print("--- Panel de Control Doughelia IED — Demo Pública ---")
    try:
        user_n = int(input(f"Introduce el número de Damas (N <= {MAX_N}): "))
        solver = DougheliaNQueensSolver(user_n)
        solver.ejecutar_analisis()
    except ValueError as e:
        print(f"❌ {e}")
    except TypeError as e:
        print(f"❌ {e}")
