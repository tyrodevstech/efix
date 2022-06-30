// document.querySelector() is used to select an element from the document using its ID
let captchaText = document.querySelector('#captcha');
if (captchaText) {
  var ctx = captchaText.getContext("2d");
  ctx.font = "700 30px Arial";
  ctx.fillStyle = "#313131";

  let userText = document.querySelector('#textBox');
  let submitButton = document.querySelector('#create');
  let output = document.querySelector('#output');
  let refreshButton = document.querySelector('#refreshButton');

  let alphaNums = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  let emptyArr = [];

  for (let i = 1; i <= 7; i++) {
    emptyArr.push(alphaNums[Math.floor(Math.random() * alphaNums.length)]);
  }

  var c = emptyArr.join('');

  ctx.fillText(emptyArr.join(''), captchaText.width / 4, captchaText.height / 1.25);
  for (var i = 0; i < 7; i += 1) {
    ctx.beginPath();
    ctx.moveTo(Math.random() * captchaText.width, Math.random() * captchaText.height);
    ctx.lineTo(Math.random() * captchaText.width, Math.random() * captchaText.height);
    ctx.stroke();
  }

  var dots = [];
  var numDots = 25;
  var width = captchaText.width;
  var height = captchaText.height;
  var bounce = -1;
  for (var i = 0; i < numDots; i++) {
    dots.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: Math.random() * 10 - 5,
      vy: Math.random() * 10 - 5,
    })
  }

  function draw() {
    var j, dot;
    for (j = 0; j < numDots; j++) {
      dot = dots[j];
      ctx.beginPath();
      ctx.arc(dot.x, dot.y, 1.5, 0, Math.PI * 2, false);
      ctx.fillStyle = "#313131"
      ctx.fill();
      ctx.stroke();
    }
  }
  draw();


  function update() {
    var i, dot;
    for (i = 0; i < numDots; i++) {
      dot = dots[i];
      dot.x += dot.vx;
      dot.y += dot.vy;

      if (dot.x > width) {
        dot.x = width;
        dot.vx *= bounce;
      } else if (dot.x < 0) {
        dot.x = 0;
        dot.vx *= bounce;
      }

      if (dot.y > height) {
        dot.y = height;
        dot.vy *= bounce;
      } else if (dot.y < 0) {
        dot.y = 0;
        dot.vy *= bounce;
      }
    }
  }






  userText.addEventListener('keyup', function (e) {
    if (e.keyCode === 13) {
      if (userText.value === c) {
        output.classList.remove("errorlabel");
        output.innerHTML = "Captcha Matched !";
      } else {
        e.preventDefault();
        output.classList.add("errorlabel");
        output.innerHTML = "Incorrect, please try again";
      }
    }
  });

  submitButton.addEventListener('click', function (e) {
    if (userText.value === c) {
      output.classList.remove("errorlabel");
      output.innerHTML = "Captcha Matched!";
    } else {
      e.preventDefault();
      output.classList.add("errorlabel");
      output.innerHTML = "Incorrect, please try again";

    }
  });

  refreshButton.addEventListener('click', function () {
    userText.value = "";
    let refreshArr = [];
    for (let j = 1; j <= 7; j++) {
      refreshArr.push(alphaNums[Math.floor(Math.random() * alphaNums.length)]);
    }
    ctx.clearRect(0, 0, captchaText.width, captchaText.height);
    c = refreshArr.join('');
    ctx.fillText(refreshArr.join(''), captchaText.width / 4, captchaText.height / 1.25);
    for (var i = 0; i < 7; i += 1) {
      ctx.beginPath();
      ctx.moveTo(Math.random() * captchaText.width, Math.random() * captchaText.height);
      ctx.lineTo(Math.random() * captchaText.width, Math.random() * captchaText.height);
      ctx.stroke();
    }
    update();
    draw();
    output.classList.remove("errorlabel");
    output.innerHTML = "Read Captcha Properly and Then Enter The Code";
  });

}