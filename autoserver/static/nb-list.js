/**
 * Created by summer on 2017/8/3.
 */

(function (jq) {

    var GLOBAL_DICT = {};

    String.prototype.format = function (args) {
    return this.replace(/\{(\w+)\}/g, function (s, i) {
        return args[i];
    });
};

    function initial(url) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType:'JSON',
        success:function (arg) {
            $.each(arg.global_dict,function (k,v) {
                GLOBAL_DICT[k] = v
            });

            initialHeader(arg.table_config);
            initialBody(arg.server_list,arg.table_config);
        }
    })

}

    function initialHeader(table_config) {
    $.each(table_config,function (k,v) {
        if (v.display){
            var tag = document.createElement('th');
            tag.innerHTML = v.title;
            $('#tbHead').find('tr').append(tag);

        }



    })

}

    function initialBody(server_list,table_config) {
    $.each(server_list,function (k,row) {
        var tr = document.createElement('tr');
        $.each(table_config,function (kk,vv) {
            if (vv.display){
                var td = document.createElement('td');
                /*
                if (vv.q){
                    td.innerHTML = row[vv.q];

                }else {
                    td.innerHTML = vv.text;
                }
                */
                var newKwargs = {};
                $.each(vv.text.kwargs,function (kkk,vvv) {
                    var av = vvv;
                    if (vvv.substring(0,2) == '@@'){
                        var nid = row[vv.q];
                        $.each(GLOBAL_DICT[vvv.substring(2,vvv.length)],function (gk,gv) {
                           if (gv[0]==nid){
                               av = gv[1]
                           }
                        });
                    }
                    else if (vvv[0] == '@'){
                        av = row[vvv.substring(1,vvv.length)]
                    }
                    newKwargs[kkk] = av
                });
                var newText = vv.text.tpl.format(newKwargs);
                td.innerHTML = newText;

                $.each(vv.attrs,function (atkey,atval) {
                    if (atval[0] == '@'){
                        td.setAttribute(atkey,row[atval.substring(1,atval.length)])
                    }else{
                        td.setAttribute(atkey,atval)
                    }


                    
                });



                $(tr).append(td);

            }

        });
        $('#tbBody').append(tr);
    })

}

    function trIntoEdit($tr) {
            console.log($tr)
    }

    jq.extend({
        xx:function (url) {
            initial(url);



            $('#tbBody').on('click',':checkbox',function () {
                var $tr = $(this).parent().parent();
                if ($(this).prop('checked')){
                    // 进入编辑模式
                    trIntoEdit($tr)


            }
        })
        }



    })


})(jQuery);