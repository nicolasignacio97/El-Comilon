document.getElementById('file').onchange=function(e){
    let reader=new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload=function(){
        let preview=document.getElementById('preview');
        image=document.createElement('img');
        image.src=reader.result;
        preview.innerHTML='';
        preview.append(image);
        /*let url = document.getElementById('file').value;
        console.log(url);*/
    }

    var formData = new FormData();
    var file = document.getElementById('file').files[0];
    formData.append("Filedata", file);
    var t = file.type.split('/').pop().toLowerCase();
    if (t != "jpeg" && t != "jpg" && t != "png" && t != "bmp" && t != "gif") {
        Swal.fire({
            icon: 'error',
            title: 'Formato inválido',
            text: 'Por favor selecciona un formato de imagen válido'
          })
        document.getElementById('file').value = '';
        return false;
    }
}