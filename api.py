from rauth import OAuth1Session

def search_yelp(location, term='lawyer', limit='6',
                consumer_key='W4FAfHIVPA3cZb8z0QtI7w',
                consumer_secret='ga1UHeL0EcpvM2MzFlTd-kkLnYc',
                access_token='n4dG1spU53Fe_UQ3c8IejRds4IQMr6ds',
                access_token_secret='AW6s7OBGFUS9Z5HF-hjPcF1nFN0'
                ):
    """
    searches yelp for a term at a location (city, state, ...)

    consumer_key, consumer_secret, access_token and access_token_secret can be
    accessed at http://www.yelp.com/developers/getting_started/api_access.
    They are not included for security reasons. 
    """
    path = 'http://api.yelp.com/v2/search'
    params = {'term':term, 'location':location, 'limit':limit}
    session = OAuth1Session(consumer_key, consumer_secret,
                            access_token, access_token_secret)
    return session.get(path, params=params).json()
