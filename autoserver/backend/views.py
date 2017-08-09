import json
from django.shortcuts import render,HttpResponse,redirect
from repository import models





def curd(request):
    print('curd')
    # v = models.Server.objects.all()
    return render(request,'curd.html')

def curd_json(request):
    print('curd_json')
    # v = models.Server.objects.all()
    # 序列化操作 1
    # from django.core import serializers
    # data = serializers.serialize('json',v)


    # 序列化操作 2


    table_config = [

        {
            'q': None,        # 去 数据库查询的字段
            'title': '选择',   # 显示的 标签
            'display': True,  # 是否显示
            'text': {
                'tpl': '<input type="checkbox" values="{n1}">',
                'kwargs': {'n1': '@id'}
            },
            'attrs': {'nid':'@id'}
        },

        {
            'q':'id',
            'title':'ID',
            'display':False,
            'text':{
                'tpl':'{n1}-{n2}',
                'kwargs':{'n1':'@id','n2':'ddd'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },

        {
            'q':'hostname',
            'title':'主机名',
            'display': True,
            'text':{
                'tpl':'d{n1}',
                'kwargs':{'n1':'@hostname'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':'create_at',
            'title':'时间',
            'display': False,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@create_at'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':'asset__cabinet_num',
            'title':'机柜号',
            'display': True,
            'text':{
                'tpl':'BJ-{n1}',
                'kwargs':{'n1':'@asset__cabinet_num'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':'asset__cabinet_order',
            'title':'序号',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@asset__cabinet_order'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':'asset__idc__name',
            'title':'IDC机房',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@asset__idc__name'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':'asset__business_unit__name',
            'title':'业务线',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@asset__business_unit__name'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        },
        {
            'q':None,
            'title':'操作',
            'display': True,
            'text':{
                'tpl':'<a href="/del?nid={nid}">删除</a>',
                'kwargs':{'nid':'@id'}
            },
            'attrs': {'k1': 'v1','k2':'@hostname'}
        }

    ]





    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])


    from datetime import datetime
    from datetime import date

    # 序列化时间
    class JsonCustomEncoder(json.JSONEncoder):

        def default(self, value):

            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, value)

    v = models.Server.objects.values(*values_list)

    print('server_list',v)
    print('table_config',table_config)

    ret = {
        'server_list':list(v),
        'table_config':table_config
    }



    return HttpResponse(json.dumps(ret,cls=JsonCustomEncoder))







def asset(request):
    print('asset')
    # v = models.Server.objects.all()
    return render(request,'asset.html')


def asset_json(request):





    table_config = [
        {
            'q':'id',
            'title':'ID',
            'display':False,
            'text':{
                'tpl':'{n1}-{n2}',
                'kwargs':{'n1':'@id','n2':'ddd',},
            },
            'attrs': {'k1': 'v1','k2':'@id'}

        },

        {
            'q':'cabinet_num',
            'title':'机柜号',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@cabinet_num'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}


        },
        {
            'q':'device_type_id',
            'title':'资产类型',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@@device_type_choices'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },
        {
            'q':'device_status_id',
            'title':'状态',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@@device_status_choices'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },
        {
            'q':'cabinet_order',
            'title':'序号',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@cabinet_order'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },
        {
            'q':'idc__name',
            'title':'IDC',
            'display': True,
            'text':{
                'tpl':'BJ-{n1}',
                'kwargs':{'n1':'@idc__name'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },
        {
            'q':'business_unit__name',
            'title':'业务线号',
            'display': True,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@business_unit__name'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },
        {
            'q':'create_at',
            'title':'时间',
            'display': False,
            'text':{
                'tpl':'{n1}',
                'kwargs':{'n1':'@create_at'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },

        {
            'q':None,
            'title':'操作',
            'display': True,
            'text':{
                'tpl':'<a href="/del?nid={nid}">删除</a>',
                'kwargs':{'nid':'@id'}
            },
            'attrs': {'k1': 'v1','k2':'@id'}
        },

    ]





    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])


    from datetime import datetime
    from datetime import date

    # 序列化时间
    class JsonCustomEncoder(json.JSONEncoder):

        def default(self, value):

            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, value)

    v = models.Asset.objects.values(*values_list)

    print('server_list',v)
    print('table_config',table_config)

    ret = {
        'server_list':list(v),
        'table_config':table_config,
        'global_dict':{
            'device_type_choices': models.Asset.device_type_choices,
            'device_status_choices': models.Asset.device_status_choices
        }
    }



    return HttpResponse(json.dumps(ret,cls=JsonCustomEncoder))

