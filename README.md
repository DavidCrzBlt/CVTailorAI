# 🧠 CVTailorAI

## Descripción
CVTailorAI es una aplicación personal que adapta tu CV, carta de presentación y correo de aplicación a diferentes vacantes usando **Google Gemini** a través de **LangChain**.  
El proyecto se ejecuta localmente con **FastAPI** y almacena las vacantes aplicadas en **PostgreSQL**.

---

## 🚀 Flujo de la Aplicación

1. **Usuario** ingresa su información personal y profesional (perfil, habilidades, experiencia).  
2. **Vacante**: se introduce texto o URL de la oferta laboral.  
3. **Modelo LLM (Gemini)** genera:
   - CV adaptado en formato Markdown (convertible a PDF)
   - Carta de presentación personalizada
   - Asunto y cuerpo de correo de aplicación
4. **Base de datos**: se guarda el historial de aplicaciones.

---

## 🧩 Estructura del Proyecto

