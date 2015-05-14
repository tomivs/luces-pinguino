var form = document.getElementById("form-bombillo");

$("#bombillo").click(function () {
   estado = $('#estado').val();
   if (estado == 'si')
   {
      $('#estado').val('no');
   }
   else if(estado == 'no')
   {
      $('#estado').val('si');
   }
   else
   {
      $('#estado').val('no');
   }
   
   $.post( "/ajax/", $( "#formbombillo" ).serialize() , function( data ) {
      if(data.trim()*1)
         $("#bombillo").attr("src", img_on);
      else
         $("#bombillo").attr("src", img_off);
   });
});
