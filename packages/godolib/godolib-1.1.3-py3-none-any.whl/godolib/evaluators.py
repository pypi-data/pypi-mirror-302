from tensorflow.keras import backend as K

def r2(y_true, y_pred):
    """
    Calcula el coeficiente de determinación R², que mide la calidad de ajuste de un modelo de regresión lineal.

    El coeficiente de determinación R² indica la proporción de la varianza en la variable dependiente que es explicada
    por las variables independientes del modelo. Un valor de R² de 1 indica un ajuste perfecto, mientras que un valor
    de 0 indica que el modelo no explica ninguna de las variaciones en los datos.

    Parámetros:
    -----------
    y_true : tensor
        Tensor de valores reales observados (verdaderos).
        
    y_pred : tensor
        Tensor de valores predichos por el modelo.

    Retorna:
    --------
    float
        Valor del coeficiente de determinación R².

    Descripción del cálculo:
    ------------------------
    - `ss_res`: Suma de los residuos al cuadrado, que representa la suma de las diferencias entre los valores predichos
      y los valores reales elevados al cuadrado.
    - `ss_tot`: Suma total de cuadrados, que representa la variación total de los valores reales en torno a su media.
    - El coeficiente R² se calcula como: 1 - (ss_res / ss_tot).
    - `K.epsilon()` se usa para evitar divisiones por cero.

    """
    ss_res = K.sum(K.square(y_true - y_pred))  # Suma de los residuos al cuadrado
    ss_tot = K.sum(K.square(y_true - K.mean(y_true)))  # Suma total de cuadrados
    return 1 - ss_res / (ss_tot + K.epsilon())
