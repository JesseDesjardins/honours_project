import os

from stable_baselines3.common.callbacks import BaseCallback

class SaveImageAndActionEachStateCallback(BaseCallback):
    """
    Callback for saving an image and an action after each state.

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """
    def __init__(self, log_dir: str, verbose=1):
        super(SaveImageAndActionEachStateCallback, self).__init__(verbose)
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'best_model')
        self.obs = self.training_env

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.log_dir is not None:
            os.makedirs(self.log_dir, exist_ok=True)

    def _on_step(self) -> bool:
        action, _ = self.model.predict(self.obs)
        print(action)
        