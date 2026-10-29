function getErrorMessage(response) {
  return response.json().then(function(data) {
    if (data && data.error) {
      if (typeof data.error === "string") {
        return data.error;
      }

      return JSON.stringify(data.error);
    }

    return "HTTP status: " + response.status;
  }).catch(function() {
    return "HTTP status: " + response.status;
  });
}

function getOneTimeUploadUrl(uploadEndpoint) {
  var url = document.location.origin + uploadEndpoint;

  return fetch(url).then(function(response) {
    if (!response.ok) {
      return getErrorMessage(response).then(function(message) {
        throw new Error(message);
      });
    }

    return response.json();
  });
}

function showError(element, message) {
  var error = element.querySelector(".ci-widget-error");

  if (error) {
    error.textContent = message || "";
  }
}

function setUploading(button, uploading) {
  if (! button) {
    return;
  }

  if (uploading) {
    button.dataset.defaultLabel = button.textContent;
    button.textContent = "Uploading...";
  } else {
    button.textContent = button.dataset.defaultLabel || "Upload";
  }

  button.disabled = uploading;
}

function clickListener(e, element, button) {
  e.preventDefault();

  var fileInput = element.querySelector("input[type='file']");
  var file = fileInput && fileInput.files ? fileInput.files[0] : null;

  showError(element, "");

  if (! file) {
    showError(element, "Please select an image.");
    return;
  }

  setUploading(button, true);

  getOneTimeUploadUrl(element.dataset.uploadEndpoint)
    .then(function(response) {
      if (! response.result || ! response.result.uploadURL) {
        throw new Error("Cloudflare did not return an upload URL.");
      }

      var data = new FormData();
      data.append("file", file);

      return fetch(response.result.uploadURL, {
        method: "POST",
        body: data
      });
    })
    .then(function(response) {
      if (! response.ok) {
        return getErrorMessage(response).then(function(message) {
          throw new Error(message);
        });
      }

      return response.json();
    })
    .then(function(d) {
      if (! d.result || ! d.result.id) {
        throw new Error("Cloudflare did not return an image ID.");
      }

      var link = element.getElementsByTagName("a")[0];
      if (! link) {
        link = document.createElement("a");
        element.append(link);
      }

      if (element.dataset.signed === "true") {
        link.removeAttribute("href");
        link.removeAttribute("target");
        link.textContent = "Uploaded: " + d.result.id;
      } else {
        var variants = d.result.variants || [];
        if (variants[0]) {
          link.setAttribute("href", variants[0]);
        } else {
          link.removeAttribute("href");
        }
        link.setAttribute("target", "_blank");
        link.textContent = d.result.id;
      }

      var hiddenId = element.querySelector("input[type='hidden']");
      if (hiddenId) {
        hiddenId.value = d.result.id;
      }
    })
    .catch(function(err) {
      showError(element, err.message || "Upload failed.");
    })
    .finally(function() {
      setUploading(button, false);
    });
}

function setupUploadForm(element) {
  var button = element.querySelector("button");

  if (! button) {
    return;
  }

  button.addEventListener("click", function(e) {
    clickListener(e, element, button);
  });
}

window.addEventListener("DOMContentLoaded", function() {
  var elements = document.querySelectorAll(".ci-widget");

  for (var i = 0; i < elements.length; i++) {
    setupUploadForm(elements[i]);
  }
});
