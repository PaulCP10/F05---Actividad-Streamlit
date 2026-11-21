# Tickets de Compras: Toma de decisiones con datos

App de Streamlit para la materia **Ciencia de datos: Toma de decisiones en los
negocios**. Recorre el framework **Entender → Limpiar → Describir → Predecir →
Prescribir → Decidir** sobre solicitudes de un centro de compras.

**Pregunta guía:** ¿Qué tickets de compras tienen mayor probabilidad de
incumplir el SLA, y qué acción o priorización deberíamos tomar con cada tipo?

## Datos

- Archivo: `data/tickets_compras_sinteticos.csv`
- **Dataset sintético y anonimizado**, generado con `generar_dataset.py`. No
  contiene datos personales ni información real de ningún proveedor o empresa.
- 1,515 filas · 15 variables · incluye a propósito valores faltantes y
  duplicados para la etapa de limpieza.
- Unidad de análisis: **un ticket**. Variable objetivo: `incumplio_sla` (1/0).

## Cómo correr

```bash
# 1. Crear y activar el entorno virtual
py -m venv venv
venv\Scripts\Activate.ps1        # Windows (PowerShell)
# source venv/bin/activate       # Mac / Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run app.py
```

## Estructura

```
tickets_compras/
├── data/
│   └── tickets_compras_sinteticos.csv
├── tabs/
│   ├── entender.py       # 1. Entender
│   ├── limpiar.py        # 2. Limpiar
│   ├── descriptiva.py    # 3. Describir
│   ├── modelo.py         # lógica del modelo (regresión logística)
│   ├── predictiva.py     # 4. Predecir
│   ├── prescriptiva.py   # 5. Prescribir
│   └── decisiones.py     # 6. Decidir
├── app.py                # orquesta: carga, limpia, entrena y arma las pestañas
├── generar_dataset.py    # genera el dataset sintético (reproducible)
├── requirements.txt
└── .gitignore
```
