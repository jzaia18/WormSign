function displayNum(e) {
  // get label id
  var labelId = e.target.name + "-displaynum";

  $("#"+labelId)[0].innerText = e.target.value;
}

function createIngredientsSubmission() {
  var ingredientsList = $("#selected-ingredients")[0];
  var ingredients = "[";

  Array.from(ingredientsList.children).forEach(
    ingredientDiv => {
      ingredients += ingredientDiv.id + ", ";
    }
  );

  $("#secret-ingredients-holder")[0].value = ingredients.substring(0, ingredients.length-2) + "]";
}

function removeSelectedIngredient(e) {
  console.log(e.target);
  var ingredientDiv = $("#"+e.target.name)[0];
  console.log(ingredientDiv);
  $("#selected-ingredients")[0].removeChild(ingredientDiv);
  createIngredientsSubmission();
}

function appendSelectedIngredient(e) {
  var ingredientDiv = document.createElement("div");

  ingredientDiv.id = e.target.id.split("-")[1];
  ingredientDiv.className = "selected-ingredient";
  ingredientDiv.innerText = e.target.innerText;


  var removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.className = "selected-ingredient-remove";
  removeButton.name = ingredientDiv.id;
  removeButton.onclick = removeSelectedIngredient;
  ingredientDiv.appendChild(removeButton);

  $("#ingredient-search-bar")[0].value = "";
  var searchResultsDiv = $("#search-results-wrapper")[0];
  while (searchResultsDiv.lastChild) {
    searchResultsDiv.removeChild(searchResultsDiv.lastChild);
  }
  $("#selected-ingredients")[0].appendChild(ingredientDiv);
  createIngredientsSubmission();
}

function handleQueryResults(dataStr) {
  var data = JSON.parse(dataStr);

  var results = document.createElement("div");
  for(var i = 0; i < data.length; i++) {
    var entry = document.createElement("div");
    entry.className = "search-result";
    entry.innerText = data[i][1];
    entry.id = "result-" + data[i][0];
    entry.onclick = appendSelectedIngredient;
    results.appendChild(entry);
  }

  var searchResultsDiv = $("#search-results-wrapper")[0];
  while (searchResultsDiv.lastChild) {
    searchResultsDiv.removeChild(searchResultsDiv.lastChild);
  }

  searchResultsDiv.appendChild(results);
}

function queryIngredients(e) {
  $.ajax({url: "/ingredientsearch",
          success: handleQueryResults,
          type: "POST",
          data: {
            ingredient_name: e.target.value
          }
  });
}

$("#Servings-input")[0].oninput = displayNum;
$("#Difficulty-input")[0].oninput = displayNum;
$("#ingredient-search-bar")[0].oninput = queryIngredients;
