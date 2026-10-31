# ============================================================
# DOUGHELIA IED — Análisis Estructural abc (DEMO PÚBLICA BLINDADA)
# Instituto Doughel · UNEG
# DOI Tripla abc: 10.5281/zenodo.23838919
# ============================================================
# AVISO EPISTEMOLÓGICO:
# Este script realiza VALIDACIÓN ESTRUCTURAL de triplas abc.
# NO prueba ni refuta la conjetura abc.
# NO certifica el grado SAG del Instituto Doughel.
# ============================================================

import hashlib
import hmac
import math
import os

__all__ = ["DougheliaABCSolver"]

MAX_VALOR = 10 ** 9
_SIGNING_KEY = os.environ.get("DOUGHELIA_SIGNING_KEY", "").encode() or None


class DougheliaABCSolver:
    """
    Doughelia IED — Analizador estructural del Teorema abc (versión pública).

    Límites:
      - a, b enteros positivos <= 10^9
      - c = a + b
      - gcd(a,b) == 1 (condición de coprimilidad)

    Calcula q = log(c) / log(rad(abc)) y clasifica la tripla como extrema
    si q > 1.0. Esto es un criterio estructural, NO una prueba matemática.
    """

    def __init__(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("a y b deben ser enteros.")
        if a <= 0 or b <= 0:
            raise ValueError("a y b deben ser enteros positivos.")
        if a > MAX_VALOR or b > MAX_VALOR:
            raise ValueError(f"Límite de la versión pública: a, b <= {MAX_VALOR}.")
        self.a = a
        self.b = b
        self.c = a + b

    def __gcd(self, x, y):
        while y:
            x, y = y, x % y
        return x

    def __radical(self, n):
        """Radical de n (producto de primos distintos). Privado."""
        if n <= 0:
            return 0
        rad = 1
        p = 2
        while p * p <= n:
            if n % p == 0:
                rad *= p
                while n % p == 0:
                    n //= p
            p += 1
        if n > 1:
            rad *= n
        return rad

    def _payload_reproducible(self, rad_abc, q):
        return f"v:public|a:{self.a}|b:{self.b}|c:{self.c}|rad:{rad_abc}|q:{q:.6f}"

    def _firmar(self, payload: str):
        hash_hex = hashlib.sha256(payload.encode()).hexdigest()[:16]
        if _SIGNING_KEY:
            firma = hmac.new(_SIGNING_KEY, payload.encode(), hashlib.sha256).hexdigest()[:32]
        else:
            firma = None
        return hash_hex, firma

    def ejecutar_analisis(self):
        print("\n🚀 DOUGHELIA IED — ANÁLISIS ESTRUCTURAL (abc)")
        print("=" * 65)

        gcd_ab = self.__gcd(self.a, self.b)
        gcd_bc = self.__gcd(self.b, self.c)
        gcd_ac = self.__gcd(self.a, self.c)

        if gcd_ab != 1 or gcd_bc != 1 or gcd_ac != 1:
            print(f"❌ La tripla ({self.a}, {self.b}, {self.c}) NO es coprima.")
            print(f"   gcd(a,b)={gcd_ab}, gcd(b,c)={gcd_bc}, gcd(a,c)={gcd_ac}")
            print("=" * 65)
            return False

        print(f"  Tripla coprima: a={self.a}, b={self.b}, c={self.c}")

        rad_abc = self.__radical(self.a * self.b * self.c)
        print(f"  Radical rad(abc): {rad_abc}")

        # Fix del bug: rad_abc == 1 (caso a·b·c primo) → q indefinido
        if rad_abc <= 1:
            print("  ⚠️ rad(abc) <= 1: la calidad q no está definida en este caso.")
            print("=" * 65)
            return False

        proporcion = self.c / rad_abc
        print(f"  Proporción c / rad(abc): {proporcion:.4f}")

        calidad_q = math.log(self.c) / math.log(rad_abc)
        print(f"  Calidad matemática (q): {calidad_q:.4f}")

        if calidad_q > 1.0:
            print("\n🏆 RESULTADO: Tripla estructuralmente extrema (q > 1).")
            print("   NOTA: criterio estructural, no prueba de la conjetura abc.")
        else:
            print("\n⚠️ RESULTADO: Tripla estándar (q <= 1).")

        payload = self._payload_reproducible(rad_abc, calidad_q)
        hash_hex, firma = self._firmar(payload)
        print(f"\n🔐 Hash SHA-256 reproducible: {hash_hex}")
        if firma:
            print(f"🖋️  Firma HMAC del Instituto: {firma}")
        else:
            print("ℹ️  Modo público: sin firma (DOUGHELIA_SIGNING_KEY no definida).")
        print("=" * 65)
        return True


if __name__ == "__main__":
    print("--- Panel de Control Doughelia IED — Demo Pública (abc) ---")
    try:
        user_a = int(input("Introduce el valor de a: "))
        user_b = int(input("Introduce el valor de b: "))
        solver = DougheliaABCSolver(user_a, user_b)
        solver.ejecutar_analisis()
    except (ValueError, TypeError) as e:
        print(f"❌ {e}")
