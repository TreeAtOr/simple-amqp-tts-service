import threading

import pika
import os, time
import pickle
import io
import threading



class TTSThread(threading.Thread):
    def __init__(self, speaker, amqp_uri, in_queue, out_queue, output_folder):
        threading.Thread.__init__(self)
        params = pika.URLParameters(amqp_uri)
        params.socket_timeout = 5

        while True:
            succeeded = False
            try:
                connection = pika.BlockingConnection(params)
                self.ichannel = connection.channel()
                self.ichannel.queue_declare(queue=in_queue)

                self.ochannel = connection.channel()
                self.ochannel.queue_declare(queue=out_queue)

                succeeded = True
            
            except Exception as error:
                print('[TTS] Failed to connect to AMQP...')
                time.sleep(10)
            if succeeded:
                break

        def handle_tts_message(_id, content, filename):
            if not os.path.exists(filename):
                speaker.save_wav(content, filename)
                print(f"[TTS] Created result file {filename}")

            msg = {"type": "ready", "_id": _id}
            self.ochannel.basic_publish(
                exchange='', routing_key=out_queue, body=pickle.dumps(msg))

        def handle_message(ch, method, properties, body):
            request = pickle.loads(body)
            _id = request['_id']
            filename = f'{output_folder}/{_id}.wav'
            try:
                if(request['type'] == 'tts'):
                    handle_tts_message(_id, request['content'], filename)
                if(request['type'] == 'free'):
                    filename = request['_id']
                    print(f"[TTS] Removing file {filename}")
                    os.remove(f'{output_folder}/{filename}.wav')
            except Exception as error:
                msg = {"type": "error",
                       "_id": request['_id'], "content": error}
                self.ochannel.basic_publish(
                    exchange='', routing_key=out_queue, body=pickle.dumps(msg))

        self.ichannel.basic_consume(
            in_queue, handle_message, auto_ack=True)

    def run(self):
        print("[TTS] Text-to-speech is now running")
        self.ichannel.start_consuming()
        self.connection.close()
