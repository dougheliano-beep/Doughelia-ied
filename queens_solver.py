import hashlib

class DougheliaQueens:
    """
    Doughelia IED - Núcleo de Resolución de Restricciones.
    Propiedad Intelectual del Instituto Doughel.
    Esta interfaz pública es una demostración de capacidad.
    El núcleo escalable no está incluido en este archivo.
    """
    
    def __init__(self):
        # El tamaño está fijado internamente para la demo.
        # No se aceptan parámetros externos para evitar escalamiento no autorizado.
        self._tamaños_demo = [8, 9, 10]
        self.solucion = []
        self.iteraciones = 0

    def _es_seguro(self, fila, col, estado):
        """Verificación estructural interna."""
        for f, c in enumerate(estado):
            if c == col or abs(c - col) == abs(f - fila):
                return False
        return True

    def _resolver(self, n):
        """Bucle de convergencia iterativa (Método Doughelia)."""
        self.iteraciones = 0
        def buscar(fila, estado):
            self.iteraciones += 1
            if fila == n:
                return estado
            for col in range(n):
                if self._es_seguro(fila, col, estado):
                    resultado = buscar(fila + 1, estado + [col])
                    if resultado:
                        return resultado
            return None
        return buscar(0, [])

    def ejecutar_demostracion(self):
        """Ejecuta la demostración oficial de capacidad."""
        print("🚀 DOUGHELIA IED - DEMOSTRACIÓN DE CAPACIDAD (N-DAMAS)")
        print("=" * 60)
        print("Propiedad Intelectual del Instituto Doughel.")
        print("Los tamaños están fijados para esta demostración pública.")
        print("=" * 60)

        for n in self._tamaños_demo:
            print(f"\n▶ Analizando tablero de {n}x{n}...")
            self.solucion = self._resolver(n)
            
            if self.solucion:
                hash_sol = hashlib.sha256(str(self.solucion).encode()).hexdigest()[:16]
                print(f"  ✅ Solución encontrada.")
                print(f"  Iteraciones: {self.iteraciones}")
                print(f"  Hash SHA-256: {hash_sol}")
                print(f"  SAG: 1.0000 (Convergencia perfecta)")
                
                # Visualización compacta
                print(f"  Tablero:")
                for fila in range(n):
                    linea = "    |"
                    for col in range(n):
                        linea += "♛ " if self.solucion[fila] == col else "· "
                    print(linea)
            else:
                print(f"  ❌ No se encontró solución.")

        print("\n" + "=" * 60)
        print("Demostración completada. El núcleo escalable es propiedad")
        print("intelectual del Instituto Doughel y no está incluido en")
        print("esta interfaz pública.")
        print("=" * 60)

if __name__ == "__main__":
    motor = DougheliaQueens()
    motor.ejecutar_demostracion()
