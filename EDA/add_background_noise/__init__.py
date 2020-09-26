from pydub import AudioSegment
import os, random
class Background_noise():
    def __init__(self):
        ''' Constructor for this class. '''
        pass
        
    def random_noise(infile,background_noise_path):
        filename=os.path.splitext(os.path.split(infile)[1])[0]
        filepath=os.path.dirname(infile)+"\\bn_added"
        try:
            os.mkdir(filepath)
        except OSError:
            pass

        orig_audio = AudioSegment.from_file(infile)
        background_noise = random.choice(os.listdir(background_noise_path))
        noise_add = AudioSegment.from_file(background_noise_path+"/"+background_noise)
        outfile = orig_audio.overlay(noise_add)
        outfile.export("%s\%s_bn_added.wav"%(filepath,filename), format='wav')
#         return print("File with background noise saved")