import matplotlib.pyplot as plt
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
from matplotlib import cm
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

path = "Audio_Files/Audio"
files = os.listdir(path)

for i in range(len(files)):
    files[i] = f"{path}/{files[i]}"

embeds = []
for file in files:
    fpath = Path(file)
    wav = preprocess_wav(fpath)

    enc = VoiceEncoder()
    embeds.append(enc.embed_utterance(wav))

for i in range(len(embeds)):
    embed = embeds[i]
    height = int(np.sqrt(len(embed)))
    shape = (height, -1)
    embed = embed.reshape(shape)

    cmap = cm.get_cmap()
    mappable = plt.imshow(embed, cmap=cmap)
    cbar = plt.colorbar(mappable, fraction=0.046, pad=0.04)
    plt.title(f"{files[i]}")
    plt.savefig(f"HeatMaps/{i}")
    plt.close()
