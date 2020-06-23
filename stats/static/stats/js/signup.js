document.getElementById('addAccount').onclick = function newAccount(){
  // document.getElementById('extraAccounts').innerHTML = '<input class="form-control" type="text" placeholder="Example: Judge Jett">';
var count = 1;
  	
$( '<input class="form-control" id="extraAccountsField" type="text" placeholder="Additional Account">' ).appendTo( ".extraAccountLabel" );
count++;
}