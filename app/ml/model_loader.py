_model = None

def load_model():
    global _model
    if _model is None:
        _model = "mock-model"
    return _model
