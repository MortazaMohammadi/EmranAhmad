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
function handleSelectChange(str) {
  // Get the select element
  const selectElement = document.getElementById("emp");

  // Check if a dynamically added input field exists
  let inputField = document.getElementById("dynamicInput");

  // Get the selected value
  const selectedValue = selectElement.value;

  // Check if the selected value is "یورو"
  if (selectedValue === "2") {
    // Check if the input field already exists
    if (!inputField) {
      // Create a new input element
      inputField = document.createElement("input");
      inputField.setAttribute("type", "number");
      inputField.className = "form-control";
      inputField.id = "dynamicInput";

      // Create a new column div
      const newColumnDiv = document.createElement("div");
      newColumnDiv.className = "col-lg-6 col-md-6 col-sm-12 p-2 fs-5";

      // Create a new paragraph element
      const paragraphElement = document.createElement("p");
      paragraphElement.className = "text-dark m-1";
      paragraphElement.innerHTML = '<i class="fa fa-list-alt text-danger px-2" aria-hidden="true"></i>'+ str;

      // Append the input element and paragraph element to the new column div
      newColumnDiv.appendChild(paragraphElement);
      newColumnDiv.appendChild(inputField);

      // Insert the new column div after the second column
      const secondColumn = document.querySelector("#reg .col-lg-6:nth-child(3)");
      secondColumn.parentNode.insertBefore(newColumnDiv, secondColumn.nextSibling);
    }
  } else {
    // Remove the dynamically added input field if it exists
    if (inputField) {
      inputField.parentNode.parentNode.removeChild(inputField.parentNode);
      inputField = null;
    }
  }
}
function selectPDF(containerId) {
  const container = document.getElementById(containerId);
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "application/pdf";
  fileInput.click();
  fileInput.addEventListener("change", function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
      const pdfData = e.target.result;
      const pdfObject = `<object data="${pdfData}" type="application/pdf" width="100%" height="100%"></object>`;
      container.innerHTML = pdfObject;
    };

    reader.readAsDataURL(file);
  });

  
}
function showOptions(inputValue) {
const inputField = document.getElementById("input-field");
const optionsList = document.getElementById("options-list");

// Array of select options
const selectOptions = [
  { value: "1", label: "قیس الفت" },
  { value: "2", label: "رضا محمدی" },
  // Add more options as needed
];

  // Clear the existing list items
  optionsList.innerHTML = "";

  // Filter select options based on input value
  const filteredOptions = selectOptions.filter((option) =>
    option.label.includes(inputValue)
  );

  // Display the options list if there are matches
  if (filteredOptions.length > 0) {
    optionsList.style.display = "block";

    // Create and append list items for each option
    filteredOptions.forEach((option) => {
      const listItem = document.createElement("li");
      listItem.textContent = option.label;
      listItem.addEventListener("click", function () {
        setInputValue(option.label);
      });
      optionsList.appendChild(listItem);
    });
  } else {
    optionsList.style.display = "none";
  }
  document.addEventListener("click", function (event) {
    if (!inputField.contains(event.target) && !optionsList.contains(event.target)) {
      optionsList.style.display = "none";
    }
  });
}

function setInputValue(value) {
  inputField.value = value;
  optionsList.style.display = "none";
  
}

// Close the options list when clicking outside the input field or list

