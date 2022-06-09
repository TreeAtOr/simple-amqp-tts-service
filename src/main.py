from SileroAI import SileroAI
from ResultsServer import FTPServerThread, HTTPServerThread
from TTSService import TTSThread

from os import getenv


if __name__ == "__main__":
    silero = SileroAI(getenv('TTS_LANGUAGE'), getenv(
        'TTS_MODEL'), getenv('TORCH_DEVICE'))
    speaker = silero.createSpeaker(getenv('TTS_SPAEKER'))

    tts = TTSThread(speaker,
                    getenv('AMQP_URL'),
                    getenv('AMQP_IN_QUEUE'),
                    out_queue=getenv('AMQP_OUT_QUEUE'),
                    output_folder='results')
    tts.start()

    if(getenv('SERVE_METHOD') == 'ftp'):
        server = FTPServerThread(getenv('SERVE_PORT'), "./results")
        server.start()
    elif(getenv('SERVE_METHOD') == 'http'):
        server = HTTPServerThread(getenv('SERVE_PORT'), "./results")
        server.start()
