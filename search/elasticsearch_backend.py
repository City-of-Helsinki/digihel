from wagtail.wagtailsearch.backends.elasticsearch import ElasticSearch as WagtailElasticSearch


class ElasticSearch(WagtailElasticSearch):
    def __init__(self, params):
        # Use voikko for tokenizing
        conf = self.settings['settings']['analysis']
        voikko_analyzer = {
            'tokenizer': 'finnish',
            'filter': ['lowercase', 'voikko_filter']
        }
        voikko_filter = {
            'type': 'voikko',
            'dictionaryPath': '/usr/lib/voikko',
            'language': 'fi_FI-x-morphoid'
        }
        conf['analyzer']['default'] = voikko_analyzer
        conf['filter']['voikko_filter'] = voikko_filter
        super().__init__(params)

SearchBackend = ElasticSearch
