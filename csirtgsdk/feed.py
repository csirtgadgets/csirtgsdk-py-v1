
class Feed(object):
    """
    Represents a Feed Object
    """
    def __init__(self, client):
        self.client = client

    def new(self, user, name, description=None):
        """
        Creates a new Feed object

        :param user: feed username
        :param name: feed name
        :param description: feed description
        :return: dict
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)

        data = {
            'feed': {
                'name': name,
                'description': description
            }
        }

        body = self.client.post(uri, data)
        if body.get('feed'):
            return body['feed']

        return body

    def remove(self, user, name):
        """
        Removes a feed

        :param user: feed username
        :param name: feed name
        :return: true/false
        """

        uri = self.client.remote + '/users/{}/feeds/{}'.format(user, name)

        body = self.client.session.delete(uri)
        return body.status_code


    def index(self, user):
        """
        Returns a list of Feeds from the API

        :param user: feed username
        :return: list

        Example:
            ret = feed.index('csirtgadgets')
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)
        return self.client.get(uri)

    def show(self, user, name, limit=None, lasttime=None):
        """
        Returns a specific Feed from the API

        :param user: feed username
        :param name: feed name
        :param limit: limit the results
        :param lasttime: only show >= lasttime
        :return: dict

        Example:
            ret = feed.show('csirtgadgets', 'port-scanners', limit=5)
        """
        uri = self.client.remote + '/users/{0}/feeds/{1}'.format(user, name)
        return self.client.get(uri, params={'limit': limit, 'lasttime': lasttime})
