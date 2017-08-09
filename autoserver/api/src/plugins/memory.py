from repository import models

class Memory(object):
    def __init__(self):
        pass


    @classmethod
    def initial(cls):
        return cls()

    def process(self,server_info,hostname,server_obj):
        print('start')
        # ############### 处理内存信息 ##################

        new_memory_dict = server_info['memory']['data']

        old_memory_list = models.Memory.objects.filter(server_obj=server_obj)

        # 交集：5, 创建：3,删除4;
        new_slot_list = list(new_memory_dict.keys())

        old_slot_list = []
        for item in old_memory_list:
            old_slot_list.append(item.slot)

        # 交集：更新[5,]
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集: 创建[3]
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集: 创建[4]
        del_list = set(old_slot_list).difference(new_slot_list)


        if del_list:
            # 删除
            models.Memory.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除内存：%s" % ("、".join(del_list),))

        # 增加、
        record_list = []
        for slot in create_list:
            memory_dict = new_memory_dict[slot]
            memory_dict['server_obj'] = server_obj
            models.Memory.objects.create(**memory_dict)
            temp = "新增内存:位置{slot},容量{capacity},型号:{model},speed:{speed},manufacturer:{manufacturer},sn:{sn}".format(**memory_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'capacity': '容量', 'speed': '类型', 'model': '型号'}
        print(update_list)
        for slot in update_list:
            new_memory_row = new_memory_dict[slot]
            ol_memory_row = models.Memory.objects.filter(slot=slot, server_obj=server_obj).first()
            for k, v in new_memory_row.items():

                value = getattr(ol_memory_row, k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" % (slot, row_map[k], value, v,))
                    setattr(ol_memory_row, k, v)
            ol_memory_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

