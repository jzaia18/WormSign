function displayNum(e) {
  // get label id
  var labelId = e.target.name + "-displaynum";

  $("#"+labelId)[0].innerText = e.target.value;
}

$("#Servings-input")[0].oninput = displayNum;
$("#Difficulty-input")[0].oninput = displayNum;
