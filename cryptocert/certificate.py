import json, hashlib

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def load(path):
    with open(path,encoding='utf8') as f:return json.load(f)
