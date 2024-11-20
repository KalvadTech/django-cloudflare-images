function getOneTimeUploadUrl() {
  // TODO: The "ext" part
  var url = document.location.origin + "/ext/cloudflare_images/api";

  return fetch(url).then(function(response) {
    return response.json();
  }).then(function(data) {
    console.log(data);
    return data;
  });
}

function setupUploadForm(response, element) {
  console.log(element);
  var submit = element.getElementsByTagName("button")[0];

  submit.addEventListener("click", function(e) {
    console.log("inside click");
    e.preventDefault();

    // TODO: there's probably a better way to prevent multiple clicks
    submit.style.display = 'none';

    var data = new FormData();
    data.append("file", element.getElementsByTagName("input")[0].files[0]);

    fetch(response.result.uploadURL, {
      method: "POST",
      body: data
    }).then(function(response) {
      return response.json();
    }).then(function(d) {
      console.log(d);

      var link = element.getElementsByTagName("a")[0];
      link.setAttribute("href", d.result.variants[0]);
      link.innerHTML = d.result.id;

      var input = element.getElementsByTagName("input")[0];
      input.value = d.result.id; // Browser throws an error, we cannot modify a file type
    });
  });

}

window.addEventListener('DOMContentLoaded', function() {
  var elements = document.getElementsByClassName("ci-widget");

  // TODO: no need to pre-request a one time url every time
  for (element of elements) {
    getOneTimeUploadUrl().then(function(data) {
      setupUploadForm(data, element);
    });
  }
});
