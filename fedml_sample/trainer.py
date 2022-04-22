from fedml_core.trainer.model_trainer import ModelTrainer


class ModelTrainer:
    def set_id(self, trainer_id):
        ...
    def get_model_params(self):
        ...
    def set_model_params(self, model_parameters):
        ...
    def train(self, train_data, device, args=None):
        ...
    def test(self, test_data, device, args=None):
        ...
    def test_on_the_server(self, train_data_local_dict, test_data_local_dict, device, args=None) -> bool:
        pass    



class FederateTrainer:
    def update_model(self, weights):
        ...
    
    def update_dataset(self, client_index):
        ...

    def train(self, round_idx = None):
        ...

    def test(self):
        ...



class MyModelTrainerNWP(ModelTrainer):
    """FedMLではただのMyModelTrainerのエイリアスで、何のため別名をつけているのか意図が分からない"""
    ...

class MyModelTrainerTAG(ModelTrainer):
    """FedMLではただのMyModelTrainerのエイリアスで、何のため別名をつけているのか意図が分からない"""
    ...

class MyModelTrainerCLS(ModelTrainer):
    """FedMLではただのMyModelTrainerのエイリアスで、何のため別名をつけているのか意図が分からない"""
    ...
