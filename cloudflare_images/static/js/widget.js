function getOneTimeUploadUrl(upload_endpoint) {
  var url = document.location.origin + upload_endpoint;

  return fetch(url).then(function(response) {
    if (!response.ok) {
      throw new Error("HTTP status:" + response.status);
    }

    return response.json();
  }).then(function(data) {
    return data;
  }).catch(function(err) {
    console.error("Something went wrong: " + err);
  });
}

function clickListener(e, element) {
  e.preventDefault();

  e.target.disabled = true;

  getOneTimeUploadUrl(element.dataset.uploadEndpoint).then(function(response) {
    var data = new FormData();
    data.append("file", element.querySelectorAll("input[type='file']")[0].files[0]);

    fetch(response.result.uploadURL, {
      method: "POST",
      body: data
    }).then(function(response) {
      return response.json();
    }).then(function(d) {
      var link = element.getElementsByTagName("a")[0];
      if (! link) {
        link = document.createElement("a");
        link.setAttribute("target", "_blank");
        element.append(link);
      }
      link.setAttribute("href", d.result.variants[0]);
      link.innerHTML = d.result.id;

      var hidden_id = element.querySelectorAll("input[type='hidden']")[0];
      hidden_id.value = d.result.id;

      e.target.disabled = false;
    });

  });
}

function setupUploadForm(element) {
  var submit = element.getElementsByTagName("button")[0];
  submit.addEventListener("click", function(e) { clickListener(e, element)});
}

window.addEventListener('DOMContentLoaded', function() {
  var elements = document.getElementsByClassName("ci-widget");

  for (element of elements) {
    setupUploadForm(element);
  }
});
