_model = None

def load_model():
    global _model
    if _model is None:
        # Example: load a pickle/sklearn/torch/tf model
        # _model = joblib.load("models/my_model.joblib")
        _model = "mock-model"
    return _model
