import importlib
from repository import models

class PluginManager(object):

    def __init__(self,server_info,hostname,server_obj):
        self.hostname = hostname
        self.server_info = server_info
        self.server_obj = server_obj



    def exec_plugin(self):

        for k,v in  self.server_info.items():
            print(k,v)

            m = importlib.import_module('api.src.plugins.'+k)
            cls = getattr(m,k.capitalize())


            if hasattr(cls, 'initial'):
                obj = cls.initial()
            else:
                obj = cls()

            if not self.server_info[k]['status']:
                models.ErrorLog.objects.create(content=self.server_info[k]['data'], asset_obj=self.server_obj.asset,
                                               title='【%s】%s采集错误信息' % (self.hostname,k))

            else:
                obj.process(self.server_info,self.hostname,self.server_obj)
