$(document).ready(function()
{
  ShowMovies();
});

function ShowMovies()
{
  $.getJSON( "api/movies", function(data) 
  {
    var items = [];
    for(let i = 0; i < data.length; i++) 
    {
      let obj = data[i];
  
      html = '<div id="Movies"><ul><div class="p">';
      data.forEach(item => 
      {
        html = html + '<li>' + item.name+": " + item.addedBy + '</li>';
      });
      html = html + '</ul></div>';
      $("#Movies").html(html);
    };
  });
};

function PickRandomNumber()
{
  var movieData = {"name": name, "addedBy": addedBy};
  $.postJSON( "api/movies/random", movieData, function(randomMoviePicked) 
  {
    $("#ChosenMovie").html('<div class="p">' + '<p3>' + randomMoviePicked["name"] + '</p3>' + '</div>'); 
  });
};

function AddMovie()
{
  var x = document.getElementById("AddMovie");   
  if (x.style.display == "none") 
  {
    x.style.display = "block";
  } 
  else 
  {
    x.style.display = "none";
  };
};

$.postJSON = function(url, data, success, args) {
  args = $.extend({
    url: url,
    type: 'POST',
    data: JSON.stringify(data),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    async: true,
    success: success
  }, args);
  return $.ajax(args);
};

function SubmitFilm()
{
  var name = document.getElementById("nameOfMovie").value;
  var addedBy = document.getElementById("addedBy").value;
  var movieData = {"name": name, "addedBy": addedBy};
  $.postJSON( "api/movies", movieData, function(data) 
  {
    ShowMovies();
  });
};