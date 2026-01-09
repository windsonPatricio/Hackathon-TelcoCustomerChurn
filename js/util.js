export function navegar(idDestino){
    let telas = document.getElementsByClassName('tela');
    Array.from(telas).forEach(element => {
        element.classList.remove('show');
        element.classList.add('collapse');
    });
    document.getElementById(idDestino).classList.remove('collapse');
    document.getElementById(idDestino).classList.add('show');
}