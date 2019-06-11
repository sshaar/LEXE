import os
import sys
import shlex
import subprocess
from tqdm import tqdm 

sys.path.append('/Users/sshaar/hackathon/frontend/theme/backend/tacotron')
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer

def load_model(model_path='/Users/sshaar/hackathon/frontend/theme/backend/models/tacotron-20180906/model.ckpt'):
	model = Synthesizer()
	model.load(model_path)

	return model


def synthesize(model, sentence, audio_path=''):
	audio = model.synthesize(sentence)
	if audio_path:
		with open(audio_path, 'wb') as f:
			f.write(audio)
	return audio


def synthesize_parapgraph(model, paragraph, output_name='/Users/sshaar/hackathon/frontend/theme/output.wav'):

	try:
		cmd = 'rm /Users/sshaar/hackathon/frontend/theme/backend/sentences/*'
		output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.PIPE)
	except:
		pass

	sentences = paragraph.split('.')	

	for i, sentence in enumerate(tqdm(sentences[:6])):
		synthesize(model, sentence, '/Users/sshaar/hackathon/frontend/theme/backend/sentences/{:03d}.wav'.format(i))

	sox_cmd = 'sox /Users/sshaar/hackathon/frontend/theme/backend/sentences/*.wav ' + output_name
	output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)



if __name__ == '__main__':
    model = load_model()

    sentence = 'When is it due'
    sentence = 'How long does it take?'
    sentence = 'Can you say that again?'
    para = "The world's first computer science degree program, the Cambridge Diploma in Computer Science, began at the University of Cambridge Computer Laboratory in 1953. [note 3] The design and deployment of computers and computer systems is generally considered the province of disciplines other than computer science. Computer science is considered by some to have a much closer relationship with mathematics than many scientific disciplines, with some observers saying that computing is a mathematical science. Computer architecture, or digital computer organization, is the conceptual design and fundamental operational structure of a computer system. Computer science research also often intersects other disciplines, such as philosophy, cognitive science, linguistics, mathematics, physics, biology, statistics, and logic. [57] In 1981, the BBC produced a micro-computer and classroom network and Computer Studies became common for GCE O level students (11–16-year-old), and Computer Science to A level students. [11] As it became clear that computers could be used for more than just mathematical calculations, the field of computer science broadened to study computation in general."
    # audio = synthesize(model, sentence, audio_path='cannot_hear.wav')

    synthesize_parapgraph(model, para, output_name='/Users/sshaar/')
