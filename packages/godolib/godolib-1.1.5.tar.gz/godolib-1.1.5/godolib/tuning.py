import random


class HyperparametersSelector:
    """
    A class for selecting hyperparameters based on given configurations.

    Attributes:
        hps (dict): A dictionary to store hyperparameter names and their selected values.

    Methods:
        Int(name, min_value, max_value, step): Returns an integer hyperparameter.
        Float(name, min_value, max_value, step): Returns a floating-point hyperparameter.
        Choice(name, values): Returns a choice from given possible values.
        _get_values_(): Returns the dictionary of all hyperparameter values.
    """

    def __init__(self, hps_configuration=None):
        """
        Initializes the HyperparametersSelection with an optional hyperparameters configuration.

        Args:
            hps_configuration (dict, optional): A pre-defined dictionary of hyperparameters. Defaults to None.
        """
        self.hps = {} if hps_configuration is None else hps_configuration

    def Int(self, name, min_value, max_value, step):
        """
        Generates or retrieves an integer hyperparameter within the specified range, using the specified step.

        Args:
            name (str): The name of the hyperparameter.
            min_value (int): The minimum value of the range.
            max_value (int): The maximum value of the range.
            step (int): The step between possible values within the range.

        Returns:
            int: The chosen or retrieved integer value for the hyperparameter.

        Raises:
            ValueError: If min_value is greater than max_value or if step is not positive.
        """
        if name in self.hps:
            return self.hps[name]
        if min_value > max_value:
            raise ValueError("min_val must be less than or equal to max_val")
        if step <= 0:
            raise ValueError("step must be a positive number")
        number = random.choice(range(min_value, max_value + 1, step))
        self.hps[name] = number
        return number

    def Float(self, name, min_value, max_value, step):
        """
        Generates or retrieves a floating-point hyperparameter within the specified range, using the specified step.

        Args:
            name (str): The name of the hyperparameter.
            min_value (float): The minimum value of the range.
            max_value (float): The maximum value of the range.
            step (float): The step between possible values within the range.

        Returns:
            float: The chosen or retrieved floating-point value for the hyperparameter.

        Raises:
            ValueError: If min_value is greater than max_value or if step is not positive.
        """
        if name in self.hps:
            return self.hps[name]
        if min_value > max_value:
            raise ValueError("min_val must be less than or equal to max_val")
        if step <= 0:
            raise ValueError("step must be a positive number")
        number = random.choice([min_value + i * step for i in range(int((max_value - min_value) / step) + 1)])
        self.hps[name] = number
        return number

    def Choice(self, name, values):
        """
        Chooses or retrieves a value from a list of possible values for a hyperparameter.

        Args:
            name (str): The name of the hyperparameter.
            values (list): A list of possible values from which to choose.

        Returns:
            Any: The chosen or retrieved value from the list.

        Raises:
            ValueError: If the list of possible values is empty.
        """
        if name in self.hps:
            return self.hps[name]
        if not values:
            raise ValueError("list cannot be empty")
        election = random.choice(values)
        self.hps[name] = election
        return election

    def _get_values_(self):
        """
        Retrieves the dictionary containing all hyperparameter names and their selected values.

        Returns:
            dict: The dictionary of hyperparameter names and values.
        """
        return self.hps


