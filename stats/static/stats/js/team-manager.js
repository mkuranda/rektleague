$(document).ready(function(){
    $('.sliderTop').slick();
    $('.sliderJungle').slick();
    $('.sliderMid').slick();
    $('.sliderBot').slick();
    $('.sliderSupport').slick();
    $('.sliderSub').slick();
    var elo;
    var top = 0;
    var jungle = 0;
    var mid = 0;
    var bot = 0;
    var support = 0;
    var sub1 = 0;
    var sub2 = 0;
    var sub3 = 0;
    var supportValue = 0;
    var botValue = 0;
    var midValue = 0;
    var jungleValue = 0;
    var topValue = 0;

    // ADD TOP
    $(document).on( "click","#addTop", function() {
        // If statement if team doesnt have a top
        if(top === 0){
        // Update ELO counter
        topValue = Number( $('.sliderTop .slick-active > div > .playerCard > .playerInfo > .playerValue').text() );
        elo = topValue + supportValue + midValue + botValue + jungleValue;
        $("#teamElo").text( elo );
        // Color indicator for ELO
        if ( elo > 0){
            $( "#teamElo" ).css( "color", "red" );
        }

        else {
            $( "#teamElo" ).css( "color", "white" );
        }
        console.log(topValue);
        console.log(elo)
        // Move playercard
        $(".sliderTop .slick-active > div > .playerCard").prependTo("#myTop");
        // Reset Slider now that cards missing
        $('.sliderTop').slick('slickNext');
        $('.sliderTop').slick('unslick');
        $('.sliderTop').slick();
        // Swap out add icon for minus icon
        $( "#myTop > .playerCard > .playerPhoto > #addTop" ).remove();
        $( "#myTop > .playerCard > .playerPhoto").append( "<i id='removeTop' class='fas fa-minus-square'></i>" );
        // Add "Add to team" button
        $( "#myTop > .playerCard > .playerPhoto").append( "<span id='inviteTop' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
        // Increment top so that you can only add one top
        ++top;
        // Color indicator for ELO
        }

        else{
            alert("You already have a top, silly!");
        }

    });

    // REMOVE TOP
    $(document).on( "click", "#removeTop", function() {
        // Declare variables
        topValue = 0;
        elo = topValue + supportValue + midValue + botValue + jungleValue;
        // Update ELO counter
        $("#teamElo").text( elo );
        // Color indicator for ELO
        if ( elo > 0){
            $( "#teamElo" ).css( "color", "red" );
        }

        else {
            $( "#teamElo" ).css( "color", "white" );
        }
        console.log(topValue);
        console.log(elo)
        // Switch - to +
        $("#myTop > .playerCard > .playerPhoto > #removeTop").remove();
        $("#myTop > .playerCard > .playerPhoto").append( "<i id='addTop' class='fas fa-plus-square'></i>" );
        // remove "Add to team" button
        $( "#myTop > .playerCard > .playerPhoto > #inviteTop").remove();
        // Add back into slider
        $('.sliderTop').slick('unslick');
        $("#myTop > .playerCard").prependTo( $(".sliderTop") );
        $('.sliderTop').slick();
        // Allow new top to be added
        top = 0;
    });

        // ADD JUNGLE
        $(document).on( "click","#addJungle", function() {
            // If statement if team doesnt have a top
            if(jungle === 0){
            // Update ELO counter
            jungleValue = Number( $('.sliderJungle  .slick-active > div > .playerCard > .playerInfo > .playerValue').text() );
            elo = topValue + supportValue + midValue + botValue + jungleValue;
            $("#teamElo").text( elo );
            // Color indicator for ELO
            if ( elo > 0){
                $( "#teamElo" ).css( "color", "red" );
            }
    
            else {
                $( "#teamElo" ).css( "color", "white" );
            }
            console.log(jungleValue);
            console.log(elo)
            // Move playercard
            $(".sliderJungle .slick-active > div > .playerCard").prependTo("#myJungle");
            // Reset Slider now that cards missing
            $('.sliderJungle').slick('slickNext');
            $('.sliderJungle').slick('unslick');
            $('.sliderJungle').slick();
            // Swap out add icon for minus icon
            $( "#myJungle > .playerCard > .playerPhoto > #addJungle" ).remove();
            $( "#myJungle > .playerCard > .playerPhoto").append( "<i id='removeJungle' class='fas fa-minus-square'></i>" );
            // Add "Add to team" button
            // Add "Add to team" button
            $( "#myJungle > .playerCard > .playerPhoto").append( "<span id='inviteJungle' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
            // Increment top so that you can only add one top
            ++jungle;
            // Color indicator for ELO
            }
    
            else{
                alert("You already have a jungler, silly!");
            }
    
        });
    
        // REMOVE JUNGLE
        $(document).on( "click", "#removeJungle", function() {
            // Declare variables
            jungleValue = 0;
            elo = topValue + supportValue + midValue + botValue + jungleValue;
            // Update ELO counter
            $("#teamElo").text( elo );
            // Color indicator for ELO
            if ( elo > 0){
                $( "#teamElo" ).css( "color", "red" );
            }
    
            else {
                $( "#teamElo" ).css( "color", "white" );
            }
            console.log(jungleValue);
            console.log(elo)
            // Switch - to +
            $("#myJungle > .playerCard > .playerPhoto > #removeJungle").remove();
            $("#myJungle > .playerCard > .playerPhoto").append( "<i id='addJungle' class='fas fa-plus-square'></i>" );
            // remove "Add to team" button
            $( "#myJungle > .playerCard > .playerPhoto > #inviteJungle").remove();
            // Add back into slider
            $('.sliderJungle').slick('unslick');
            $("#myJungle > .playerCard").prependTo( $(".sliderJungle") );
            $('.sliderJungle').slick();
            // Allow new top to be added
            jungle = 0;
        });


    // ADD MID
    $(document).on( "click","#addMid", function() {
        // If statement if team doesnt have a top
        if(mid === 0){
        // Update ELO counter
        midValue = Number( $('.sliderMid  .slick-active > div > .playerCard > .playerInfo > .playerValue').text() );
        elo = topValue + supportValue + midValue + botValue + jungleValue;
        $("#teamElo").text( elo );
        // Color indicator for ELO
        if ( elo > 0){
            $( "#teamElo" ).css( "color", "red" );
        }

        else {
            $( "#teamElo" ).css( "color", "white" );
        }
        console.log(midValue);
        console.log(elo)
        // Move playercard
        $(".sliderMid .slick-active > div > .playerCard").prependTo("#myMid");
        // Reset Slider now that cards missing
        $('.sliderMid').slick('slickNext');
        $('.sliderMid').slick('unslick');
        $('.sliderMid').slick();
        // Swap out add icon for minus icon
        $( "#myMid > .playerCard > .playerPhoto > #addMid" ).remove();
        $( "#myMid > .playerCard > .playerPhoto").append( "<i id='removeMid' class='fas fa-minus-square'></i>" );
        // Add "Add to team" button
        $( "#myMid > .playerCard > .playerPhoto").append( "<span id='inviteMid' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
        // Increment top so that you can only add one top
        ++mid;
        // Color indicator for ELO
        }

        else{
            alert("You already have a mid, silly!");
        }

    });

    // REMOVE MID
    $(document).on( "click", "#removeMid", function() {
        // Declare variables
        midValue = 0;
        elo = topValue + supportValue + midValue + botValue + jungleValue;
        // Update ELO counter
        $("#teamElo").text( elo );
        // Color indicator for ELO
        if ( elo > 0){
            $( "#teamElo" ).css( "color", "red" );
        }

        else {
            $( "#teamElo" ).css( "color", "white" );
        }
        console.log(midValue);
        console.log(elo)
        // Switch - to +
        $("#myMid > .playerCard > .playerPhoto > #removeMid").remove();
        $("#myMid > .playerCard > .playerPhoto").append( "<i id='addMid' class='fas fa-plus-square'></i>" );
        // remove "Add to team" button
        $( "#myMid > .playerCard > .playerPhoto > #inviteMid").remove();
        // Add back into slider
        $('.sliderMid').slick('unslick');
        $("#myMid > .playerCard").prependTo( $(".sliderMid") );
        $('.sliderMid').slick();
        // Allow new top to be added
        mid = 0;
    });


 // ADD BOT
 $(document).on( "click","#addBot", function() {
    // If statement if team doesnt have a top
    if(bot === 0){
    // Update ELO counter
    botValue = Number( $('.sliderBot  .slick-active > div > .playerCard > .playerInfo > .playerValue').text() );
    elo = topValue + supportValue + midValue + botValue + jungleValue;
    $("#teamElo").text( elo );
    // Color indicator for ELO
    if ( elo > 0){
        $( "#teamElo" ).css( "color", "red" );
    }

    else {
        $( "#teamElo" ).css( "color", "white" );
    }
    console.log(botValue);
    console.log(elo)
    // Move playercard
    $(".sliderBot .slick-active > div > .playerCard").prependTo("#myBot");
    // Reset Slider now that cards missing
    $('.sliderBot').slick('slickNext');
    $('.sliderBot').slick('unslick');
    $('.sliderBot').slick();
    // Swap out add icon for minus icon
    $( "#myBot > .playerCard > .playerPhoto > #addBot" ).remove();
    $( "#myBot > .playerCard > .playerPhoto").append( "<i id='removeBot' class='fas fa-minus-square'></i>" );
    // Add "Add to team" button
    $( "#myBot > .playerCard > .playerPhoto").append( "<span id='inviteBot' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
    // Increment top so that you can only add one top
    ++bot;
    // Color indicator for ELO
    }

    else{
        alert("You already have a ADC, silly!");
    }

});

// REMOVE BOT
$(document).on( "click", "#removeBot", function() {
    // Declare variables
    botValue = 0;
    elo = topValue + supportValue + midValue + botValue + jungleValue;
    // Update ELO counter
    $("#teamElo").text( elo );
    // Color indicator for ELO
    if ( elo > 0){
        $( "#teamElo" ).css( "color", "red" );
    }

    else {
        $( "#teamElo" ).css( "color", "white" );
    }
    console.log(botValue);
    console.log(elo)
    // Switch - to +
    $("#myBot > .playerCard > .playerPhoto > #removeBot").remove();
    $("#myBot > .playerCard > .playerPhoto").append( "<i id='addBot' class='fas fa-plus-square'></i>" );
    // remove "Add to team" button
    $( "#myBot > .playerCard > .playerPhoto > #inviteBot").remove();
    // Add back into slider
    $('.sliderBot').slick('unslick');
    $("#myBot > .playerCard").prependTo( $(".sliderBot") );
    $('.sliderBot').slick();
    // Allow new top to be added
    bot = 0;
});

 // ADD SUPPORT
 $(document).on( "click","#addSupport", function() {
    // If statement if team doesnt have a top
    if(support === 0){
    // Update ELO counter
    supportValue = Number( $('.sliderSupport  .slick-active > div > .playerCard > .playerInfo > .playerValue').text() );
    elo = topValue + supportValue + midValue + botValue + jungleValue;
    $("#teamElo").text( elo );
    // Color indicator for ELO
    if ( elo > 0){
        $( "#teamElo" ).css( "color", "red" );
    }

    else {
        $( "#teamElo" ).css( "color", "white" );
    }
    console.log(supportValue);
    console.log(elo)
    // Move playercard
    $(".sliderSupport .slick-active > div > .playerCard").prependTo("#mySupport");
    // Reset Slider now that cards missing
    $('.sliderSupport').slick('slickNext');
    $('.sliderSupport').slick('unslick');
    $('.sliderSupport').slick();
    // Swap out add icon for minus icon
    $( "#mySupport > .playerCard > .playerPhoto > #addSupport" ).remove();
    $( "#mySupport > .playerCard > .playerPhoto").append( "<i id='removeSupport' class='fas fa-minus-square'></i>" );
    // Add "Add to team" button
    $( "#mySupport > .playerCard > .playerPhoto").append( "<span id='inviteSupport' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
    // Increment top so that you can only add one top
    ++support;
    // Color indicator for ELO
    }

    else{
        alert("You already have a Support, silly!");
    }

});

// REMOVE SUPPORT
$(document).on( "click", "#removeSupport", function() {
    // Declare variables
    supportValue = 0;
    elo = topValue + supportValue + midValue + botValue + jungleValue;
    // Update ELO counter
    $("#teamElo").text( elo );
    // Color indicator for ELO
    if ( elo > 0){
        $( "#teamElo" ).css( "color", "red" );
    }

    else {
        $( "#teamElo" ).css( "color", "white" );
    }
    console.log(supportValue);
    console.log(elo)
    // Switch - to +
    $("#mySupport > .playerCard > .playerPhoto > #removeSupport").remove();
    $("#mySupport > .playerCard > .playerPhoto").append( "<i id='addSupport' class='fas fa-plus-square'></i>" );
    // remove "Add to team" button
    $( "#mySupport> .playerCard > .playerPhoto > #inviteSupport").remove();
    // Add back into slider
    $('.sliderSupport').slick('unslick');
    $("#mySupport > .playerCard").prependTo( $(".sliderSupport") );
    $('.sliderSupport').slick();
    // Allow new top to be added
    support = 0;
});

 // ADD SUB
 $(document).on( "click","#addSub", function() {
    // If statement if team doesnt have a top
    if(sub1 === 0){
    // Move playercard
    $(".sliderSub .slick-active > div > .playerCard").prependTo("#mySub1");
    // Reset Slider now that cards missing
    $('.sliderSub').slick('slickNext');
    $('.sliderSub').slick('unslick');
    $('.sliderSub').slick();
    // Swap out add icon for minus icon
    $( "#mySub1 > .playerCard > .playerPhoto > #addSub" ).remove();
    $( "#mySub1 > .playerCard > .playerPhoto").append( "<i id='removeSub1' class='fas fa-minus-square'></i>" );
    // Add "Add to team" button
    $( "#mySub1 > .playerCard > .playerPhoto").append( "<span id='inviteSub1' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
    // Increment top so that you can only add one top
    ++sub1;
    }

    else if(sub2 === 0){
    // Move playercard
    $(".sliderSub .slick-active > div > .playerCard").prependTo("#mySub2");
    // Reset Slider now that cards missing
    $('.sliderSub').slick('slickNext');
    $('.sliderSub').slick('unslick');
    $('.sliderSub').slick();
    // Swap out add icon for minus icon
    $( "#mySub2 > .playerCard > .playerPhoto > #addSub" ).remove();
    $( "#mySub2 > .playerCard > .playerPhoto").append( "<i id='removeSub2' class='fas fa-minus-square'></i>" );
    // Add "Add to team" button
    $( "#mySub2 > .playerCard > .playerPhoto").append( "<span id='inviteSub2' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
    // Increment top so that you can only add one top
    ++sub2;
    }

    else if(sub3 === 0){
        // Move playercard
        $(".sliderSub .slick-active > div > .playerCard").prependTo("#mySub3");
        // Reset Slider now that cards missing
        $('.sliderSub').slick('slickNext');
        $('.sliderSub').slick('unslick');
        $('.sliderSub').slick();
        // Swap out add icon for minus icon
        $( "#mySub3 > .playerCard > .playerPhoto > #addSub" ).remove();
        $( "#mySub3 > .playerCard > .playerPhoto").append( "<i id='removeSub3' class='fas fa-minus-square'></i>" );
        // Add "Add to team" button
        $( "#mySub3 > .playerCard > .playerPhoto").append( "<span id='inviteSub3' class='addtoTeam'>INVITE <i class='fas fa-paper-plane'></i></span>" );
        // Increment top so that you can only add one top
        ++sub3;
        }

    else{
        alert("You already have 3 Subs, silly!");
    }

});

// REMOVE SUB 1
$(document).on( "click", "#removeSub1", function() {
    // Switch - to +
    $("#mySub1 > .playerCard > .playerPhoto > #removeSub1").remove();
    $("#mySub1 > .playerCard > .playerPhoto").append( "<i id='addSub' class='fas fa-plus-square'></i>" );
    // remove "Add to team" button
    $( "#mySub1 > .playerCard > .playerPhoto > #inviteSub1").remove();
    // Add back into slider
    $('.sliderSub').slick('unslick');
    $("#mySub1 > .playerCard").prependTo( $(".sliderSub") );
    $('.sliderSub').slick();
    // Allow new top to be added
    sub1 = 0;
});

// REMOVE SUB 2
$(document).on( "click", "#removeSub2", function() {
    // Switch - to +
    $("#mySub2 > .playerCard > .playerPhoto > #removeSub2").remove();
    $("#mySub2 > .playerCard > .playerPhoto").append( "<i id='addSub' class='fas fa-plus-square'></i>" );
    // remove "Add to team" button
    $( "#mySub2 > .playerCard > .playerPhoto > #inviteSub2").remove();
    // Add back into slider
    $('.sliderSub').slick('unslick');
    $("#mySub2 > .playerCard").prependTo( $(".sliderSub") );
    $('.sliderSub').slick();
    // Allow new top to be added
    sub2 = 0;
});

// REMOVE SUB 3
$(document).on( "click", "#removeSub3", function() {
    // Switch - to +
    $("#mySub3 > .playerCard > .playerPhoto > #removeSub3").remove();
    $("#mySub3 > .playerCard > .playerPhoto").append( "<i id='addSub' class='fas fa-plus-square'></i>" );
    // remove "Add to team" button
    $( "#mySub3 > .playerCard > .playerPhoto > #inviteSub3").remove();
    // Add back into slider
    $('.sliderSub').slick('unslick');
    $("#mySub3 > .playerCard").prependTo( $(".sliderSub") );
    $('.sliderSub').slick();
    // Allow new top to be added
    sub3 = 0;
});

// CLOSING OF READY FUNCTION
});