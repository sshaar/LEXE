import pyaudio
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

def play_audio(path):
	f = wave.open(path,"rb")  
	p = pyaudio.PyAudio() 

	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  

	#read data  
	data = f.readframes(CHUNK)  

	#play stream  
	while data:  
	    stream.write(data)  
	    data = f.readframes(CHUNK)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	p.terminate()  


class aud():
	"""docstring for ClassName"""
	def play(self):
		
		


		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)

		print("* recording")

		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)

		print("* done recording")
		#print(frames)




		stream.stop_stream()
		stream.close()
		p.terminate()



		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()


		# instantiate PyAudio (1)
		p = pyaudio.PyAudio()

		# open stream (2)
		streamout = p.open(format=p.get_format_from_width(wf.getsampwidth()),
		                channels=wf.getnchannels(),
		                rate=wf.getframerate(),
		                output=True)

		# read data
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
		data = wf.readframes(CHUNK)

		# play stream (3)
		while len(data) > 0:
		    streamout.write(data)
		    data = wf.readframes(CHUNK)
		print("hellloooooo")
		# stop stream (4)
		streamout.stop_stream()
		streamout.close()

		# close PyAudio (5)
		p.terminate()
		wf.close()


if __name__ == '__main__':
	path = '/Users/sshaar/hackathon/frontend/theme/backend/due_date.wav'
	play_audio(path)



