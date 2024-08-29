var originalXHR = window.XMLHttpRequest;
window.XMLHttpRequest = function() {
  var xhr = new originalXHR();
  xhr.addEventListener('load', function() {
    console.log('XHR Response:', this.responseText);
  });
  return xhr;
};
