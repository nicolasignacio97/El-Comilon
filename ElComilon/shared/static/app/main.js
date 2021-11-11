// const btn = document.querySelector('#menu-btn');
// const menu = document.querySelector('#sidemenu');
// const sinIcono1 = document.querySelector('#icono1');
// const sinIcono2 = document.querySelector('#icono2');
// const sinIcono3 = document.querySelector('#icono3');
// const sinIcono4 = document.querySelector('#icono4');
// const sinIcono5 = document.querySelector('#icono5');
// const sinIcono6 = document.querySelector('#icono6');
// const sinIcono7 = document.querySelector('#icono7');


// btn.addEventListener('click', function () {

//     document.getElementById('sidemenu').classList.toggle('menu-expanded');
//     document.getElementById('sidemenu').classList.toggle('menu-collapsed');
//     document.getElementById('sidemenu').classList.toggle('animate__fadeight');
//     document.getElementById('sidemenu').classList.toggle('animate__fadeInLeft');

//     // if (a == false) {
//     //     sinIcono1.style.display='block';
//     //     sinIcono2.style.display='block';
//     //     sinIcono3.style.display='block';
//     //     sinIcono4.style.display='block';
//     //     sinIcono5.style.display='block';
//     //     sinIcono6.style.display='block';
//     //     sinIcono7.style.display='block';

//     // }else{
//     //     sinIcono1.style.display='none';
//     //     sinIcono2.style.display='none';
//     //     sinIcono3.style.display='none';
//     //     sinIcono4.style.display='none';
//     //     sinIcono5.style.display='none';
//     //     sinIcono6.style.display='none';
//     //     sinIcono7.style.display='none';

//     // }

// });


const menuIzquierdo = document.querySelector('.menu-izquerdo');
const menuBajo = document.querySelector('.menu-bajo');

menuIzquierdo.addEventListener('click', (e) => {
    const claseMenu = e.target.classList;

    // Selecciona el contenedor
    const contenedor = document.querySelector('.menu-admin');
        
        flechaDer = document.querySelector('.fa-arrow-right');
 
      
        contenedor.classList.add('no-menu');   
        flechaDer.style.display = 'block';
 
});
menuBajo.addEventListener('click', (e) => {
    const claseMenu = e.target.classList;

    const contenedor = document.querySelector('.menu-admin');
        flechaDer = document.querySelector('.fa-arrow-right');
        claseMenu.contains('fa-arrow-right');
        contenedor.classList.remove('no-menu');
        flechaDer.style.display = 'none';

});