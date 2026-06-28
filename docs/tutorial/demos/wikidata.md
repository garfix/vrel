# Wikidata

Wikidata is a huge database that contains structured information from Wikipedia, as well as other information.

Clone the repository to view and run the demo. The code can be found in `tests/integration/Wikidata_test.py`

The endpoint is accessed via HTTP, so we need the `requests` library

~~~bash
pip install requests
~~~

The Wikidata is just a simple proof-of-concept with a dialog that consists of a single sentence.

## Too many requests

Wikidata requires that you send a User-Agent header to identify yourself. Without it, the service quickly responds with "too many requests".

Even with the header, it's good practise not to create too many queries, and since a single request may produce hundreds of calls to the SPARQL endpoint, it may be wise to cache the results of the endpoint.


