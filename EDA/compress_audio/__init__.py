from ffmpy import FFmpeg
import os, glob
class Normalize_Audio():
    def __init__(self):
        ''' Constructor for this class. '''
        pass
        
    def normalize(infile,bitrate):
        filename=os.path.splitext(os.path.split(infile)[1])[0]
        filepath=os.path.dirname(infile)+"\\normalized"
        try:
            os.mkdir(filepath)
        except OSError:
            pass

        ff = FFmpeg(inputs={infile: None},outputs={'%s\%s_normalized.mp3'%(filepath,filename): '-ac 1 -ab %s'%(bitrate)})
        ff.run()
        return print("File Normalized")
        
    def compress(infile,bitrate):
        filename=os.path.splitext(os.path.split(infile)[1])[0]
        filepath=os.path.dirname(infile)+"\\compressed"
        try:
            os.mkdir(filepath)
        except OSError:
            pass
        ff = FFmpeg(inputs={infile: None},outputs={'%s\%s_compressed.mp3'%(filepath,filename): '-ac 1 -ab %s'%(bitrate)})
        ff.run()
        return print("File Compressed")

