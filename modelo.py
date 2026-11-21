"""Etapa 4 - PREDECIR (lógica del modelo, separada de la interfaz).

Entrena una regresión logística que estima la probabilidad de que un ticket
incumpla el SLA, y agrega esa probabilidad a cada fila del dataset.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

TARGET = "incumplio_sla"

NUM_COLS = [
    "antiguedad_solicitante_meses", "adjuntos", "interacciones",
    "reasignaciones", "horas_primera_respuesta", "horas_abierto",
]
CAT_COLS = [
    "categoria_compra", "prioridad", "tipo_solicitud",
    "canal_entrada", "region", "turno",
]


def _construir_X(df):
    """Convierte las columnas en una matriz numérica para el modelo.

    - Numéricas: se usan tal cual.
    - Categóricas: one-hot encoding (una columna 0/1 por categoría).
    """
    X_num = df[NUM_COLS].copy()
    X_cat = pd.get_dummies(df[CAT_COLS].astype(str), drop_first=True).astype(int)
    return pd.concat([X_num, X_cat], axis=1)


def entrenar_modelo(df):
    df = df.copy()
    X = _construir_X(df)
    y = df[TARGET].astype(int)

    # Separamos en entrenamiento y prueba para medir de forma honesta.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Estandarizamos: dejamos todas las variables en la misma escala.
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train_s, y_train)

    # Métricas sobre los datos de PRUEBA (que el modelo no vio al entrenar).
    y_pred = modelo.predict(X_test_s)
    y_proba = modelo.predict_proba(X_test_s)[:, 1]
    metricas = {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion": confusion_matrix(y_test, y_pred),
        "n_test": len(y_test),
    }

    # Peso de cada variable (coeficiente de la regresión).
    coeficientes = pd.DataFrame({
        "variable": X.columns,
        "coeficiente": modelo.coef_[0],
    })
    coeficientes["abs"] = coeficientes["coeficiente"].abs()
    coeficientes = coeficientes.sort_values("abs", ascending=False)

    # Probabilidad estimada para TODOS los tickets (la usan las etapas 5 y 6).
    df["prob_incumplir"] = modelo.predict_proba(scaler.transform(X))[:, 1]

    return {
        "df_scored": df,
        "metricas": metricas,
        "coeficientes": coeficientes,
        "modelo": modelo,
    }
