
function getInputName() {
  // TODO: not hardcode and handle multi
  return "image"
}

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

function setupUploadForm(data) {
  var form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("action", data.result.uploadURL);
  form.setAttribute("enctype", "multipart/form-data");

  var input = document.createElement("input");
  input.setAttribute("type", "file");
  input.setAttribute("id", getInputName());
  input.setAttribute("name", "file");

  var submit = document.createElement("button");
  submit.innerHTML = "Upload";

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

      // TODO: Instead of creating a link, update the existing one (?)
      var link = document.createElement("a");
      link.setAttribute("href", d.result.variants[0]);
      link.setAttribute("target", "_blank");
      link.innerHTML = "Preview link";
      form.appendChild(link);
    });
  });

  form.appendChild(input);
  form.appendChild(submit);
  
  //TODO:
  document.getElementsByClassName("ci-widget")[0].appendChild(form);
}

window.addEventListener('DOMContentLoaded', function() {
  // TODO: Check if there are some .ci-widget on the page or not first
  getOneTimeUploadUrl().then(function(data) {
    setupUploadForm(data);
  });
});
