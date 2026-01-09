function navegar(destino){
    let telas = document.getElementsByClassName('tela');
    Array.from(telas).forEach(element => {
        element.classList.remove('show');
        element.classList.add('collapse');
    });
    document.getElementById(destino).classList.remove('collapse');
    document.getElementById(destino).classList.add('show');
}