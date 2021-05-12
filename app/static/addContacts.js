let i=1;

document.getElementById('no-of-contacts').value = 1;


document.getElementById('add-contact').onclick = function() {

    var element = `
    <div>    
        <h4> <b> Contact ${i+1} </b> </h4>
        <label for="name"> Name </label>
        <input class="form-control"  type="text" name="contacts[${i}][name]" id="name">
        <label for="name"> Email </label>
        <input class="form-control"  type="email" name="contacts[${i}][email]" id="email">
        <label for="name"> Phone </label>
        <input class="form-control" type="tel" name="contacts[${i}][phone]" id="phone"> 
    </div> <br>
    `;
    

    let div = document.createElement('div');
    div.innerHTML = element;

    let contacts = document.getElementById('contacts');
    contacts.innerHTML += element;

    i++;

    document.getElementById('no-of-contacts').value = i;

}

document.getElementById('delete-contact').onclick = function() {

    if (i==1){
        alert("Minimum one contact is needed");
        return
    }

    let doc = document.getElementById('contacts')
    doc.removeChild(doc.lastElementChild)
    doc.removeChild(doc.lastElementChild)
    
    i--;
    document.getElementById('no-of-contacts').value = i;

}