class RandomSearch():
    """
    Clase RandomSearch para realizar una búsqueda aleatoria de hiperparámetros para un modelo de aprendizaje profundo.

    Atributos:
    ----------
    buildin_func : function
        Función que recibe un objeto de hiperparámetros y devuelve un modelo configurado.
    objective : str
        Métrica de validación que se utilizará para optimizar los hiperparámetros. Debe ser una de las siguientes: 
        ['val_loss', 'val_mae', 'val_mse', 'val_mape', 'val_r2'].
    max_trials : int
        Número máximo de configuraciones de hiperparámetros a probar.
    executions_per_trial : int
        Número de veces que se ejecutará el entrenamiento para cada configuración de hiperparámetros.
    results : dict
        Diccionario que almacena los resultados de las configuraciones probadas. Las keys son los números de los trials, 
        y los valores son una tupla con la configuración de hiperparámetros y el valor promedio de la métrica objetivo.

    Métodos:
    --------
    __init__(self, buildin_func, objective, max_trials, executions_per_trial):
        Inicializa la clase RandomSearch con la función de construcción de modelos, el objetivo a optimizar, 
        el número máximo de configuraciones (trials) y las ejecuciones por trial.

    search(self, X, Y, epochs, batch_size, validation_data, callbacks, verbose=1):
        Ejecuta la búsqueda de hiperparámetros. Entrena varios modelos con configuraciones de hiperparámetros aleatorios y
        selecciona el mejor basado en la métrica objetivo.
        
        Parámetros:
        -----------
        X : array-like
            Datos de entrada para el entrenamiento.
        Y : array-like
            Etiquetas o valores objetivo para el entrenamiento.
        epochs : int
            Número de épocas para entrenar cada modelo.
        batch_size : int
            Tamaño del lote utilizado durante el entrenamiento.
        validation_data : tuple
            Datos de validación en forma de (X_val, Y_val) para calcular la métrica objetivo.
        callbacks : list
            Lista de callbacks a utilizar durante el entrenamiento.
        verbose : int, opcional
            Nivel de verbosidad (1 por defecto). Determina qué tan detallada será la salida impresa.

    _generator_(self):
        Genera una nueva configuración de hiperparámetros utilizando la función de construcción y un objeto de selección de hiperparámetros.
        
        Retorna:
        --------
        hps_configuration : dict
            Diccionario que contiene los valores de la configuración de hiperparámetros generados.
        hps_object : object
            Objeto que contiene la información de los hiperparámetros seleccionados.
    """

    def __init__(self, building_func, objective, max_trials, executions_per_trial):
        self.building_func = building_func
        valid_objectives = ['val_loss', 'val_mae', 'val_mse', 'val_mape', 'val_r2']
        if objective not in valid_objectives:
            raise ValueError(f"'{objective}' is not a valid mode. Choose from {valid_objectives}.")
        self.objective = objective
        self.max_trials = max_trials
        self.executions_per_trial = executions_per_trial

    def search(self, X, Y, epochs, batch_size, validation_data, callbacks, verbose=1):
        """
        Realiza la búsqueda de hiperparámetros probando varias configuraciones de modelos.

        Parámetros:
        -----------
        X : array-like
            Conjunto de datos de entrada para el entrenamiento del modelo.
        Y : array-like
            Conjunto de etiquetas o valores objetivo para el entrenamiento.
        epochs : int
            Número de épocas para entrenar cada modelo.
        batch_size : int
            Tamaño del batch utilizado durante el entrenamiento.
        validation_data : tuple
            Conjunto de datos de validación en la forma (X_val, Y_val).
        callbacks : list
            Lista de callbacks a utilizar durante el entrenamiento.
        verbose : int, opcional
            Nivel de verbosidad del proceso de entrenamiento, por defecto es 1.

        Retorna:
        --------
        None
        """
        print('Searching: \n')
        self.results = {}
        for trial in range(self.max_trials):
            print(f'Searching model: {trial}')
            trial_results = []
            current_hps_configuration, current_hp_object = self._generator_()
            for model_trial in range(self.executions_per_trial):
                print(f'model trial: {model_trial}')
                model = self.building_func(current_hp_object)
                history = model.fit(x=X, y=Y, batch_size=batch_size, epochs=epochs, verbose=verbose, 
                                    callbacks=callbacks, validation_data=validation_data)

                # Seleccionar la métrica según el objetivo
                if self.objective == 'val_loss':
                    score = history.history['val_loss'][-1]
                    self.reverse = False
                elif self.objective == 'val_mae':
                    score = history.history['val_mae'][-1]
                    self.reverse = False
                elif self.objective == 'val_mse':
                    score = history.history['val_mse'][-1]
                    self.reverse = False
                elif self.objective == 'val_mape':
                    score = history.history['val_mape'][-1]
                    self.reverse = False
                elif self.objective == 'val_r2':
                    score = history.history['val_r2'][-1]
                    self.reverse = True

                trial_results.append(score)

            self.results[trial] = (current_hps_configuration, sum(trial_results) / len(trial_results))

        # Ordenar los resultados según la métrica objetivo
        self.results = {k: v for k, v in sorted(self.results.items(), key=lambda item: item[1][1], reverse=self.reverse)}

    def _generator_(self):
        """
        Genera una nueva configuración de hiperparámetros aleatoria.

        Retorna:
        --------
        hps_configuration : dict
            Configuración generada de los hiperparámetros.
        hps_object : object
            Objeto que contiene los hiperparámetros seleccionados.
        """
        hps_object = HyperparametersSelector()
        _ = self.building_func(hps_object)
        hps_configuration = hps_object._get_values_()
        return hps_configuration, hps_object