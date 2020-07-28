import librosa
import json
import gc
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)



def analyze():
    begin = 3735
    end = 4516
    source_file=open("./statistics3735-4515.json", encoding='utf-8')
    json_str = source_file.read()
    json_list = json.loads(json_str)
    for i,json_dict in zip(range(begin,end),json_list):
        path = './music3735-4515/music'+str(i)+".mp3"
        y, sr = librosa.load(path, sr=None)
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        roll_off = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        zero_crossings = np.mean(librosa.feature.zero_crossing_rate(y))
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        json_dict['tempo'] = tempo[0]
        json_dict['centroid'] = centroid
        json_dict['roll_off'] = roll_off
        json_dict['zero_crossings'] = zero_crossings
        del tempo
        del centroid
        del roll_off
        del zero_crossings
        gc.collect()
        json_str = json.dumps(json_dict, cls=MyEncoder, indent=4, sort_keys=True, ensure_ascii=False)
        with open('./Astatistics3735-4515.json', 'a', encoding='utf-8', newline=None) as json_file:
            json_file.write('\n' + json_str + ',')
    source_file.close()

if __name__=='__main__':
    analyze()