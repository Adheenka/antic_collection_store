$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/plus_wishliste",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = 'http://localhost:8000/proDetail/${id}
        }
    })
})
$('.minus-wishliste').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/mius_wishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = 'http://localhost:8000/proDetail/${id}
        }
    })
})