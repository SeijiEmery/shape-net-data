import numpy as np
import pickle as pkl
import json
import os
import zipfile

def load_json_params_from_zipfile (path, file_ext = '.json'):
    dataset = {}
    print("loading '%s'"%path)
    with zipfile.ZipFile(path, 'r') as zf:        
        for file in zf.namelist():
            if file.endswith(file_ext):
                with zf.open(file, 'r') as f:
                    dataset[file.split('/')[-1].split('.')[0]] = json.loads(f.read())
    return dataset

def process_dataset (zip_file_input, pkl_output, expected_param_length = 6162):
    dataset = load_json_params_from_zipfile(zip_file_input)
    print("got %s entries"%len(dataset))

    dataset_dimensions = set([ len(value) for value in dataset.values() ])
    if expected_param_length not in dataset_dimensions:
        print("invalid expected_param_length, %s not in %s"%(expected_param_length, dataset_dimensions))
    if len(dataset_dimensions) != 1:
        print("warning: dataset has mismatching dimensions: %s (expected %s)"%(
            dataset_dimensions, expected_param_length))

    print(dataset_dimensions)
    non_corrupt_elements = [ value for value in dataset.values() if len(value) == expected_param_length ]
    corrupt_elements     = [ value for value in dataset.values() if len(value) != expected_param_length ]
    keys = [ key for key in dataset.keys() if len(dataset[key]) == expected_param_length ]
    print("have %s corrupt elements with sizes %s"%(len(corrupt_elements), set(map(len, corrupt_elements))))
    print("have %s non-corrupt elements; using those as our dataset"%(len(non_corrupt_elements)))
    print("have %s keys"%(len(keys)))
    data = np.array(non_corrupt_elements)
    print("dataset shape: %s"%(data.shape,))
    
    print("saving as %s"%pkl_output)
    basedir = os.path.split(pkl_output)[0]
    if basedir and not os.path.exists(basedir):
        os.makedirs(basedir)
    with open(pkl_output, 'wb') as f:
        pkl.dump({
            'data': data,
            'keys': keys
        }, f)
    
process_dataset('../output-lv5/output.zip', '../datasets/training-lv5.pkl', 6162)