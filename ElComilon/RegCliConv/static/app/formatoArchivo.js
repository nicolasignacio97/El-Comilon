function checkfile(sender) {
    var validExts = new Array(".xlsx", ".xls", ".csv");
    var fileExt = sender.value;
    fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
    if (validExts.indexOf(fileExt) < 0) {
        Swal.fire({
          icon: 'error',
          title: 'Formato inválido',
          text: 'Por favor selecciona un formato'+ validExts.toString() + " types."
        })
        document.getElementById('arch').value = '';
      return false;
    }
    else return true;
}
