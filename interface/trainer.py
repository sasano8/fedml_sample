from fedml_core.trainer.model_trainer import ModelTrainer


class MyModelTrainer(ModelTrainer):
    def get_model_params(self):
        ...

    def set_model_params(self, model_parameters):
        self.model.load_state_dict(model_parameters)

    def train(self, train_data, device, args):
        ...


    def test(self, test_data, device, args):
        ...

    def test_on_the_server(self, train_data_local_dict, test_data_local_dict, device, args=None) -> bool:
        ...

class MyModelTrainerNWP(MyModelTrainer):
    """FedMLではただのMyModelTrainerのエイリアスで、何のため別名をつけているのか意図が分からない"""
    ...

class MyModelTrainerTAG(MyModelTrainer):
    """FedMLではただのMyModelTrainerのエイリアスで、何のため別名をつけているのか意図が分からない"""
    ...