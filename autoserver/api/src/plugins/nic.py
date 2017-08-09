from repository import models

class Nic(object):
    def __init__(self):
        pass


    @classmethod
    def initial(cls):
        return cls()

    def process(self,server_info,hostname,server_obj):
        print('start')
        # ############### 处理硬盘信息 ##################

        new_nic_dict = server_info['nic']['data']

        old_nic_list = models.NIC.objects.filter(server_obj=server_obj)


        # 交集：5, 创建：3,删除4;
        new_name_list = list(new_nic_dict.keys())

        old_name_list = []
        for item in old_nic_list:
            old_name_list.append(item.name)

        # 交集：更新[5,]
        update_list = set(new_name_list).intersection(old_name_list)
        # 差集: 创建[3]
        create_list = set(new_name_list).difference(old_name_list)
        # 差集: 删除[4]
        del_list = set(old_name_list).difference(new_name_list)




        if del_list:
            # 删除
            models.NIC.objects.filter(server_obj=server_obj, name__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除网卡：%s" % ("、".join(del_list),))

        # 增加、
        record_list = []
        for name in create_list:
            nic_dict = new_nic_dict[name]
            nic_dict['name'] = name
            nic_dict['server_obj'] = server_obj
            models.NIC.objects.create(**nic_dict)


            temp = "新增网卡name:{name},up:{up},hwaddr:{hwaddr},ipaddrs:{ipaddrs},netmask:{netmask}".format(**nic_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'netmask': 'netmask', 'hwaddr': '网卡mac地址', 'ipaddrs': 'ip地址','name':'n姓名'}

        for name in update_list:
            new_nic_row = new_nic_dict[name]
            ol_nic_row = models.NIC.objects.filter(name=name, server_obj=server_obj).first()

            for k, v in new_nic_row.items():

                value = getattr(ol_nic_row, k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" % (name, row_map[k], value, v,))
                    setattr(ol_nic_row, k, v)
            ol_nic_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

