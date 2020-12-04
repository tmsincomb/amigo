import requests as r
import io
from yarl import URL
import pandas as pd


def amigo(queries, species='"Homo sapiens"', verbose=True):
    dfs = []
    for query in queries:
        url = URL(''.join(dict(
            base = 'http://golr-aux.geneontology.io/solr/select?',
            options = f'defType=edismax&qt=standard&indent=on&wt=csv&rows=100000&start=0&fq=taxon_subset_closure_label:{species}&q={query}',
            table = '&fl=source,bioentity_internal_id,bioentity_label,qualifier,annotation_class,reference,evidence_type,evidence_with,aspect,bioentity_name,synonym,type,taxon,date,assigned_by,annotation_extension_class,bioentity_isoform',
            facet = '&facet=true&facet.mincount=1&facet.sort=count&json.nl=arrarr&facet.limit=25&facet.field=aspect&facet.field=taxon_subset_closure_label&facet.field=type&facet.field=evidence_subset_closure_label&facet.field=regulates_closure_label&facet.field=annotation_class_label&facet.field=qualifier&facet.field=annotation_extension_class_closure_label&facet.field=assigned_by&facet.field=panther_family_label',
            misc_dic = '&hl=true&hl.simple.pre=%3Cem%20class=%22hilite%22%3E&hl.snippets=1000&csv.encapsulator=&csv.separator=%09&csv.header=true&csv.mv.separator=%7C&fq=document_category:%22annotation%22',
            qf = '&qf=annotation_class%5E2&qf=annotation_class_label_searchable%5E1&qf=bioentity%5E2&qf=bioentity_label_searchable%5E1&qf=bioentity_name_searchable%5E1&qf=annotation_extension_class%5E2&qf=annotation_extension_class_label_searchable%5E1&qf=reference_searchable%5E1&qf=panther_family_searchable%5E1&qf=panther_family_label_searchable%5E1&qf=bioentity_isoform%5E1&qf=regulates_closure%5E1&qf=regulates_closure_label_searchable%5E1',
        ).values()))
        resp = r.get(url)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text), delimiter='\t')
        df = df.where(df.notnull(), None)
        df['query'] = query
        dfs.append(df)
        if verbose: print(f'=== query - [{query}] - complete ===')
    df = pd.concat(dfs)
    return df