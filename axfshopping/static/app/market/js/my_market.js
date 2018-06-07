


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
          getTotalPrice();
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
                if (msg.num == 0){
                    checkCartZero($('#num_'+goods_id))
                };
                getTotalPrice()
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
            };
            getTotalPrice();
            if (checkAllSelect()){
                    $('#all_select').text('√');
                    $('#all_select').attr('allstatus', 'True');
                }else {
                $('#all_select').text('X');
                    $('#all_select').attr('allstatus', 'False');
            }
        },
        error: function () {
            alert('请求失败')
        }
    })
})


$('#generate_order').on('click',function () {
    $.get('/axf/generateOrder/', function (data) {
        if (data.code == 9999){
            alert(data.msg);
        }else{
            location.href = '/axf/waitPayToPayed/?order_id='+data.order_id
        }
    })
})

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
                getTotalPrice()
            }
        },
        error: function () {
            alert('请求失败')
        }

    })
})

// 付款
$('#userpay').on('click', function (evt) {
    var order_id = $('#userpay').attr('orderid');
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/axf/changeOrderStatus/',
        type:'POST',
        data:{'order_id':order_id},
        datatype:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (data) {
            if (data.code == '200'){
                location.href = '/axf/mine/'
            }
        },
        error:function (data) {
            alert('支付失败')
        }
    })

})

// 检查是否全选
function checkAllSelect() {
    var allSelect = true;
    var allgoodsStatus = $('.is_select')
    for (var i=0;i<allgoodsStatus.length;i+=1){
        if (allgoodsStatus[i].textContent == 'X'){
            allSelect = false;
        }
    }
    return allSelect
}

//  检查购物车中商品数量是否为0
function checkCartZero(elem) {
    if (elem.parent().parent().attr('class')=='menuList'){
        elem.parent().parent().remove()
    }
}

// 获取总价
function getTotalPrice() {
    $.get('/axf/getTotalPrice/', function (data) {
        if (data.code == 200){
            $('#total').text(data.total)
        }
    })
}

getTotalPrice()