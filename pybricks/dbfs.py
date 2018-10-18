from .session import Session

class DBFS(object):

    def __init__(self, **kwargs):
        self.__session = Session(**kwargs)

    def ls(self, path='/'):
        params = {'path':path}
        return self.__session.perform_query('get','dbfs/list', params)['files']

    def get_status(self, path='/'):
        params = {'path':path}
        return self.__session.perform_query('get','dbfs/get-status', params)
