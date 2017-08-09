from repository import models

class Basic(object):
    def __init__(self):
        pass


    @classmethod
    def initial(cls):
        return cls()

    def process(self,server_info,hostname,server_obj):
        print('start')
        # ############### 处理基础信息 ##################

        new_basic_dict = server_info['basic']['data']

        old_basic_dict = models.Server.objects.filter(hostname=hostname).values('os_platform','os_version','hostname').first()


        if not old_basic_dict==new_basic_dict:


            models.Server.objects.filter(hostname=hostname).update(**new_basic_dict)

            # ############ 更新 ############

            record_list = []
            row_map = {'os_platform': '系统', 'os_version': '系统版本', 'hostname': 'CPU型号'}


            for k, v in new_basic_dict.items():

                print(k,v)
                value = old_basic_dict[k]
                if v != value:
                    record_list.append("%s,%s由%s变更为%s" % (hostname, row_map[k], value, v,))

            if record_list:
                content = ";".join(record_list)
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)



