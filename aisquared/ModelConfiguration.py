import json
from aisquared.preprocessing import TabularPreprocessor, ImagePreprocessor, LanguagePreprocessor
from aisquared.postprocessing import BinaryClassification, MulticlassClassification, ObjectDetection, Regression

PREPROCESSING_CLASSES = (
    TabularPreprocessor,
    ImagePreprocessor,
    LanguagePreprocessor
)

POSTPROCESSING_CLASSES = (
    BinaryClassification,
    MulticlassClassification,
    ObjectDetection,
    Regression
)    

class ModelConfiguration:
    """
    An object that contains all pre- and postprocessing configuration for the model
    """
    def __init__(
            self,
            preprocessing_steps,
            postprocessing_steps,
            input_shapes,
            mlflow_uri = None,
            mlflow_user = None,
            mlflow_token = None            
    ):
        """
        Parameters
        ----------
        preprocessing_steps : list or aisquared.preprocessing class
            The preprocessing steps to occur for each input to the model
        postprocessing_steps : list or aisquared.postprocessing class
            The postprocessing steps to occur for each output to the model
        input_shapes : list of int
            The input shapes for the model
        mlflow_uri : None or str (default None)
            The MLFlow URI to point to
        mlflow_user : None or str (default None)
            The MLFlow user to use
        mlflow_token : None or str (default None)
            The MLFlow token for authentication
        """
        
        self.preprocessing_steps = preprocessing_steps
        self.postprocessing_steps = postprocessing_steps
        self.input_shapes = input_shapes
        self.mlflow_uri = mlflow_uri
        self.mlflow_user = mlflow_user
        self.mlflow_token = mlflow_token

    @property
    def preprocessing_steps(self):
        return self._preprocessing_steps
    @preprocessing_steps.setter
    def preprocessing_steps(self, value):
        if isinstance(value, PREPROCESSING_CLASSES):
            self._preprocessing_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, PREPROCESSING_CLASSES) for val in value]):
            self._preprocessing_steps = value
        else:
            raise TypeError('preprocessing_steps must be a single instance of or a list of instances of classes in the `aisquared.preprocessing` package')

    @property
    def postprocessing_steps(self):
        return self._postprocessing_steps
    @postprocessing_steps.setter
    def postprocessing_steps(self, value):
        if isinstance(value, POSTPROCESSING_CLASSES):
            self._postprocessing_steps = [value]
        elif isinstance(value, list) and all([isinstance(val, POSTPROCESSING_CLASSES) for val in value]):
            self._postprocessing_steps = value
        else:
            raise TypeError('postprocessing_stpes must be a single instance of or a list of instances of classes in the `aisquared.postprocessing` package')

    @property
    def input_shapes(self):
        return self._input_shapes
    @input_shapes.setter
    def input_shapes(self, value):
        if not isinstance(value, list):
            raise TypeError('input_shapes must be list of list of ints')
        if not all([isinstance(val, list) for val in value]):
            raise TypeError('input_shapes must be list of list of ints')
        for val in value:
            if not all([isinstance(v, int) for v in val]):
                raise TypeError('input_shapes must be list of list of ints')
        self._input_shapes = value
        
    @property
    def mlflow_uri(self):
        return self._mlflow_uri
    @mlflow_uri.setter
    def mlflow_uri(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError('mlflow_uri must be None or str')
        self._mlflow_uri = value

    @property
    def mlflow_user(self):
        return self._mlflow_user
    @mlflow_user.setter
    def mlflow_user(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError('mlflow_user must be None or str')
        self._mlflow_user = value

    @property
    def mlflow_token(self):
        return self._mlflow_token
    @mlflow_token.setter
    def mlflow_token(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError('mlflow_token must be None or str')
        self._mlflow_token = value

    def to_dict(self):
        """
        Get the ModelConfiguration object as a dictionary
        """
        return {
            'modelConfig' : {
                'uri' : self.mlflow_uri,
                'user' : self.mlflow_user,
                'token' : self.mlflow_token,
                'preprocessing' : [step.to_dict() for step in self.preprocessing_steps],
                'postprocessing' : [step.to_dict() for step in self.postprocessing_steps]
            }
        }

    def to_json(self):
        """
        Get the ModelConfiguration object as a JSON string
        """
        return json.dumps(self.to_dict())
