from urllib.request import urlopen
import pickle as pkl
import os

urlcache = {}
def load_dataset(path):
    file = os.path.split(path)[1]
    if os.path.exists(file):
        print("loading cached '%s'"%file)
        with open(file, 'rb') as f:
            return pkl.load(f)

    if path.startswith('https://'):
        print("fetching %s..."%path)
        data = urlopen(path).read()
        print("done; caching locally as '%s'"%file)
        with open(file, 'wb') as f:
            f.write(data)
        return pkl.loads(data)

dataset = load_dataset('https://raw.githubusercontent.com/SeijiEmery/shape-net-data/master/datasets/training-lv5.pkl')
print("keys:\n%s"%(dataset['keys'],))
print("shape: %s"%(dataset['data'].shape,))
