
function fetchdata_perf()
{

    //var SicaklikKayit = 37 + Math.floor(Math.random() * 15);

    $.ajax({        
              url: 'tempList',
              type: 'POST',
            //   type: 'GET',
              data:{

              //SicaklikKayit:SicaklikKayit,
              csrfmiddlewaretoken: '{{ csrf_token }}',
              dataType: "json",

              },
              success: function(response){
              $('#temperature_ajax').html(response);
              },
                              failure: function() {
                          alert("ajax reverse fail geldi");
                            }               
          });
  }
  $(document).ready(fetchdata_perf()) // sayfa manuel refresh yapıldığında 60 saniye beklemeden ilk kayıdı yapabilmek için. 
                                      //Birden fazla pencerede dashboard açılırsa otomatik 1den fazla kayıt yapılmış olur,hatalı işleme denk gelir.
  $(document).ready(function(){
    setInterval(fetchdata_perf,20000);
    });