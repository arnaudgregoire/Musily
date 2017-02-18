import sys
import time
import matplotlib.pyplot as plt
import scipy.fftpack as f
import numpy 
import wave 
import pyaudio

chunk = 2**16
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS=16

freq_note=[55.0*(2.0**(k/12.0)) for k in range(108)]
nom_note=["a'","ais'","b'","c'","cis'","d'","dis'","e'","f'","fis'","g'","gis'"]*9
sensibilite=0.99




def record():
		w = wave.open('test.wav', 'w')
		w.setnchannels(CHANNELS)
		w.setsampwidth(2)
		w.setframerate(RATE)
		p = pyaudio.PyAudio()




        stream = p.open(format=FORMAT,
                       channels=CHANNELS, 
                       rate=RATE, 
                       input=True,
                       output=True,
                       frames_per_buffer=chunk)

        print("* recording")
        t0=time.time()
        while time.time()-t0<RECORD_SECONDS:
           data = stream.read(chunk)
           a = numpy.fromstring(data, dtype='int16')
           print(numpy.abs(a).mean())
           w.writeframes(data)


def open_file(path):
	op=wave.open(path,'r')
	data=op.readframes(op.getnframes())
	liste_frames=numpy.fromstring(data, dtype='int16')
	return(liste_frames)

def deco_fourier(x):
	fourier=abs(f.fft(x))
	signal_freq=f.fftfreq(x.shape[0],1.0/RATE)
	
	fourier=fourier[0:len(fourier)//2]
	signal_freq=signal_freq[0:len(signal_freq)//2]
	return(signal_freq,fourier)    


def extract_note(signal_freq,Lff):
	m=max(Lff)
	liste_note=[]
	note=m*sensibilite
	freq_max=numpy.shape(Lff)[0]
	for k in range(freq_max-1):
		if Lff[k]>note:
			liste_note.append(signal_freq[k])
	return(liste_note)

def find_note(l):
	accord=[' ']
	for k in l:
		for i in range(60):
			if 2*k>freq_note[i]+freq_note[i-1] and 2*k<freq_note[i]+freq_note[i+1]:
				accord.append(nom_note[i])
	return(accord)



def save_note(Ln):
	partition=open('partition.ly','a')
	partition.write('<<')
	for k in Ln:
		partition.write(' ')
		partition.write(k)
	partition.write('>>')
	partition.close()

def debut():
        partition=open('partition.ly','w')
        a='{ a8 '
        partition.write(a)
        partition.close()

def fin():
        partition=open('partition.ly','a')
        b='}'
        partition.write(b)
        partition.close()

def lire_morceau(path, temps, pulsation):
	morceau=open_file(path)
	s=morceau.shape
	print(s)
	n=s[0]
	longcr=int(n*(60/(pulsation*2)/temps))
	print(longcr)
	print("range",int(n/longcr))
	debut()
	for k in range(int(n/longcr)-1):
		croche=morceau[k*longcr:(k+1)*longcr]
		dc=deco_fourier(croche)
		note=extract_note(dc[0],dc[1])
		accord=find_note(note)
		save_note(accord)
		
	fin()
record()
lire_morceau('test.wav',RECORD_SECONDS,60)

morceau=open_file('test.wav')
L=deco_fourier(morceau)
plt.subplot(121)
plt.plot(L[0],L[1])
plt.subplot(122)
plt.plot([k for k in range(len(morceau))],morceau)
plt.show()
