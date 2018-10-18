from .session import Session

class Cluster(object):

    def __init__(self, **kwargs):
        self.__session = Session(**kwargs)

    def create(self,
               name,
               size='r3.xlarge',
               spark_version='4.1.x-scala2.11',
               autoscale=(1,2),
               **kwargs):
        config = {
            "cluster_name": name,
            "spark_version": spark_version,
            "node_type_id": size,
            "spark_conf": {
                "spark.speculation": True
                },
            "aws_attributes": {
                "availability": "SPOT",
                "zone_id": "us-west-2a"
                },
            "autoscale": {'min_workers':autoscale[0],'max_workers':autoscale[1]}
            }
        config = {**config, **kwargs}
        response = self.__session.perform_query('post','clusters/create',config)
        if response.status_code == 200:
            return response['cluster_id']
        else:
            print("Error launching cluster: %s: %s" %
                  (response["error_code"], response["message"]))

    def list_clusters(self, user=None):
        response = self.__session.perform_query('get', 'clusters/list')
        c = [resp['default_tags'] for resp in response['clusters']]
        if user:
            return [i for i in c if i['Creator'] == user]
        else:
            return c

    def cluster_state(self, state, cluster_id):
        """
        Methods: start, restart, delete (terminate), permanent-delete
        """
        return self.__session.perform_query('post',
                                            'clusters/%s' % state,
                                            {'cluster_id':cluster_id})

    def resize(self, cluster_id, workers=None, auto_scale=None):
        config = {'cluster_id':cluster_id}
        if workers:
            config['num_workers'] = workers
        elif auto_scale:
            config['autoscale'] = auto_scale
        else:
            raise TypeError('resize() missing argument workers or auto_scale')
        return self.__session.perform_query('post','clusters/resize', config)
