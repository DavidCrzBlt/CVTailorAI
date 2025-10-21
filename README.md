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

```
CVTailorAI/
│
├── app/
│ ├── main.py # Punto de entrada FastAPI
│ ├── routers/
│ │ ├── user.py # Endpoints para perfil del usuario
│ │ ├── job.py # Endpoints para vacantes
│ │ ├── generator.py # Endpoints para generar CVs y cartas
│ │
│ ├── services/
│ │ ├── langchain_service.py # Lógica de interacción con Gemini
│ │ ├── pdf_service.py # Conversión Markdown → PDF
│ │
│ ├── db/
│ │ ├── models.py # Modelos SQLAlchemy
│ │ ├── database.py # Conexión y sesión PostgreSQL
│ │
│ ├── templates/
│ │ └── cv_template.md # Plantilla base del CV
│ │
│ └── utils/
│ ├── text_cleaner.py # Limpieza y preprocesamiento de textos
│ └── parsers.py # Lectura y extracción de texto de vacantes
│
├── tests/ # Pruebas unitarias
├── requirements.txt
├── README.md
└── .env.example # Variables de entorno (DB_URL, API_KEYS, etc.)
```