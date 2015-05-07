var form = document.getElementById("form-bombillo");

document.getElementById("bombillo").addEventListener("click", function () {
   estado = $('.estado').val();
   if (estado == 'si')
   {
      $('.estado').val('no');
   }
   else if(estado == 'no')
   {
      $('.estado').val('si');
   }
   else
   {
      $('.estado').val('no');
   }
   form.submit();
});
