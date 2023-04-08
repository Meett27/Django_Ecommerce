// Add to cart
    $(document).on("click",".add-to-cart", function(){
        var _id=$("#productId")
        var _qty=$("#productQuantity").val()
        var _title=$("#productTitle").val()
        var _price=$("#productPrice").val()
        var _category=$("#productCategory").val()
        var _subCategory=$("#productSubCategory").val()
        var _brand=$("#productBrand").val()
        console.log(_id,_title,_brand,_category,_subCategory,_price,_qty)
        // $.ajax({
        //     url:'/add-to-cart',
        //     data:{
        //         'id':_productId,
        //         'image':_productImage,
        //         'qty':_qty,
        //         'title':_productTitle,
        //         'price':_productPrice
        //     },
        //     dataType:'json',
        //     beforeSend:function(){
        //         _vm.attr('disabled',true);
        //     },
        //     success:function(res){
        //         $(".cart-list").text(res.totalitems);
        //         _vm.attr('disabled',false);
        //     }
        // });
        
    });


// 