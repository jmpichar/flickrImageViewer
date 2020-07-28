
const displayedImage = document.querySelector('.full-img');
const thumbBar = document.querySelector('.thumb-bar');


function show_images() {
    d3.json('/photos').then((data) => {
      // var PANEL = d3.select("#flickr_images");
      // PANEL.html("");

      console.log(data)
      if (!data.hasOwnProperty("no_images")) {
        firstImage = Object.values(data)[0].replace("_m.jpg", "_b.jpg");
        currentImage = document.createElement('img');
        currentImage.setAttribute('src',firstImage)
        displayedImage.appendChild(currentImage)
        console.log("First image:" + firstImage + "\n");
        newImage = document.getElementById("flickr_images")
        newImage.innerHTML = "";
        // document.getElementById("flickr_images").innerHTML = "";
        for (var key of Object.keys(data)) {
          var image = data[key];
          var tmp = "<img src=" + image + "></a>";
          newImage.innerHTML += tmp;
          newImage.onclick = function(e) {
            console.log(e.target.src)
            var large_image = e.target.src.replace("_t.jpg", "_b.jpg");
            currentImage.src = large_image;
          }
        }
      }
    });
}

function  init() {
  if ( typeof(load_images) != "undefined") {
    console.log("load images is :" + load_images)
  }

  show_images()
}

init();
