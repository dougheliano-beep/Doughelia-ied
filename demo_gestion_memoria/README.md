# Gestión de Memoria Dirigida por IED — Demo Pública

**Paper:** [DOI 10.5281/zenodo.24447458](https://doi.org/10.5281/zenodo.24447458)

**Autor:** Prof. Douglas Helvesio Urbina Duque (ORCID [0009-0005-1230-7549](https://orcid.org/0009-0005-1230-7549))

**Institución:** Instituto Doughel · UNEG, Venezuela

---

## ¿Qué es esto?

Demo pública de la arquitectura de **Gestión de Memoria Dirigida por IED** para modelos de lenguaje en hardware de recursos limitados.

**El demo muestra:**
- Clasificación de consultas (cálculo, redacción, fuera).
- Decisión de cargar o no el modelo.
- Selección de capas (simulada).
- Métricas de RAM y latencia.

**El demo NO muestra:**
- Cómo la IED decide qué capas cargar (la métrica de equilibrio interna).
- La implementación real del streaming.
- El núcleo del MREI.

**Eso es propiedad intelectual reservada del Instituto Doughel.**

---

## ¿Cómo funciona?

1. **La IED recibe la consulta.**
2. **La clasifica:** ¿es cálculo (no necesita modelo), redacción (sí lo necesita), o fuera (no necesita nada)?
3. **Si es redacción:** selecciona las capas relevantes del modelo (simulado: 8 de 32).
4. **Carga esas capas** en RAM (simulado: 2 GB de 8 GB).
5. **Genera la respuesta** usando las capas cargadas.
6. **Descarga las capas** para liberar RAM.

**Resultado:** La RAM activa se reduce de 8 GB a ~2.3 GB. Eso es una reducción del 71%.

---

## Cómo ejecutarlo

```bash
python demo_gestion_memoria.py
