$(function () {

    // 解析表字段
    $("#checkTblName").click(function () {
        $.ajax({
            type: "get",
            url: '/tool/createApi/getCols?db=' + $('#db').val() + '&tblName=' + $('#tblName').val(),
            async: true,
            dataType: "html",//返回整合HTML
            success: function (data) {
                $("#reqCol").html(data);//刷新整个body页面的html
                $("#repCol").html(data);//刷新整个body页面的html
            }
        })

    });

    // function getFormData($form) {
    //     var unindexed_array = $form.serializeArray();
    //     var indexed_array = {};
    //
    //     $.map(unindexed_array, function (n, i) {
    //         indexed_array[n['name']] = n['value'];
    //     });
    //
    //     return indexed_array;
    // }
    //
    // 生成文档
    $("#handleCols").click(function () {

        // var data = $('form').serialize();
        // for(var dom in $('[name]')){
        //     data[$(dom).attr("name")]=$(dom).val();
        // }
        // console.info(data);

        $(".ischecked").each(function () {

            if (!($(this).prop("checked"))) {
                // $(this).value = "0";
                // $(this).next().attr('value', 0);
                $(this).next().prop('value', 0);
            }
            else {
                // $(this).value = "1";
                //  $(this).next().attr('value', 1);
                $(this).next().prop('value', 1);
            }
            // $(this).prop("checked",true);

        });

        // $("#form").submit();
        $.post(
            $("#form").attr('action'),
            $("#form").serialize(),
            function (res) {
                // $("#api").html(res);//刷新整个body页面的html
                //alert(res.data);
                // window.open().location = "/tool/createApi/download?path=" + res.data;
                var link = document.createElement('a');
                // link.setAttribute("download", $(this).attr("data-name"));
                link.setAttribute("download", res.data.fileName);
                link.href = "/tool/createApi/download?path=" + res.data.url;
                link.click();
            }
        );

        // $.post($("#form").attr('action'),
        //     $("#form").serialize(),
        //     function (res) {
        //         $("#api").html(res);//刷新整个body页面的html
        //
        //     }, "html");

        // $.ajax({
        //     type: "post",
        //     url: '/tool/createApi/handleCols',
        //     async: true,
        //     contentType: "application/json; charset=utf-8",
        //     data: new FormData($('#form')[0]),
        //     // dataType: "json",
        //     success: function (data) {
        //         // $("#reqCol").html(data);//刷新整个body页面的html
        //         $("#api").html(data);//刷新整个body页面的html
        //     }
        // })

    });


});
