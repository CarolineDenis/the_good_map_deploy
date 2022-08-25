
var images = new Array("../static/img/eolienne.jpg",
    "../static/img/food.jpg",
    "../static/img/nature1.png",
    "../static/img/plant.jpg",
    "../static/img/plastic_bottle.jpg",
    "../static/img/tree.jpg",
    );

var images2 = new Array("../static/img/boat.jpg", 
"../static/img/construction.jpg",
"../static/img/eolienne.jpg",
"../static/img/water.jpg",
"../static/img/friends.jpg",);

var images3 = new Array("../static/img/boat1.jpg",
"../static/img/construction1.jpg",
"../static/img/deer.jpg",
"../static/img/field.jpg",
"../static/img/grape.jpg");

var images4 = new Array("../static/img/kid.jpg",
"../static/img/mother.jpg",
"../static/img/river.jpg",
"../static/img/school.jpg",
"../static/img/sheep.jpg",
"../static/img/street.jpg");

popup();
function popup() {
    randomImage = images[Math.floor(Math.random() * images.length)];
    document.getElementById("changeThis").style.display = "block";
    document.getElementById("changeThis").style.position = "absolute";
    document.getElementById("changeThis").style.top = "110%";
    document.getElementById("changeThis").style.left = "10%";
    document.getElementById("changeThis").style.width = "80px";
    document.getElementById("changeThis").src = randomImage;
    setTimeout(hidePopup, 2000);
}
function hidePopup() {
    document.getElementById("changeThis").style.display = "none";
    setTimeout(popup, 2800);
}

popup2();
function popup2() {
    randomImage2 = images2[Math.floor(Math.random() * images2.length)];
    document.getElementById("changeThis2").style.display = "block";
    document.getElementById("changeThis2").style.position = "absolute";
    document.getElementById("changeThis2").style.top = "160%";
    document.getElementById("changeThis2").style.left = "20%";
    document.getElementById("changeThis2").style.width = "80px";
    document.getElementById("changeThis2").src = randomImage2;
    setTimeout(hidePopup2, 3000);
}
function hidePopup2() {
    document.getElementById("changeThis2").style.display = "none";
    setTimeout(popup2, 1000);
}

popup3();
function popup3() {
    randomImage3 = images3[Math.floor(Math.random() * images3.length)];
    document.getElementById("changeThis3").style.display = "block";
    document.getElementById("changeThis3").style.position = "absolute";
    document.getElementById("changeThis3").style.top = "110%";
    document.getElementById("changeThis3").style.left = "70%";
    document.getElementById("changeThis3").style.width = "80px";
    document.getElementById("changeThis3").src = randomImage3;
    setTimeout(hidePopup3, 2500);
}
function hidePopup3() {
    document.getElementById("changeThis3").style.display = "none";
    setTimeout(popup3, 2500);
}

popup4();
function popup4() {
    randomImage4 = images4[Math.floor(Math.random() * images4.length)];
    document.getElementById("changeThis4").style.display = "block";
    document.getElementById("changeThis4").style.position = "absolute";
    document.getElementById("changeThis4").style.top = "170%";
    document.getElementById("changeThis4").style.left = "60%";
    document.getElementById("changeThis4").style.width = "80px";
    document.getElementById("changeThis4").src = randomImage4;
    setTimeout(hidePopup4, 3000);
}
function hidePopup4() {
    document.getElementById("changeThis4").style.display = "none";
    setTimeout(popup4, 3000);
}