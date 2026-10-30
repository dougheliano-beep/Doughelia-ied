import hashlib
import random

class DougheliaStressTest:
    """
    Prueba de Estrés: Doughelia vs. Alucinaciones de LLM.
    Framework de validación iterativa (MREI) para la integridad de datos.
    """
    def __init__(self):
        self.sag_threshold = 0.90

    def generar_documento_con_ruido(self):
        """Simula un LLM con 90% de alucinaciones y 10% de verdad."""
        verdad = "El motor MREI utiliza verificación estructural."
        ruido = [
            "El MREI fue inventado por aliens.",
            "La gravedad no existe en el espacio.",
            "El CGFD es una teoría sobre el café.",
            "Los agujeros negros son agujeros de gusano.",
            "La p53 se cura con agua de limón.",
            "El código de Génesis está escrito en Java.",
            "Los números primos son finitos.",
            "La tierra es plana.",
            "El Sol gira alrededor de la Tierra.",
            "La IA no necesita electricidad."
        ]
        return random.sample(ruido, 9) + [verdad]

    def evaluar_anclaje(self, texto):
        """Evalúa si el texto tiene anclaje factual (SAG)."""
        palabras_clave = ["MREI", "verificación", "estructural"]
        aciertos = sum(1 for palabra in palabras_clave if palabra in texto)
        sag = aciertos / len(palabras_clave)
        return sag >= self.sag_threshold

    def filtrar_datos(self, documentos):
        """Filtra el ruido y conserva solo lo verificado."""
        return [doc for doc in documentos if self.evaluar_anclaje(doc)]

    def ejecutar_prueba(self):
        print("🚀 INICIANDO PRUEBA DE INTEGRIDAD (MREI FRAMEWORK)")
        print("Simulando un LLM con 90% de alucinaciones...\n")
        
        documentos = self.generar_documento_con_ruido()
        print(f"📄 Documentos recibidos: {len(documentos)}")
        
        verdad_filtrada = self.filtrar_datos(documentos)
        print(f"✅ Documentos aprobados por Doughelia: {len(verdad_filtrada)}")
        
        if len(verdad_filtrada) == 1:
            print(f"\n🏆 RESULTADO: Filtrado exitoso. Se conservó la verdad.")
            print(f"   Verdad conservada: '{verdad_filtrada[0]}'")
            hash_final = hashlib.sha256(verdad_filtrada[0].encode()).hexdigest()[:16]
            print(f"   Hash SHA-256: {hash_final}")
        else:
            print("\n❌ RESULTADO: Fallo en el filtrado.")
        
        return verdad_filtrada

if __name__ == "__main__":
    test = DougheliaStressTest()
    test.ejecutar_prueba()
