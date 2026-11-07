import soundfile as sf, numpy as np, json
from kokoro_onnx import Kokoro
k=Kokoro("models/kokoro.onnx","models/voices.bin")
lines=[
 "Nepal's clocks run five hours and forty-five minutes ahead of world time.",
 "That's fifteen minutes ahead of India, right next door.",
 "So why such an odd number? The answer is a mountain.",
 "Nepal set its time by the sun over Gauri Shankar, a sacred peak east of Kathmandu, near eighty-six and a quarter degrees east.",
 "Every degree east adds four minutes to the clock. Eighty-six and a quarter, times four, is exactly five hours and forty-five minutes.",
 "A country that tells time by its mountains.",
]
out=[];t=0;times=[];sr=24000
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="bm_george",speed=1.0,lang="en-gb")
    gap=np.zeros(int(sr*0.45),dtype=a.dtype)
    times.append((round(t,2),round(t+len(a)/sr,2)))
    out+= [a,gap]; t+= (len(a)+len(gap))/sr
sf.write("voice.wav",np.concatenate(out),sr)
json.dump(times,open("times.json","w"));print(times, round(t,2))
