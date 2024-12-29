$(".btn-remove").click(function() {
	var id = $(this).attr("pid").toString();
    eml= this;
	console.log(id);
    $.ajax({

        type: "GET",
        url: "/removecart",
        data: {
            product_id: id
        },
        success: function(data) {
            
          document.getElementById('amount').innerText = data.amount;
          document.getElementById('totalamount').innerText = data.totalamount;
          eml.parentNode.parentNode.remove();
          


          
            
        }

    })
})
