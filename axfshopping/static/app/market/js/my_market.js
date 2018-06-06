


$('.addcart').on('click', function (evt) {
    var goods_id = $(evt.target).attr('goodsid')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/addcart/',
        type:'POST',
        data:{'goods_id':goods_id},
        datatype:'json',
        headers:{'X-CSRFToken':csrf},
        success: function (msg) {
          if (msg.code == 200){
              $('#num_'+ goods_id).text(msg.num)
          }else {
              alert(msg.msg)
          }
        },
        error: function (msg) {
            alert('请求失败')
        }
    })
})

$('.subcart').on('click', function (evt) {
    var goods_id = $(evt.target).attr('goodsid')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/subcart/',
        type:'POST',
        data:{'goods_id':goods_id},
        datatype: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            if (msg.code == 200){
                $('#num_'+goods_id).text(msg.num)
            }else {
                alert(msg.msg)
            }
        },
        error: function (msg) {
           alert('请求失败')
        }


    })
})


$('.is_select').on('click', function (evt) {
    var goods_id = $(evt.target).attr('goodsid')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/changeSelectStatus/',
        type:'POST',
        data:{'goods_id':goods_id},
        datatype:'json',
        headers:{'X-CSRFToken':csrf},
        success: function (data) {

            if (data.select_status){
                $(evt.target).text('√')
            }else {
                $(evt.target).text('X')
            }
        },
        error: function () {
            alert('请求失败')
        }
    })
})


// $('#generate_order').on('click',function () {
//     $.get('/axf/generateOrder/', function (data) {
//         if (data.code == 9999){
//             alert(data.msg);
//         }
//     })
// })

// 全选
$('#all_select').on('click', function (evt) {
    var allstatus = $(evt.target).attr('allstatus')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/allSelect/',
        type:'POST',
        data:{'allstatus':allstatus},
        datatype:'json',
        headers:{'X-CSRFToken':csrf},
        success: function (data) {
            if (data.code == 200){
                if (data.allstatus){
                    $('#all_select').text('√');
                    $('.is_select').text('√');
                    $('#all_select').attr('allstatus', 'True');
                }else {
                    $('#all_select').text('X');
                    $('.is_select').text('X');
                    $('#all_select').attr('allstatus', 'False');
                }
            }
        },
        error: function () {
            alert('请求失败')
        }

    })
})