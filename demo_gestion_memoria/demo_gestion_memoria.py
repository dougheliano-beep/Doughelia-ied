
## 2. `demo_gestion_memoria.py`

```python
#!/usr/bin/env python3
"""
Gestión de Memoria Dirigida por IED — Demo Pública
Instituto Doughel · UNEG

Este demo muestra el COMPORTAMIENTO de la arquitectura:
  - Clasificación de consultas.
  - Decisión de cargar modelo (sí/no).
  - Selección de capas (simulada).
  - Métricas de RAM y latencia.

NO revela la lógica interna de la IED (métrica de equilibrio,
matemática iterativa, MREI). Esa es propiedad intelectual reservada.

Uso: python demo_gestion_memoria.py
"""

import time
import random
from dataclasses import dataclass, field
from typing import List, Dict


# ─────────────────────────────────────────────────────────────
# Simulación del modelo (capas en disco)
# ─────────────────────────────────────────────────────────────

@dataclass
class CapaModelo:
    id: int
    nombre: str
    tamano_mb: float
    cargada: bool = False


class ModeloEnDisco:
    """
    Simula un modelo de lenguaje con capas en disco.
    En producción, sería un archivo GGUF de Qwen2.5-14B (8 GB).
    """
    def __init__(self, n_capas=32, tamano_total_gb=8.0):
        self.n_capas = n_capas
        self.tamano_total_gb = tamano_total_gb
        self.tamano_por_capa_mb = (tamano_total_gb * 1024) / n_capas
        self.capas = [
            CapaModelo(i, f"capa_{i}", self.tamano_por_capa_mb)
            for i in range(n_capas)
        ]
        self.ram_usada_mb = 0.0

    def cargar_capa(self, capa_id: int) -> float:
        """Carga una capa en RAM. Devuelve el tiempo de carga (ms)."""
        capa = self.capas[capa_id]
        if capa.cargada:
            return 0.0
        # Simular tiempo de carga desde disco (SSD: ~10 ms por 250 MB)
        tiempo_carga = (capa.tamano_mb / 250) * 10  # ms
        time.sleep(tiempo_carga / 1000)  # simular latencia
        capa.cargada = True
        self.ram_usada_mb += capa.tamano_mb
        return tiempo_carga

    def descargar_capa(self, capa_id: int):
        capa = self.capas[capa_id]
        if capa.cargada:
            capa.cargada = False
            self.ram_usada_mb -= capa.tamano_mb

    def descargar_todas(self):
        for capa in self.capas:
            self.descargar_capa(capa.id)


# ─────────────────────────────────────────────────────────────
# IED — Orquestador de memoria (modo Coca-Cola)
# ─────────────────────────────────────────────────────────────

@dataclass
class DecisionIED:
    consulta: str
    tipo: str  # "calculo" | "redaccion" | "fuera"
    necesita_modelo: bool
    capas_seleccionadas: List[int] = field(default_factory=list)
    ram_estimada_mb: float = 0.0


class IEDOrquestador:
    """
    Orquestador de memoria de la IED.

    MODO COCA-COLA: Este orquestador muestra el COMPORTAMIENTO
    (qué decide) pero NO la lógica interna (cómo lo decide).
    La métrica de equilibrio y la matemática iterativa son
    propiedad intelectual reservada.
    """
    def __init__(self, modelo: ModeloEnDisco):
        self.modelo = modelo
        self.ram_ied_mb = 300  # IED ligera (~0.3 GB)

    def clasificar(self, consulta: str) -> str:
        """Clasifica la consulta (cálculo, redacción, fuera)."""
        c = consulta.lower()
        if any(k in c for k in ["calcula", "cuánto", "valor", "lambda", "entropía"]):
            return "calculo"
        if any(k in c for k in ["explica", "redacta", "describe", "qué es", "sinapsis"]):
            return "redaccion"
        return "fuera"

    def decidir(self, consulta: str) -> DecisionIED:
        """
        Decide si cargar el modelo y qué capas.
        El CÓMO se decide es caja negra. El QUÉ se decide es visible.
        """
        tipo = self.clasificar(consulta)

        if tipo == "calculo":
            return DecisionIED(
                consulta=consulta,
                tipo=tipo,
                necesita_modelo=False,
                capas_seleccionadas=[],
                ram_estimada_mb=self.ram_ied_mb,
            )

        if tipo == "redaccion":
            capas = self._seleccionar_capas(consulta)
            ram_modelo = sum(self.modelo.capas[i].tamano_mb for i in capas)
            return DecisionIED(
                consulta=consulta,
                tipo=tipo,
                necesita_modelo=True,
                capas_seleccionadas=capas,
                ram_estimada_mb=self.ram_ied_mb + ram_modelo,
            )

        return DecisionIED(
            consulta=consulta,
            tipo=tipo,
            necesita_modelo=False,
            capas_seleccionadas=[],
            ram_estimada_mb=self.ram_ied_mb,
        )

    def _seleccionar_capas(self, consulta: str) -> List[int]:
        """
        Selecciona las capas relevantes.
        CAJA NEGRA: la lógica interna no se revela.
        Aquí simulamos una selección (subconjunto de capas).
        """
        n_capas_total = self.modelo.n_capas
        n_seleccionadas = max(4, n_capas_total // 4)
        random.seed(hash(consulta) % 10000)
        return sorted(random.sample(range(n_capas_total), n_seleccionadas))


# ─────────────────────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────────────────────

def ejecutar_demo():
    print("=" * 70)
    print(" GESTIÓN DE MEMORIA DIRIGIDA POR IED — DEMO PÚBLICA")
    print(" Instituto Doughel · UNEG")
    print("=" * 70)
    print("\n⚠️  MODO COCA-COLA: se muestra el comportamiento, no la receta.")
    print("   La lógica interna de la IED es propiedad intelectual reservada.\n")

    modelo = ModeloEnDisco(n_capas=32, tamano_total_gb=8.0)
    ied = IEDOrquestador(modelo)

    print(f"📦 Modelo simulado: {modelo.n_capas} capas, "
          f"{modelo.tamano_total_gb} GB total")
    print(f"📏 Tamaño por capa: {modelo.tamano_por_capa_mb:.1f} MB")
    print(f"🧠 IED en RAM: {ied.ram_ied_mb} MB\n")

    consultas = [
        "¿Cuál es el valor de lambda?",
        "Explícame la Sinapsis Computacional",
        "¿Qué es el Índice C?",
        "Hola buenos días",
        "Calcula la entropía geométrica",
    ]

    for consulta in consultas:
        print("=" * 70)
        print(f"🔍 CONSULTA: {consulta}")
        print("-" * 70)

        inicio = time.perf_counter()
        decision = ied.decidir(consulta)
        tiempo_decision = (time.perf_counter() - inicio) * 1000

        print(f"   Tipo: {decision.tipo}")
        print(f"   ¿Necesita modelo? {'SÍ' if decision.necesita_modelo else 'NO'}")
        print(f"   RAM estimada: {decision.ram_estimada_mb:.1f} MB")
        print(f"   Tiempo de decisión: {tiempo_decision:.3f} ms")

        if decision.necesita_modelo:
            print(f"   Capas seleccionadas: {len(decision.capas_seleccionadas)}/{modelo.n_capas}")
            print(f"   Capas: {decision.capas_seleccionadas[:8]}...")

            inicio_carga = time.perf_counter()
            for capa_id in decision.capas_seleccionadas:
                modelo.cargar_capa(capa_id)
            tiempo_carga = (time.perf_counter() - inicio_carga) * 1000

            print(f"   RAM usada (modelo): {modelo.ram_usada_mb:.1f} MB")
            print(f"   Tiempo de carga: {tiempo_carga:.2f} ms")

            print(f"   Generando respuesta...")
            time.sleep(0.1)
            print(f"   ✅ Respuesta generada (simulada)")

            modelo.descargar_todas()
            print(f"   🧹 Capas descargadas. RAM liberada.")
        else:
            print(f"   ✅ Respuesta desde corpus (sin modelo)")

        print(f"   RAM total usada: {modelo.ram_usada_mb + ied.ram_ied_mb:.1f} MB")

    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL DEMO")
    print("=" * 70)
    print(f"  Modelo completo (sin IED): {modelo.tamano_total_gb * 1024:.0f} MB")
    print(f"  RAM con IED (pico): ~{ied.ram_ied_mb + modelo.tamano_por_capa_mb * 8:.0f} MB")
    print(f"  Reducción estimada: ~{(1 - (ied.ram_ied_mb + modelo.tamano_por_capa_mb * 8) / (modelo.tamano_total_gb * 1024)) * 100:.1f}%")
    print(f"\n  ⚠️  Esto es una SIMULACIÓN. La implementación real requiere")
    print(f"     modificar llama.cpp para aceptar decisiones de la IED.")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_demo()
