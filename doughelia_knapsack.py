# ============================================================
# DOUGHELIA IED — Knapsack 0/1 (DEMO PÚBLICA BLINDADA)
# Instituto Doughel · UNEG
# ============================================================
# AVISO: Demo de poda estructural. NO certifica SAG sin firma.
# ============================================================

import hashlib
import hmac
import os

__all__ = ["DougheliaKnapsackSolver"]

MAX_OBJETOS = 20
MAX_CAPACIDAD = 10**6
_SIGNING_KEY = os.environ.get("DOUGHELIA_SIGNING_KEY", "").encode() or None


class DougheliaKnapsackSolver:
    """
    Doughelia IED — Mochila 0/1 por backtracking con poda.
    Límites: N <= 20 objetos, capacidad <= 10^6.
    Resultado sellado tras ejecutar_analisis().
    """

    def __init__(self, pesos, valores, capacidad):
        if not isinstance(pesos, (list, tuple)) or not isinstance(valores, (list, tuple)):
            raise TypeError("pesos y valores deben ser listas.")
        n = len(pesos)
        if n == 0 or n > MAX_OBJETOS:
            raise ValueError(f"Se requieren 1..{MAX_OBJETOS} objetos.")
        if len(valores) != n:
            raise ValueError("pesos y valores deben tener igual longitud.")
        for p in pesos:
            if not isinstance(p, (int, float)) or p <= 0:
                raise ValueError("Cada peso debe ser numérico y > 0.")
        for v in valores:
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError("Cada valor debe ser numérico y >= 0.")
        if not isinstance(capacidad, (int, float)) or capacidad <= 0:
            raise ValueError("La capacidad debe ser numérica y > 0.")
        if capacidad > MAX_CAPACIDAD:
            raise ValueError(f"Capacidad máxima: {MAX_CAPACIDAD}.")

        self.n = n
        self.pesos = tuple(pesos)
        self.valores = tuple(valores)
        self.capacidad = capacidad
        self._mejor_valor = None
        self._mejor_seleccion = None
        self._sellado = False

    @property
    def mejor_valor(self):
        return self._mejor_valor

    @property
    def mejor_seleccion(self):
        return self._mejor_seleccion

    def __poda_bound(self, idx, peso_restante, valor_actual):
        """Cota superior optimista: asume que se puede fraccionar el resto."""
        bound = valor_actual
        w = peso_restante
        for i in range(idx, self.n):
            if self.pesos[i] <= w:
                w -= self.pesos[i]
                bound += self.valores[i]
            else:
                bound += self.valores[i] * (w / self.pesos[i])
                break
        return bound

    def __resolver(self, idx, peso_restante, valor_actual, seleccion):
        if idx == self.n:
            if valor_actual > (self._mejor_valor or 0):
                self._mejor_valor = valor_actual
                self._mejor_seleccion = tuple(seleccion)
            return
        if self.__poda_bound(idx, peso_restante, valor_actual) <= (self._mejor_valor or 0):
            return
        # Tomar
        if self.pesos[idx] <= peso_restante:
            seleccion.append(idx)
            self.__resolver(idx + 1, peso_restante - self.pesos[idx],
                           valor_actual + self.valores[idx], seleccion)
            seleccion.pop()
        # No tomar
        self.__resolver(idx + 1, peso_restante, valor_actual, seleccion)

    def _payload(self):
        sel = ",".join(map(str, self._mejor_seleccion)) if self._mejor_seleccion else "none"
        return (f"v:public|n:{self.n}|cap:{self.capacidad}"
                f"|pesos:{','.join(map(str, self.pesos))}"
                f"|valores:{','.join(map(str, self.valores))}"
                f"|sel:{sel}|valor:{self._mejor_valor}")

    def _firmar(self, p):
        h = hashlib.sha256(p.encode()).hexdigest()[:16]
        f = hmac.new(_SIGNING_KEY, p.encode(), hashlib.sha256).hexdigest()[:32] if _SIGNING_KEY else None
        return h, f

    def ejecutar_analisis(self):
        if self._sellado:
            raise RuntimeError("Solver ya ejecutado y sellado.")
        print("\n🚀 DOUGHELIA IED — MOCHILA 0/1 (PODA ESTRUCTURAL)")
        print("=" * 65)
        print(f"  Objetos: {self.n} | Capacidad: {self.capacidad}")
        self.__resolver(0, self.capacidad, 0, [])
        self._sellado = True
        print(f"  Selección óptima (índices): {self._mejor_seleccion}")
        print(f"  Valor máximo: {self._mejor_valor}")
        h, f = self._firmar(self._payload())
        print(f"\n🔐 Hash: {h}")
        print(f"🖋️  Firma: {'SI' if f else 'NO (modo público)'}")
        print("=" * 65)
