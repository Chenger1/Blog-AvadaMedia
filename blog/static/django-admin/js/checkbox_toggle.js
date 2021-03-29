const checkbox = document.getElementById('checkbox_toggle')
const select_checkboxes = document.getElementsByClassName('action-select')

checkbox.addEventListener('change', function (){
    if (this.checked){
        change_checkboxes_status(true)
    }else{
        change_checkboxes_status(false)
    }
})

function change_checkboxes_status(status){
    for(let checkbox of select_checkboxes){
        checkbox.checked = status;
    }
}
