// SEARCH BAR


var $rows = $('#table tr');
$('#search').keyup(function() {

    var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
        reg = RegExp(val, 'i'),
        text;

    $rows.show().filter(function() {
        text = $(this).text().replace(/\s+/g, ' ');
        return !reg.test(text);
    }).hide();
});

// SORT HERADER

function sortTable(f,n){
	var rows = $('#dataTable tbody  tr').get();

	rows.sort(function(a, b) {

		var A = getVal(a);
		var B = getVal(b);

		if(A < B) {
			return -1*f;
		}
		if(A > B) {
			return 1*f;
		}
		return 0;
	});

	function getVal(elm){
		var v = $(elm).children('td').eq(n).text().toUpperCase().replace(/%$/g, "");
		if($.isNumeric(v)){
			v = parseFloat(v,10);
		}
		return v;
	}

	$.each(rows, function(index, row) {
		$('#dataTable').children('tbody').append(row);
	});
}
var f_sl = 1;
var f_nm = 1;
$("#playerName").click(function(){
    f_sl *= -1;
    var n = $(this).prevAll().length;
    sortTable(f_sl,n);
});
$("#teamName").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#position").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#gamesPlayed").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#avgKills").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#avgDeaths").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#avgAssists").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#KDA").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#killParticipation").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#csDiff").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#csPerMin").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#teamDamagePercent").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
$("#visionScore").click(function(){
  f_sl *= -1;
  var n = $(this).prevAll().length;
  sortTable(f_sl,n);
});
