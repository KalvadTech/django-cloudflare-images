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

function setupUploadForm(data, element) {
  console.log(element);
  var form = element.getElementsByTagName("form")[0];
  form.setAttribute("action", data.result.uploadURL);

  var submit = element.getElementsByTagName("button")[0];

  form.addEventListener("submit", function(e) {
    console.log("inside submit");
    e.preventDefault();

    submit.style.display = 'none';

    var data = new FormData(e.target);
    fetch(event.target.action, {
      method: form.method,
      body: data
    }).then(function(response) {
      return response.json();
    }).then(function(d) {
      console.log(d);

      var link = element.getElementsByTagName("a")[0];
      link.setAttribute("href", d.result.variants[0]);
      link.innerHTML = d.result.id;
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
