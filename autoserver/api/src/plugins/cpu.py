from repository import models

class Cpu(object):
    def __init__(self):
        pass


    @classmethod
    def initial(cls):
        """
        预留钩子
        :return: 
        """
        return cls()


    def process(self,server_info,hostname,server_obj):
        print('start')
        # ############### 处理CPU信息 ##################

        new_cpu_dict = server_info['cpu']['data']

        old_cpu_dict = models.Server.objects.filter(hostname=hostname).values('cpu_count','cpu_physical_count','cpu_model').first()
        if not new_cpu_dict==old_cpu_dict:

            models.Server.objects.filter(hostname=hostname).update(**new_cpu_dict)

            # ############ 更新 ############

            record_list = []
            row_map = {'cpu_count': 'CPU个数', 'cpu_physical_count': 'CPU物理个数', 'cpu_model': 'CPU型号'}


            for k, v in new_cpu_dict.items():

                print(k,v)
                value = old_cpu_dict[k]
                if v != value:
                    record_list.append("%s,%s由%s变更为%s" % (hostname, row_map[k], value, v,))

            if record_list:
                content = ";".join(record_list)
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)



