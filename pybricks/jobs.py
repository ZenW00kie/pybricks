from .session import Session

class Job(object):

    def __init__(self, **kwargs):
        self.__session = Session(**kwargs)

    def create(self,
               name,
               size='r3.xlarge',
               spark_version='4.1.x-scala2.11',
               autoscale=(1,2),
               cli_params=None,
               cluster_kwargs={},
               job_kwargs={}):
        """
        kwargs: https://docs.databricks.com/api/latest/jobs.html#create
        """
        cluster_params = {
            "cluster_name": name + '_jobcluster',
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
        cluster_params = {**cluster_params, **cluster_kwargs}
        config = {
            'name':name,
            'new_cluster':cluster_params,
            'spark_python_task':{'python_file':path, 'parameters':cli_params},
            }
        config = {**config, **job_kwargs}
        return self.__session.perform_query('post', 'jobs/create', config)


    def list_jobs(self, user=None):
        response = self.__session.perform_query('get', 'jobs/list')
        j = [{'job_id':resp['job_id'],
              'name':resp['settings']['name'],
              'user':resp['creator_user_name']}
             for resp in response['jobs']]
        if user:
            return [i for i in j if i['user'] == user]
        else:
            return j

    def delete(self, job_id):
        config = {'job_id':job_id}
        return self.__session.perform_query('post', 'jobs/delete', config)

    def get(self, job_id):
        config = {'job_id':job_id}
        return self.__session.perform_query('post', 'jobs/get', config)

    def reset(self, job_id, new_settings={}, **kwargs):
        config = {'job_id':job_id, 'new_settings': new_settings, **kwargs}
        return self.__session.perform_query('post', 'jobs/reset', config)

    def run_job(self, job_id, params=[], params_type=None):
        config = {'job_id':job_id}
        if params_type:
            config[params_type] = params
        return self.__session.perform_query('post', 'jobs/run-now', config)

    def run(self,
            name=None,
            cluster='new',
            size='r3.xlarge',
            spark_version='4.1.x-scala2.11',
            availability='SPOT',
            autoscale=(1,2),
            task_type='spark_python_task',
            cli_params=None,
            cluster_config={},
            job_kwargs={}):
        """
        cluster either 'new' or cluster_id as int
        """
        config = {'run_name':name}
        if cluster == 'new':
            config['new_cluster'] = {
                "spark_version": spark_version,
                "node_type_id": size,
                "spark_version": spark_version,
                "node_type_id": size,
                "spark_conf": {
                    "spark.speculation": True
                    },
                "aws_attributes": {
                    "availability": availability
                    },
                "autoscale": {'min_workers':autoscale[0],
                              'max_workers':autoscale[1]},
                **cluster_config
            }
        else:
            config['existing_cluster_id'] = cluster
        if task_type == 'spark_python_task':
            config[task_type] = {'python_file':path, 'parameters':cli_params}
        elif task_type == 'notebook_task':
            config[task_type] = {'notebook_path':path,
                                 'base_parameters':cli_params}
        config = {**config, **job_kwargs}
        return self.__session.perform_query('post', 'jobs/runs/submit', config)
