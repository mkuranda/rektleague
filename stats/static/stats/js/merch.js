// INCREMENT SHOTS
var shots = 0;
var shotsPrice = 5.99
document.getElementById('numberOfItemsShots').innerHTML = shots;

document.getElementById('downShots').onclick = function numberDown() {
    document.getElementById('numberOfItemsShots').innerHTML = shots;
    if(shots <= 0){
    shots=0;
    } else {
        shots = shots - 1;
    }
    document.getElementById('numberOfItemsShots').innerHTML = shots;
}

document.getElementById('upShots').onclick = function numberUp() {
    shots++;
    document.getElementById('numberOfItemsShots').innerHTML = shots;
}

// ADD SHOTS TO CART AND ROUND THEM TO 2 DECIMALS
document.getElementById('addShotsToCart').onclick = function shotsToCart() {
document.getElementById('shotsTotal').innerHTML = Number(Math.round(parseFloat((shots * shotsPrice) + 'e' + 2)) + 'e-' + 2);
document.getElementById('shotsInCart').innerHTML = shots;
if (shots > 0){
document.getElementById('addShotsToCart').innerHTML = "UPDATE";}
else {
    document.getElementById('addShotsToCart').innerHTML = "ADD TO CART";
}
showShots();
updateTotal();
}

// INCREMENT STICKERS
var stickers = 0;
var stickersPrice = 1.99
document.getElementById('numberOfItemsStickers').innerHTML = stickers;

document.getElementById('downStickers').onclick = function numberDownStickers() {
    if(stickers <= 0){
    stickers = 0;
    } else {
        stickers = stickers - 1;
    }
    document.getElementById('numberOfItemsStickers').innerHTML = stickers;
    return stickers;
}

document.getElementById('upStickers').onclick = function numberUpStickers() {
    stickers++;
    document.getElementById('numberOfItemsStickers').innerHTML = stickers;
    return stickers;
}

// REMOVE SHOTS FROM CART

document.getElementById('removeShots').onclick = function removeShotsFromCart() {
    shots = 0;
    document.getElementById('numberOfItemsShots').innerHTML = shots;
    document.getElementById('hideShots').style.display = "none";
    updateTotal();
}


// REMOVE STICKERS FROM CART

document.getElementById('removeStickers').onclick = function removeStickersFromCart() {
    stickers = 0;
    document.getElementById('numberOfItemsStickers').innerHTML = stickers;
    document.getElementById('hideStickers').style.display = "none";
    updateTotal();
}
// SHOW OR HIDE STICKERS IN CART

function showStickers() {
    if (stickers > 0){
    document.getElementById('hideStickers').style.display = "block";
} else {
    document.getElementById('hideStickers').style.display = "none";
}
}

function showShots() {
    if (shots > 0){
    document.getElementById('hideShots').style.display = "block";
} else {
    document.getElementById('hideShots').style.display = "none";
}
}

// ADD STICKERS TO CART AND ROUND THEM TO 2 DECIMALS
document.getElementById('addStickersToCart').onclick = function stickersToCart() {
document.getElementById('stickersTotal').innerHTML = Number(Math.round(parseFloat((stickers * stickersPrice) + 'e' + 2)) + 'e-' + 2);
document.getElementById('stickersInCart').innerHTML = stickers;
if (stickers > 0){
document.getElementById('addStickersToCart').innerHTML = "UPDATE";}
else {
    document.getElementById('addStickersToCart').innerHTML = "ADD TO CART";
}
showStickers();
updateTotal();
}

total= 0.00

// MATH TOTAL
function updateTotal() {
var total = (stickers * 1.99) + (shots * 5.99);
document.getElementById('total').innerHTML = Number(Math.round(parseFloat(total + 'e' + 2)) + 'e-' + 2);
}
// IMPLEEMENT PAYPAL
    paypal.Buttons({

    style: {
    color:  'blue',
    shape:  'pill',
    height: 40,
},
    createOrder: function(data, actions) {
      // This function sets up the details of the transaction, including the amount and line item details.
      request = {
        intent: "capture",
        purchase_units: [{
          amount: {
            currency_code: "USD",
            value: (stickers * 1.99) + (shots * 5.99),
            breakdown: {
              item_total: {
                currency_code: "USD",
                value: (stickers * 1.99) + (shots * 5.99)
              }
	    }
          },
	  items: [
	  ]
        }]
      };
      if (stickers > 0)
      {
        request.purchase_units[0].items.push({
          name: "Rekt Sticker",
          unit_amount: {
            currency_code: "USD",
            value: 1.99
          },
          quantity: stickers
        });
      }
      if (shots > 0)
      {
        request.purchase_units[0].items.push({
          name: "Rekt Shot Glass",
          unit_amount: {
            currency_code: "USD",
            value: 5.99
          },
          quantity: shots
        });
      }
      return actions.order.create(request);
    },
    onApprove: function(data, actions) {
      // This function captures the funds from the transaction.
      return actions.order.capture().then(function(details) {
        // This function shows a transaction success message to your buyer.
        alert('Transaction completed by ' + details.payer.name.given_name);
      });
    }
  }).render('#paypal-button-container');
  //This function displays Smart Payment Buttons on your web page.
