from repository import models

class Board(object):
    def __init__(self):
        pass


    @classmethod
    def initial(cls):
        return cls()

    def process(self,server_info,hostname,server_obj):
        print('start')
        # ############### 处理主板信息 ##################

        new_board_dict = server_info['board']['data']

        old_board_dict = models.Server.objects.filter(hostname=hostname).values('manufacturer','model','sn').first()
        if not new_board_dict==old_board_dict:
            models.Server.objects.filter(hostname=hostname).update(**new_board_dict)


            # ############ 更新 ############

            record_list = []
            row_map = {'manufacturer': '制造商', 'model': '型号', 'sn': 'SN号'}


            for k, v in new_board_dict.items():

                print(k,v)
                value = old_board_dict[k]
                if v != value:
                    record_list.append("%s,%s由%s变更为%s" % (hostname, row_map[k], value, v,))

            if record_list:
                content = ";".join(record_list)
                models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

