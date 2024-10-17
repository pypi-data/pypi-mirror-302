import numpy as np

class PredictionResults:
    """Stores an array of dictionaries containing prediction results
    and filters specific keys (output_details' attributes)
    into their respective arrays.

    Returns
    -------
    PredictionResults
        Flattened array of dictionaries by keys (output_details attributes)

    Raises
    ------
    TypeError
        If items in raw_data are not dictionaries.
    """    
    

    def __init__(self, results):
        self.raw_data = results
        self._initialize_attributes()

        # compute weights concentration and add to class
        self.weights_concentration = [np.std(row) for row in self.weights]
        if hasattr(self, 'weights_compound'):
            self.weights_concentration_compound = [np.std(row) for row in self.weights_compound]

    def _initialize_attributes(self):
        allowed_keys = [
            'yhat', 
            'weights', 
            'weights_excluded', 
            'relevance', 
            'similarity',
            'info_x', 
            'info_theta', 
            'include', 
            'lambda_sq', 
            'n', 
            'K', 
            'phi',
            'r_star', 
            'r_star_percent', 
            'most_eval', 
            'eval_type', 
            'adjusted_fit',
            'fit', 
            'rho', 
            'agreement', 
            'outlier_influence', 
            'asymmetry', 
            'variable_importance', 
            'y_linear',
            'yhat_grid', 
            'weights_grid', 
            'adjusted_fit_grid', 
            'max_attributes',
            'combi_grid', 
            'yhat_compound', 
            'adjusted_fit_compound', 
            'fit_compound',
            'combi_compound',
            'weights_compound', 
            'maxfit_index_grid'
        ]

        if not self.raw_data:
            return
        
        if isinstance(self.raw_data, dict):
            first_item = self.raw_data
            self.raw_data = [self.raw_data]
        else:
            first_item = self.raw_data[0]

        if not isinstance(first_item, dict):
            raise TypeError("PredictionResults: Items in raw_data must be dictionaries")
        
        keys_to_populate = [key for key in first_item if key in allowed_keys]

        for key in keys_to_populate:
            values = []
            for item in self.raw_data:
                if key in item:
                    value = item[key]
                    if isinstance(value, np.ndarray) and value.shape == (1, 1):
                        value = value[0][0]
                    values.append(value)
            setattr(self, key, values)
            

    def attributes(self):
        """Display a list of accessible attributes of the class

        Returns
        -------
        list
            List of accessble attributes of the class.
        """        
        
        attribute_list = [key for key in self.__dict__.keys() if not key.startswith('__')]
        return attribute_list


    def display(self):
        """Display key-value pairs of all accessible attributes of the class.
        """        
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                print(f"{attr}: {getattr(self, attr)}")


    def __repr__(self):
        """Displays a list of all accessible attributes in the class
        """
        class_name = self.__class__.__name__
        attributes = "\n".join(f"- {key}" for key in self.raw_data[0].keys())
        return f"\nResults:\n--------- \n{attributes}\n--------- "