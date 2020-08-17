$(document).ready(function(){
    $('.slider').slick();


    document.getElementById('addTop').onclick = function moveTop(){
        var parent = document.querySelector('#myTop'),
        child = document.querySelector('.playerCard');
        
        if(parent.querySelector('.child') === null){
        $(".slick-active > div > .playerCard").prependTo("#myTop");
        $('.slider').slick('slickNext');
        $('.slider').slick('unslick');
        $('.slider').slick();
        $( "#myTop > .playerCard > .playerPhoto > #addTop" ).remove();
        $( "#myTop > .playerCard > .playerPhoto").append( "<i id='removeTop' class='fas fa-minus-square'></i>" );
        }

    };

    $( "#removeTop" ).on( "click", function() {
        $("#myTop > .playerCard > .playerPhoto > #removeTop").remove();
        $("#myTop > .playerCard > .playerPhoto").append( "<i id='addTop' class='fas fa-plus-square'></i>" );
        $("#myTop > .playerCard").prependTo(".slider");
        $('.slider').slick('unslick');
        $('.slider').slick();
        console.log("hi");
    });


});