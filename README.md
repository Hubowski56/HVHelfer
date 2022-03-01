# HVHelfer
Application aims to recognise speech and translate it to text.
It uses Speech to Text service from Azure Cognitive Services. 
The process of speech recognition is following:
1. Audio is capturing from default audio input in your computer.
2. Sound is streaming to Azure Speech Service.
3. Azure service is returning recognised speech as a text.
4. This text is displaying on your screen almost in real time.

# Configuration

1. Create required resource on Azure.
2. Fill file credentials.json using authentication data(region and key) from Azure. Write also the language of speech.
3. If you want to capture audio from your speakers(i.e when you want to see speech as a text during watching a german film or TV) you should set 'Mix Stereo' as a default input source. In this case the audio is captured internally and directly from audio source(i.e a film).

![image](https://user-images.githubusercontent.com/99900749/156261634-a5d06db2-3738-410e-b5ae-6ccaa69b7509.png)
# App

4. Now you can run the application and click start recording button.
5. In the top text box there is a recognised speech. During recognising speech, initially, the text is displayed as raw text without interpunction, capital letters and with possible grammar errors. It is a partial recognised text. During further recording old partial recognised text will be replaced by full recognised text with interpunction and grammatically correct but new recognised one is raw yet. After stopping recording all text is replaced by full recognised text.
6. In the bottom text box there are logs. There you can find a name of your default input source and information about start and stop of session events. Also there any errors are shown.
7. If you want to stop capturing click on stop recording button. 
![image](https://user-images.githubusercontent.com/99900749/156262844-4b58f8a4-6bea-4e3d-baee-98e0e4cfe626.png)




