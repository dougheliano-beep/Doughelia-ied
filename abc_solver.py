import hashlib
import math

class DougheliaABCSolver:
    """
    Doughelia IED - Interfaz de Caja Negra para el Teorema abc.
    Propiedad Intelectual del Instituto Doughel.
    Demostración de capacidad sobre un caso extremo.
    """
    
    def __init__(self):
        # Caso de estudio predefinido (Tripla extrema conocida)
        self.a = 1
        self.b = 4374
        self.c = 4375
        
    def _radical(self, n):
        """Calcula el radical de n (producto de primos distintos)."""
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

    def ejecutar_analisis(self):
        """Ejecuta la validación estructural del caso."""
        print("🚀 DOUGHELIA IED - ANÁLISIS ESTRUCTURAL DEL TEOREMA abc")
        print("=" * 60)
        print("Caso de Estudio: Tripla coprima extrema")
        print("=" * 60)

        # 1. Verificar que a + b = c
        if self.a + self.b != self.c:
            print("❌ Error: La tripla no cumple a + b = c.")
            return

        print(f"  Tripla analizada: a = {self.a}, b = {self.b}, c = {self.c}")
        
        # 2. Calcular el radical
        rad_abc = self._radical(self.a * self.b * self.c)
        print(f"  Radical rad(abc): {rad_abc}")
        
        # 3. Calcular la proporción
        proporcion = self.c / rad_abc
        print(f"  Proporción c / rad(abc): {proporcion:.4f}")
        
        # 4. Validación de la calidad de la tripla (SAG)
        # Si la proporción es > 1, la tripla es "extrema" (calidad alta).
        sag = 1.0 if proporcion > 1.0 else proporcion
        
        print(f"  SAG (Structural Alignment): {sag:.4f}")
        
        if sag == 1.0:
            print("\n🏆 RESULTADO: Tripla extrema identificada con éxito.")
        else:
            print("\n⚠️ RESULTADO: Tripla estándar, no extrema.")

        # 5. Hash de integridad
        payload = f"a:{self.a}|b:{self.b}|c:{self.c}|rad:{rad_abc}|prop:{proporcion:.4f}"
        hash_final = hashlib.sha256(payload.encode()).hexdigest()[:16]
        print(f"\n🔐 Hash SHA-256 de la validación: {hash_final}")
        print("=" * 60)

if __name__ == "__main__":
    solver = DougheliaABCSolver()
    solver.ejecutar_analisis()
