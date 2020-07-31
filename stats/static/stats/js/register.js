var count = 1;

document.getElementById('addAccount').onclick = function newAccount(){
  // document.getElementById('extraAccounts').innerHTML = '<input class="form-control" type="text" placeholder="Example: Judge Jett">';
  	
$( '<input class="form-control" id="id_extraAccount' + count + '" name="extraAccount' + count + '" type="text" placeholder="Additional Account">' ).appendTo( ".extraAccountLabel" );
count++;
}
