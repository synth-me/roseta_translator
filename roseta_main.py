import textblob
from textblob import TextBlob
import nltk 
import speech_recognition as sr 
from gtts import gTTS
import pycountry 
import pyttsx3
import pyaudio
import wave
import wavio 
import sounddevice as sd
import soundfile as sf
import datetime 

# here we will process the brute data 
# comverting the data and analysis , organizing data structure 
# the system have route of Analysis -> Node Selection -> Translation -> Synthesis 

# this class is uniquely made for stuff that can bring some better ux for the api
# for example some ways of dtermining the both languages by the localization so that 
# there're no necessity of inputing it on your on 
# the use of this api, altough, is optional given that the app may have diffent options on it
class Peripherals:
# here you can use the geo localization to determine the languages 
    def by_localization(localization):
        return True
# or use the country itself
    def by_country(country):
        return True 

    def lang_total(lng_full,mode=0):
# here it is peripherical system that can get the full language and convert it into a alpah 2 encoding 
        lang_pos = {}
# here we get all the languages that there's an possible alpha 2 encoding 
        for l in pycountry.languages:
            p = pycountry.languages.get(name=l.name)
            try:
                alpha_kind = p.alpha_2
                lang_pos[p.name]=alpha_kind
            except:
                pass
        
# check if the language is in the dictionary 
        if mode != 0 and lng_full == None:
            return lang_pos
        else:
            if lng_full in lang_pos :
                return lang_pos[lng_full]
            else:
                return 0

    def record(n,duration=3):
# here we determine the hertz and the amount of time in which the system will be recording the audio
        fs = 44100  
        seconds = duration  
# we then start the recording
        print('started recording')  
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
# save the file with an specified name 
        name_file = '/Users/murie/'+str(n)+'.wav'
        wavio.write(name_file,myrecording,fs,sampwidth=2)  
        print('finished recording')
        return name_file
# and finish the recording
# returning the file name we can pass it as an argument for the next part of the system to find the file
   
class Analysis:
    def _init_(audio_file_primer,language_s):
# we just select the language from the file so that we can continue processing
        try:
            lg = Peripherals.lang_total(language_s)
            print(lg)
            r = sr.Recognizer()
            pre_processed = sr.AudioFile(audio_file_primer)
            with pre_processed as source:
                r.adjust_for_ambient_noise(source)
# we correct the ambient noise a bit using the already in-built function ( not as efficient as a current training model)
                audio_file = r.record(source)
            text = r.recognize_google(audio_file,language=lg)
# extracting the text out of the audio .wav
            return text
        except:
            print('error on Analysis._init_')
            return 'error 0' 

        
# to make the code more fixabe i added this excpetion handler 
# so that we can know faster where are the erros spotted 
        #print('error on Analysis._init_')
# all errors will have an number by the order it's shown
# the documentation will have an section about it so it'll easier for debbuging later if the test did not pass
        #return 'error 0'

class Node:
# here we will have multiple nodes , each node will work for an especific language 
# the language was already determined by the Analysis step. if the language have no especific node
# then an generic node is used
# the generic node is good for speed but far less precise then an specific node    
    def _selection_(text,language):
# the selection method will say all the avaiables systems to be used
# using an specific folder for all the possible especific nodes and a protocol for the name
# of the files, we can upload code whithin production so the system can be updated with no stop 
# by right now , though, we will only use the generic node 
        try:
            import languages_to_use
            from languages_to_use import language_list
# using this system to check the system's folder make the maintainability of the code better given that 
# the key/value pair of the file is always a pair of string/function
# so when a string is evoked as a key the value of it, which is the language sepcific node, is evoked as well
# then to add or remove nodes ( bad nodes or just updated ones) all we need to do is change the content of this specific file
# this technic has been used by different interpreters and has been proved as efficient(typescript, node and rails)
            lg = Peripherals.lang_total(language)
            
            if lg in language_list():
                node_s = language_list()[lg]
                if node_s == 0:
                    print('the specific node could not be used, using the common node then')
                    translated_text = TextBlob(text).translate(to=str(lg))    
                    return translated_text
                else:
                    return node_s(text)
            else:
                translated_text = TextBlob(text).translate(to=str(lg))
                return translated_text

        except:
            print('error on the Node._selection')            
            return 'error 1'

class Synthesis:
# the final part of the system requires us to synthetize the voice with the target language already selected 
# as we did before the synthetizer should be especific for each language. given that is not possible right now 
# we are gonna use the generic voice synthetizer , but the system will prepared to support next updates on it 
    def _init_(translated_text,target_language):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            engine.say(translated_text)
            engine.runAndWait()
            #synth = gTTS(text=translated_text, lang=target_language, slow=False)
            #synth.save('test_sample_2.wav')
            
            return translated_text 
        except:
            print('problem with the Synthesis._init_')
            return 'error 2'

# and here we just put all together to make sense of the errors and make it to debug 

class roseta:
# here each mode will return an different file for the api
# the default 0 will only return an audio(.wav) file
    def run(audio_file,my_language,target_language,mode=0):
        try:
            if mode == 1:
                return 0 
            else:
# as mentioned before, we can stop the exception handlers that will say us what is happening in a simpler way 
# for all those expcetions there's a string that represents it and stops the main process 
                text_init = Analysis._init_(audio_file,my_language)
                if text_init == 'error 0':
                    return text_init
                
                translated = Node._selection_(str(text_init),target_language)
                if translated == 'error 1':
                    return translated
                
                synth_text = Synthesis._init_(translated,target_language)
                if synth_text == 'error 2':
                    return synth_text
                
                return synth_text
        except:
            print('error while running main function')
            return 'error X'

    def sync_run(my_language,target_language,mode=0,sync=4,time_step=3):
# here we determine the amount of rounds in which the system will be running 
        try:
            if sync >= 4 :
                counter = 0
                while counter < sync :
# the default period of time recording is always 3 seconds , as long as it takes 
# the more time of synthetization it will be and more of delay in the translated sentence
                    p = Peripherals.record(counter,time_step)        
                    text = roseta.run(p,my_language,target_language,mode=0)
                    print(text)
                    counter+=1
            elif sync == True:
                counter = 0
                while True :
                    p = Peripherals.record(counter,time_step)        
                    text = roseta.run(p,my_language,target_language,mode=0)
                    print(text)
                    counter+=1
        except:
            return 'error on the main process, restart or check the documentation'


#roseta.sync_run('English','Portuguese')
