import pytest
import json
import pkg_resources
import requests

PROD_API_URL = 'https://openpredict.semanticscience.org'

def test_get_predict():
    """Test predict API GET operation"""
    # url = PROD_API_URL + '/predict?drug_id=DRUGBANK:DB00394&model_id=openpredict-baseline-omim-drugbank&n_results=42'
    get_predictions = requests.get(PROD_API_URL + '/predict',
                        params={
                            'drug_id': 'DRUGBANK:DB00394',
                            'n_results': '42',
                            'model_id': 'openpredict-baseline-omim-drugbank'
                        }).json()
    assert 'hits' in get_predictions
    assert len(get_predictions['hits']) == 42
    assert get_predictions['count'] == 42
    assert get_predictions['hits'][0]['id'] == 'OMIM:246300'

# TODO: add tests using a TRAPI validation API if possible?
def test_post_trapi():
    """Test Translator ReasonerAPI query POST operation to get predictions"""
    headers = {'Content-type': 'application/json'}
    tests_list = [
        {'limit': 3, 'class': 'drug'},
        {'limit': 'no', 'class': 'drug'},
        {'limit': 3, 'class': 'disease'},
        {'limit': 'no', 'class': 'disease'},
    ]
    for trapi_test in tests_list:
        trapi_filename = 'trapi_' + trapi_test['class'] + '_limit' + str(trapi_test['limit']) + '.json'
        with open(pkg_resources.resource_filename('tests', 'queries/' + trapi_filename),'r') as f:
            trapi_query = f.read()
            trapi_results = requests.post(PROD_API_URL + '/query',
                        data=trapi_query, headers=headers).json()
            edges = trapi_results['knowledge_graph']['edges'].items()

            if trapi_test['limit'] == 'no':
                assert len(edges) >= 300
            else:
                assert len(edges) == trapi_test['limit']



# TODO: Check for this edge structure:
#   "knowledge_graph": {
#     "edges": {
#       "e0": {
#         "attributes": [
#           {
#             "name": "model_id",
#             "source": "OpenPredict",
#             "type": "EDAM:data_1048",
#             "value": "openpredict-baseline-omim-drugbank"
#           },
#           {
#             "name": "score",
#             "source": "OpenPredict",
#             "type": "EDAM:data_0951",
#             "value": "0.8267106697312154"
#           }
#         ],
#         "object": "DRUGBANK:DB00394",
#         "predicate": "biolink:treated_by",
#         "relation": "RO:0002434",
#         "subject": "OMIM:246300"
#       },