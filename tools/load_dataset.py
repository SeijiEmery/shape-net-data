from urllib.request import urlopen
import os

urlcache = {}
def load_dataset(path):
    file = os.path.split(path)[1]
    if os.path.exists(file):
        print("loading cached '%s'"%file)
        with open(file, 'rb') as f:
            return f.read()

    if path.startswith('https://'):
        print("fetching %s..."%path)
        data = urlopen(path).read()
        print("done; caching locally as '%s'"%file)
        with open(file, 'wb') as f:
            f.write(data)
        return data

load_dataset('https://raw.githubusercontent.com/SeijiEmery/shape-net-data/master/datasets/training-lv5.pkl')
