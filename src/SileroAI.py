import torch
from inspect import signature
class Speaker:
    def __init__(self,speaker,sample_rate,model):
        self.speaker = speaker
        self.sample_rate = sample_rate
        self.model = model
    
    def save_wav(self, ssml_text,path):
        return self.model.save_wav(
                              audio_path=path,
                              ssml_text=ssml_text,
                              speaker=self.speaker,
                              sample_rate=self.sample_rate)
    
    def apply_tts(self, ssml_text):
        return  self.model.apply_tts(ssml_text=ssml_text,
                              speaker=self.speaker,
                              sample_rate=self.sample_rate)

class SileroAI:
    def __init__(self, language, model_id, device):
        self.language = language
        self.model_id = model_id
        self.device = torch.device(device)

        self.model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                  model='silero_tts',
                                                  language=language,
                                                  speaker=model_id)
        self.model.to(self.device)
    
    def createSpeaker(self, speaker, sample_rate = 48000):
        return Speaker(speaker,sample_rate,self.model)


    

