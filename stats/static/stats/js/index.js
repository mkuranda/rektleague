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

//   // STREAM LIVE CHECK
// function CheckOnlineStatus()
// {
//   $.ajax({
// 	  type: 'GET',
//     url: "https://api.twitch.tv/kraken/streams/therektleague",
//     dataType: 'json',
//     headers: {
//       'Client-ID': 'lj3s7o2tmiisf4961ceiu18yhmapju'
//     },
//     success: function(channel)
//     {
//       if (channel["stream"] == null)
//       {
//         console.log(" is not online");
//       } else {
// 	      document.getElementById("welcome").innerHTML = "<div id='twitch-embed'></div>";
// 	      var embed = new Twitch.Embed("twitch-embed", {
//           width: "80%",
//           height: 480,
//           theme: "dark",
//           channel: "therektleague",
//         });

//       }
//     }
//   });
// }


document.getElementById("welcome").innerHTML = "<div id='twitch-embed'></div>";
var embed = new Twitch.Embed("twitch-embed", {
          width: "80%",
          height: 600,
          theme: "dark",
          channel: "therektleague",
        });