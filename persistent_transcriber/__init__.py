import whisper
import torch

"""
Use this class when you just want an easy-to-use persistent Whisper engine but don't need APIs 
"""


class PersistentTranscriber:
    def __init__(self, model_name="medium"):
        self.cuda_support = torch.cuda.is_available()
        print('Loading model, this may take a while...')
        self.audio_model = whisper.load_model(model_name)
        print(f'Model {model_name} loaded (CUDA: {self.cuda_support})')

    def transcribe_file(self, filename):
        result = self.audio_model.transcribe(filename, fp16=self.cuda_support)
        return result
