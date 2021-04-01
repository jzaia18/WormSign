function displayNum(e) {
  // get label id
  var labelId = e.target.name + "-displaynum";

  $("#"+labelId)[0].innerText = e.target.value;
}

function handleQueryResults(dataStr) {
  var data = JSON.parse(dataStr);

  var results = document.createElement("div");
  for(var i = 0; i < data.length; i++) {
    var entry = document.createElement("div");
    entry.className = "search-result";
    entry.innerText = data[i][1];
    entry.id = data[i][0];
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
