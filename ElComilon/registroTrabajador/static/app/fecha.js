window.onload = function(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    if(dia<10)
      dia='0'+dia; //agrega cero si el menor de 10
    if(mes<10)
      mes='0'+mes //agrega cero si el menor de 10
    document.getElementById('fechaActual').value=ano+"-"+mes+"-"+dia;

    var horaActual = new Date();
    var hora = horaActual.getHours();
    var minuto = horaActual.getMinutes();
    if(minuto<10)
    minuto='0'+minuto; //agrega cero si el menor de 10
    if(hora<10)
      hora='0'+hora //agrega cero si el menor de 10
    document.getElementById('horaActual').value = hora+":"+minuto;
  }