import azure.cognitiveservices.speech as speech_sdk
import pyaudio
import time
from pathlib import Path
import json

# pyaudio stream config
CHUNK = 1600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def read_credentials():
    """
    Read from file authentication data to connect azure. The file should be in the main folder
    Returns:
        dict 
        Dictionary with credentials
    """
    path = Path.joinpath(Path.cwd(), 'credentials.json')
    if path.exists():
        with open(path) as file:
            credentials = json.load(file)
        return credentials
    else:
        raise(FileNotFoundError("File '{}' is not found").format(str(path)))


class Speech:
    def __init__(self, logs_writer, text_writer):
        """
        Parameters
        ----------
        logs_writer : function to save logs from events
        text_writer : function to save recognised text
        """
        self.state = True
        self.logs_writer = logs_writer
        self.text_writer = text_writer
        #read credentials from file
        credentials = read_credentials()
        #set proper language
        self.language = credentials.get('language')
        #define configurations for speech recognition
        self.speech_config = speech_sdk.SpeechConfig(subscription=credentials.get('key'),
                                                     region=credentials.get('region'))

        # setup the audio stream
        self.sdk_stream = speech_sdk.audio.PushAudioInputStream()
        self.audio_config = speech_sdk.audio.AudioConfig(stream=self.sdk_stream)

        # instantiate the speech recognizer with push stream input
        self.speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=self.speech_config,
                                                             audio_config=self.audio_config,
                                                             language=self.language)
        
    def messages(self):
        """
        Connect callbacks to the events fired by the speech recognizer
        """
        # partial recognised speech event
        self.speech_recognizer.recognizing.connect(lambda evt: self.text_writer(evt))
        # full recognised speech event
        self.speech_recognizer.recognized.connect(lambda evt: self.text_writer(evt))
        # start session event
        self.speech_recognizer.session_started.connect(lambda evt: self.logs_writer('SESSION STARTED: {}'.format(evt)))
        # stop session event
        self.speech_recognizer.session_stopped.connect(lambda evt: self.logs_writer('SESSION STOPPED {}'.format(evt)))
        # cancel session event
        self.speech_recognizer.canceled.connect(lambda evt: self.logs_writer('CANCELED {}'.format(evt)))

    def start_pa_stream(self):
        """
        Start capturing audio 
        """
        self.pa = pyaudio.PyAudio()
        # set default system input as a input for capturing
        default_input=self.pa.get_default_input_device_info()
        self.logs_writer("Your default input is '{}'".format(default_input['name']))
        # create pyaudio stream object
        self.pa_stream = self.pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK,
                                      input_device_index=default_input['index'])

    def start_sdk_stream(self):
        """
        Start stream to azure service
        """
        # start continuous speech recognition
        self.speech_recognizer.start_continuous_recognition()
        # start pushing data until the break
        while self.state:
            # load audio frame
            frames = self.pa_stream.read(CHUNK)
            # send audio frame to azure stream
            self.sdk_stream.write(frames)
            time.sleep(.1)

    def stop_stream(self):
        """
        Stop and close both stream
        """
        self.close_pa_stream()
        self.close_sdk_stream()
        self.pa.terminate()
        
    def close_pa_stream(self):
        """
        Stop capturing audio from computer and close stream
        """
        self.pa_stream.stop_stream()
        self.pa_stream.close()

    def close_sdk_stream(self):
        """
        Stop and close streaming audio to azure service
        """
        self.sdk_stream.close()
        self.speech_recognizer.stop_continuous_recognition()