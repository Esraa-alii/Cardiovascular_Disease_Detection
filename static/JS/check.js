// var myvar myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
  showModal()
})
// function handleClick() {
//   document.getElementById("co").style.display='block'
// }

function clear() {
  document.getElementById('modal_').innerHTML = "";
}

function dbclick(e) {
  e.preventdefault()
  document.getElementById('exampleModal')
}