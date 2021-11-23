function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$('#post-form').on('submit', function (event) {
    event.preventDefault();
    let inputrut = document.getElementById('txt-rut')
    let rut = document.getElementById('txt-rut').value;
    let txtHtml = document.getElementById('txt-invalid');
    var formData = new FormData(document.getElementById('post-form'));
    formData.append('rut', rut);
    if (rut && document.getElementById('post-form').checkValidity()) {
        document.getElementById('post-form').classList.add('was-validated')
        fetch('{% url "validarRut" %}', {
            method: 'POST',
            mode: 'same-origin',
            cache: 'no-cache',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        }).then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.valid) {
                    console.log("Usuario registrado con exito")
                    fetch('{% url "regin" %}'), {
                        method: 'POST',
                        mode: 'same-origin',
                        cache: 'no-cache',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                    }
                    txtHtml.classList.replace('valid-feedback', 'invalid-feedback')
                    $('#post-form').submit();
                } else {
                    txtHtml.classList.replace('invalid-feedback', 'valid-feedback')
                    txtHtml.innerHTML = 'Rut registrado'
                    console.log("Repartidor existente en la bd")

                    alert("Repartidor existente en la bd")
                }
            });
    } else {

        console.log("Llene todos los campos")
        event.preventDefault();
    }
});