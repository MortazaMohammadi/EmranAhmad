// image input
function previewImage(event, imgs) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var img = document.getElementById(imgs);
    img.src = reader.result;
  };
  reader.readAsDataURL(input.files[0]);
}

function menubtn() {
  var menubar = document.querySelector('.menubar');
  var body = document.querySelector('.body');
  if (menubar.style.display === 'none') {
    menubar.style.display = 'block';
    body.style.marginRight = '181px';
  } else {
    menubar.style.display = 'none';
    body.style.marginRight = 0;
  }
}

function setInputValue(value) {
  inputField.value = value;
  optionsList.style.display = "none";
  
}

function printPdf(pdfUrl) {
  var printWindow = window.open(pdfUrl, '_blank');
  printWindow.onload = function() {
      printWindow.print();
  };
}

// Close the options list when clicking outside the input field or list

