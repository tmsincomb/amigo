import urllib.parse
import urllib.request
from collections import defaultdict


def gene_id_mapping(query: str = 'Q8NER1 P36544', 
                    from_src: str = 'ACC+ID',  
                    to_src: str = 'P_ENTREZGENEID') -> dict:
    """
    UniProt REST API Gene ID mapper
    
    Parameters
    ----------
    query : str, optional
        [description], by default 'Q8NER1 P36544'
    from_src : str, optional
        [description], by default 'ACC+ID'
    to_src : str, optional
        [description], by default 'P_ENTREZGENEID'

    Returns
    -------
    dict
        [description]
    """
    mapping = defaultdict(list)
    url = 'https://www.uniprot.org/uploadlists/'
    params = {'query': query, 'from': from_src, 'to': to_src, 'format': 'tab'}
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        for line in f.read().splitlines()[1:]:
            f,t = line.decode().split('\t')
            mapping[f].append(t)
    return mapping