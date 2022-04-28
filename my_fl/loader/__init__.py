class TorchLoader:
    def list(self):
        from torchvision import datasets

        return datasets.__all__

    def download(self, name, path=".fed/datasets"):
        from torchvision import datasets

        names = set(self.list())
        if name not in names:
            KeyError(f"{name}")

        dataset = getattr(datasets, name)
        dataset(root=".fed/datasets", train=False, download=True)
