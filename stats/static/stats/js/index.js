$(document).ready(function(){
    $('.homepageSlider').slick({
        slidesToShow: 1,
        arrows: false,
        slidesToScroll: 1,
        speed: 0,
        autoplay: true,
        autoplaySpeed: 6000,
        cssEase: 'ease',
        lazyload: 'ondemand',
        draggable: false,
        fade: true,
        variableWidth: false,
      });
  });


  $( "#air" ).hover(
    function() {
      $(".teamDescriptionContainerAir").append( ".teamsBanners" );  
      $(".teamDescriptionContainerAir").fadeIn( 0 );
      $(".teamDescriptionContainerAir").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerAir").fadeOut( 0 );
      $(".teamDescriptionContainerAir").removeClass( "display" );
    }
  );

  $( "#ocean" ).hover(
    function() {
      $(".teamDescriptionContainerOcean").append( ".teamsBanners" );  
      $(".teamDescriptionContainerOcean").fadeIn( 0 );
      $(".teamDescriptionContainerOcean").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerOcean").fadeOut( 0 );
      $(".teamDescriptionContainerOcean").removeClass( "display" );
    }
  );

  $( "#mountain" ).hover(
    function() {
      $(".teamDescriptionContainerMountain").append( ".teamsBanners" );  
      $(".teamDescriptionContainerMountain").fadeIn( 0 );
      $(".teamDescriptionContainerMountain").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerMountain").fadeOut( 0 );
      $(".teamDescriptionContainerMountain").removeClass( "display" );
    }
  );

  $( "#infernal" ).hover(
    function() {
      $(".teamDescriptionContainerInfernal").append( ".teamsBanners" );  
      $(".teamDescriptionContainerInfernal").fadeIn( 0 );
      $(".teamDescriptionContainerInfernal").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerInfernal").fadeOut( 0 );
      $(".teamDescriptionContainerInfernal").removeClass( "display" );
    }
  );

  $( "#raptors" ).hover(
    function() {
      $(".teamDescriptionContainerRaptors").append( ".teamsBanners" );  
      $(".teamDescriptionContainerRaptors").fadeIn( 0 );
      $(".teamDescriptionContainerRaptors").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerRaptors").fadeOut( 0 );
      $(".teamDescriptionContainerRaptors").removeClass( "display" );
    }
  );

  $( "#scuttle" ).hover(
    function() {
      $(".teamDescriptionContainerSC").append( ".teamsBanners" );  
      $(".teamDescriptionContainerSC").fadeIn( 0 );
      $(".teamDescriptionContainerSC").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerSC").fadeOut( 0 );
      $(".teamDescriptionContainerSC").removeClass( "display" );
    }
  );

  $( "#sentinels" ).hover(
    function() {
      $(".teamDescriptionContainerSentinels").append( ".teamsBanners" );  
      $(".teamDescriptionContainerSentinels").fadeIn( 0 );
      $(".teamDescriptionContainerSentinels").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerSentinels").fadeOut( 0 );
      $(".teamDescriptionContainerSentinels").removeClass( "display" );
    }
  );

  $( "#brambleback" ).hover(
    function() {
      $(".teamDescriptionContainerBramble").append( ".teamsBanners" );  
      $(".teamDescriptionContainerBramble").fadeIn( 0 );
      $(".teamDescriptionContainerBramble").addClass( "display" );
    }, function() {
      $(".teamDescriptionContainerBramble").fadeOut( 0 );
      $(".teamDescriptionContainerBramble").removeClass( "display" );
    }
  );

  // STREAM LIVE CHECK
function CheckOnlineStatus()
{
  $.ajax({
	  type: 'GET',
    url: "https://api.twitch.tv/kraken/streams/therektleague",
    dataType: 'json',
    headers: {
      'Client-ID': 'lj3s7o2tmiisf4961ceiu18yhmapju'
    },
    success: function(channel)
    {
      if (channel["stream"] == null)
      {
        console.log(" is not online");
      } else {
	      document.getElementById("welcome").insertAdjacentHTML('beforeend' , '<div id="twitch-embed"></div>');
	      var embed = new Twitch.Embed("twitch-embed", {
          width: '80%',
          height: 480,
          theme: 'dark',
          channel: "therektleague"
        });

      }
    }
  });
}