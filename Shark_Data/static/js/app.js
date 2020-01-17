
function fillForms(sample) {

    const title = document.getElementById('title');
    const cat = document.getElementById('cat');
    const val = document.getElementById('val');
    const ask = document.getElementById('ask');
    const stake = document.getElementById('stake');
    const pitch = document.getElementById('pitch');
      // Use `.html("") to clear any existing metadata
    title.value = sample.title;
    cat.value = sample.category
    val.value = sample.valuation
    ask.value = sample.ask
    stake.value = sample.exchange
    pitch.value = sample.description
};

function clearForms() {

    const title = document.getElementById('title');
    const cat = document.getElementById('cat');
    const val = document.getElementById('val');
    const ask = document.getElementById('ask');
    const stake = document.getElementById('stake');
    const pitch = document.getElementById('pitch');
      // Use `.html("") to clear any existing metadata
    title.value = "";
    cat.value = "";
    val.value = "";
    ask.value = "";
    stake.value = "";
    pitch.value = "";
};

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#userpitches");
    var cataselector = d3.select("#cat");
  
    // Use the list of sample names to populate the select options
    d3.json("/userpitches").then((inputs) => {
      inputs.forEach((input) => {
        console.log(input.title)
        selector
          .append("option")
          .text(input.title)
          .property("value", input.title);
      });
  
      // Use the first sample from the list to build the initial plots
    });

    const cats = ['Health / Wellness', 'Lifestyle / Home', 'Software / Tech',
   'Food and Beverage', 'Business Services',
   'Fashion / Beauty', 'Automotive', 'Media / Entertainment',
   'Fitness / Sports / Outdoor', 'Pet Products', 'Green / Clean Tech', 
   'Lifesytle / Home', 'Travel', 'Children / Education', 'Uncertain / Other'];

    cats.forEach((c) => {
        cataselector
        .append("option")
        .text(c)
        .property("value", c);
});
  }

  async function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    if (newSample == "New Pitch") {
        clearForms();
    } else {
    const inputdata = await d3.json("/userpitches/" + newSample)
    fillForms(inputdata[0]);
    }
  }

  function validateForm() {
    const alert = document.getElementById('alert');
    const intitle = document.forms["learn"]["title"].value.toLowerCase();
    const incata = document.forms["learn"]["cat"].value.toLowerCase();
    const inval = document.forms["learn"]["val"].value;
    const inask = document.forms["learn"]["ask"].value;
    const instake = document.forms["learn"]["stake"].value;
    const inpitch = document.forms["learn"]["pitch"].value.toLowerCase();
    const droplist = getUserList();
    

    if (intitle == "") {
      alert.style.display = "flex";
      alert.innerHTML = "You must enter a title";
      return false;
    }
    
    if (droplist.includes(intitle)) {
      alert.style.display = "flex";
      alert.innerHTML = "Title already exists";
      return false;
    }

    if (incata == "choose a category") {
        alert.style.display = "flex";
        alert.innerHTML = "You must choose a category";
        return false;
    }

    if (inval <= 0) {
        alert.style.display = "flex";
        alert.innerHTML = "The value of your company must be more than zero";
        return false;
    }

    if (inask <= 0) {
        alert.style.display = "flex";
        alert.innerHTML = "You must enter an asking amount";
        return false;
    }

    if (instake < 0 || instake > 100) {
        alert.style.display = "flex";
        alert.innerHTML = "You must enter a stake between 0 and 100";
        return false;
    }

    if (inpitch == "") {
        alert.style.display = "flex";
        alert.innerHTML = "You must enter a pitch description";
        return false;
    }


  }

  function getUserList() {
    const ddlArray= new Array();
    const ddl = document.getElementById('userpitches');
    for (i = 0; i < ddl.options.length; i++) {
        ddlArray[i] = ddl.options[i].value.toLowerCase();
    }

    return ddlArray;

  }

  init();