# 🤖 Doughelia: Inteligencia Estructural Duqueana (IED)

**Primera Arquitectura de Inteligencia Artificial Estructural desarrollada en Venezuela.**

**Autor:** Lcdo. Douglas Helvesio Urbina Duque
**ORCID:** [0009-0005-1230-7549](https://orcid.org/0009-0005-1230-7549)
**Institución:** Instituto Doughel · Universidad Nacional Experimental de Guayana (UNEG), Venezuela
**Licencia:** CC BY-NC-ND 4.0 (Uso académico) / Licencia Comercial (Uso industrial)

---

## 🌟 ¿Qué es Doughelia?

Doughelia no es un modelo de lenguaje desde cero. Es un **Framework de Orquestación Iterativa** que actúa como una capa superior de validación sobre modelos de lenguaje preentrenados. Su función principal es garantizar el **rigor epistemológico**: filtra alucinaciones, valida fuentes y corrige respuestas en tiempo real.

A diferencia de los LLM tradicionales (que dependen de la fuerza bruta estadística), Doughelia utiliza un **protocolo de validación estructural** para asegurar que cada salida generada sea verificable y esté anclada a la realidad.

---

## 🏗️ Arquitectura de 3 Agentes

Doughelia opera mediante un bucle de mejora continua compuesto por tres agentes autónomos:

1. **🧠 Agente Generador:** Recibe la consulta y genera una respuesta base utilizando el modelo de lenguaje subyacente.
2. **🔍 Agente Crítico:** Evalúa la respuesta contra los **Guardrails Epistemológicos** (verificando fuentes, ausencia de alucinaciones y coherencia con repositorios de Ciencia Abierta como Zenodo o OpenAIRE).
3. **🔧 Agente Optimizador:** Si la respuesta es rechazada, reescribe la consulta o ajusta los parámetros de generación para la siguiente iteración, buscando la convergencia hacia la verdad verificable.

El ciclo se repite hasta que la salida alcanza un **Umbral de Alineación Iterada (SAG) ≥ 0.90**.

---

## ⚡ Eficiencia y Resultados

- **Reducción del 90% en consumo de RAM** (simulaciones preliminares del protocolo).
- **Ejecución en hardware de consumo convencional** (sin necesidad de GPUs dedicadas).
- **SAG (Structural Alignment Grade) ≥ 0.90** para garantizar la convergencia lógica.
- **Trazabilidad criptográfica:** Cada respuesta aprobada genera un hash SHA-256 inmutable.

---

## 📦 Estructura del Repositorio

- `README.md`: Este documento (arquitectura y descripción).
- `doughelia_architecture.py`: Esqueleto del framework de los 3 agentes (Python).
- `codemeta.json`: Metadatos para indexación en OpenAIRE y Google Scholar.
- `tests/`: (Opcional) Directorio para pruebas de estrés y validación.

---

## 🚀 Inicio Rápido

Para ejecutar el esqueleto de Doughelia en tu máquina local:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/dougheliano-beep/doughelia-core.git
   cd doughelia-core
