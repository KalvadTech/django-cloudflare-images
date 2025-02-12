function getOneTimeUploadUrl() {
  // TODO: The "ext" part
  var url = document.location.origin + "/ext/cloudflare_images/api";

  return fetch(url).then(function(response) {
    if (!response.ok) {
      throw new Error("HTTP status:" + response.status);
    }

    return response.json();
  }).then(function(data) {
    console.log(data);
    return data;
  }).catch(function(err) {
    console.error("Something went wrong: " + err);
  });
}

function clickListener(e) {
  console.log("inside click");
  e.preventDefault();

  e.target.disabled = true;

  getOneTimeUploadUrl().then(function(response) {
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

      // TODO: Call the PUT endpoint

      e.target.disabled = false;
    });

  });
}

function setupUploadForm(element) {
  console.log(element);
  var submit = element.getElementsByTagName("button")[0];
  submit.addEventListener("click", clickListener);
}

window.addEventListener('DOMContentLoaded', function() {
  var elements = document.getElementsByClassName("ci-widget");

  for (element of elements) {
    setupUploadForm(element);
  }
});
