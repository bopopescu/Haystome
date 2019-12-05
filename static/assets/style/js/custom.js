
// $('#artistcarousel').on('slide.bs.carousel', function (e) {
//     repeatCarouselItems(e, 4);
// });
// $('#categorycarousel').on('slide.bs.carousel', function (e) {
//     repeatCarouselItems(e, 4);
// });
// $('#explistingcarousel').on('slide.bs.carousel', function (e) {
//     repeatCarouselItems(e, 4);
// });
// $('#travellerreview').on('slide.bs.carousel', function (e) {
//     repeatCarouselItems(e, 3);
// });
// $('#howitwork').on('slide.bs.carousel', function (e) {
//     repeatCarouselItems(e, 1);
// });
//
// function repeatCarouselItems(e, itemsPerSlide) {
//     $e = $(e.relatedTarget);
//     var currentTarget = e.currentTarget.id
//     var idx = $e.index();
//     var totalItems = $(`#${currentTarget} > .carousel-inner > .carousel-item`).length;
//
//     if (idx >= totalItems - (itemsPerSlide - 1)) {
//         var it = itemsPerSlide - (totalItems - idx);
//         for (var i = 0; i < it; i++) {
//             // append slides to end
//             if (e.direction == "left") {
//                 $(`#${currentTarget} > .carousel-inner > .carousel-item`).eq(i).appendTo(`#${currentTarget} > .carousel-inner`);
//             }
//             else {
//                 $(`#${currentTarget} > .carousel-inner > .carousel-item`).eq(0).appendTo(`#${currentTarget} > .carousel-inner`);
//             }
//         }
//     }
// }

$(document).on('click', '[data-toggle="lightbox"]', function(event){
    event.preventDefault();
    $(this).ekkoLightbox();
});

$("#aboutus").click(function() {
    $('html, body').animate({
        scrollTop: $("#howitwork").offset().top -50
    }, 2000);
});

$("#artist").click(function() {
    $('html, body').animate({
        scrollTop: $("#artist-list").offset().top -50
    }, 2000);
});

$("#exp").click(function() {
    $('html, body').animate({
        scrollTop: $("#experience-list").offset().top -50
    }, 2000);
});


function promoInput(){
    var x = document.getElementById("promo_code");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
function promo() {
    document.getElementById("promo_code").value = document.getElementById("promo_code").value;
    if (document.getElementById("promo_code").value.length > 0)
        $("#promo_code").css('border-color', 'green')
}
function pickupKeyUp() {
    document.getElementById("pickup_location").value = document.getElementById("pickup_location").value;

    if (document.getElementById("pickup_location").value.length > 0)
        $("#pickup_location").css('border-color', 'green')
}
function questionKeyUp() {
    document.getElementById("question").value = document.getElementById("question").value.replace(/[^0-9a-zA-Z]/g, "");

    if (document.getElementById("Question").value.length > 0)
        $("#Question").css('border-color', 'green')
}
function phoneKeyUp() {
    document.getElementById("phone_number").value = document.getElementById("phone_number").value;
    $("#phone_number").css('text-transform', 'uppercase');
    if (document.getElementById("phone_number").value.length > 0)
        $("#phone_number").css('border-color', 'green')
}

function emailKeyUp() {
    document.getElementById("email").value = document.getElementById("email").value;

    if (document.getElementById("email").value.length > 0)
        $("#email").css('border-color', 'green')
}
function languageKeyUp() {
    document.getElementById("language").value = document.getElementById("language").value.replace(/[^0-9a-zA-Z]/g, "");
    $("#language").css('text-transform', 'uppercase');
    if (document.getElementById("language").value.length > 0)
        $("#language").css('border-color', 'green')
}
function genderKeyUp() {
    document.getElementById("gender").value = document.getElementById("Gender").value.replace(/[^0-9a-zA-Z]/g, "");
    $("#gender").css('text-transform', 'uppercase');
    if (document.getElementById("gender").value.length > 0)
        $("#gender").css('border-color', 'green')
}
function passportExpDateKeyUp() {
    document.getElementById("passport_exp_date").value = document.getElementById("passport_exp_date").value.replace(/[^0-9a-zA-Z ]/g, "");
    $("#passport_exp_date").css('text-transform', 'uppercase');
    if (document.getElementById("passport_exp_date").value.length == 2)
        document.getElementById("passport_exp_date").value = document.getElementById("passport_exp_date").value.concat(" ");
    else if (document.getElementById("passport_exp_date").value.length == 6)
        document.getElementById("passport_exp_date").value = document.getElementById("passport_exp_date").value.concat(" ");
    if (document.getElementById("passport_exp_date").value.length > 0)
        $("#passport_exp_date").css('border-color', 'green')
}
function passportIdKeyUp() {
    document.getElementById("passport_id").value = document.getElementById("passport_id").value.replace(/[^0-9a-zA-Z]/g, "");
    $("#passport_id").css('text-transform', 'uppercase');
    if (document.getElementById("passport_id").value.length > 0)
        $("#passport_id").css('border-color', 'green')
}
function payerNameKeyUp() {
    document.getElementById("payer_name").value = document.getElementById("payer_name").value.replace(/[^a-zA-Z ]/g, "");
    $("#payer_name").css('text-transform', 'uppercase');
    if (document.getElementById("payer_name").value.length > 0)
        $("#payer_name").css('border-color', 'green')
}


