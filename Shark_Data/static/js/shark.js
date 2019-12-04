async function makeResponsive() {

    // if the SVG area isn't empty when the browser loads,
    // remove it and replace it with a resized version of the chart
    const svgArea = d3.select("body").select("svg");

    // clear svg is not empty
    if (!svgArea.empty()) {
        svgArea.remove();
    }

    // SVG wrapper dimensions are determined by the current width and
    // height of the browser window.

    
    const svgWidth = document.getElementById('shell').offsetWidth;

  //  const svgWidth = window.innerWidth;
    const svgHeight = window.innerHeight;

// const svgWidth = 1594;
// const svgHeight = 830;

const margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

const width = svgWidth - margin.left - margin.right;
const height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
const svg = d3
  .select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append an SVG group
const chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Initial Params
var chosenXAxis = "ask";

// function used for updating x-scale const upon click on axis label
function xScale(sharkData, chosenXAxis) {
  // create scales
  const xLinearScale = d3.scaleLinear()
    .domain([d3.min(sharkData, d => d[chosenXAxis]) * 0.8,
      d3.max(sharkData, d => d[chosenXAxis]) * 1.2
    ])
    .range([0, width]);

  return xLinearScale;

}

// function used for updating xAxis const upon click on axis label
function renderAxes(newXScale, xAxis) {
  const bottomAxis = d3.axisBottom(newXScale);

  xAxis.transition()
    .duration(1000)
    .call(bottomAxis);

  return xAxis;
}

// function used for updating circles group with a transition to
// new circles
function renderCircles(circlesGroup, newXScale, chosenXaxis, data) {



    var sel = circlesGroup.data(data).exit().remove();

    circlesGroup
    .enter()
    .append("circle")
    .attr("cx", d => xLinearScale(d[chosenXAxis]))
    .attr("cy", d => yLinearScale(d.stake))
    .attr("r", 8)
    .attr("fill", "lightblue")
    .attr("stroke", "black")
    .attr("opacity", ".5")
    .merge(circlesGroup);
    

  circlesGroup.transition()
    .duration(1000)
    .attr("cx", d => newXScale(d[chosenXAxis]));

  return circlesGroup;
}

// function redrawCircles(circlesGroup, newXScale, chosenXaxis, data) {

//     circlesGroup.data(data)
//         .enter()
//         .append("circle")
//         .attr("cx", d => xLinearScale(d[chosenXAxis]))
//         .attr("cy", d => yLinearScale(d.stake))
//         .attr("r", 8)
//         .attr("fill", "lightblue")
//         .attr("stroke", "black")
//         .attr("opacity", ".5")
//         .merge(circlesGroup)
//         .exit()
//      .remove();

//   circlesGroup.transition()
//     .duration(1000)
//     .attr("cx", d => newXScale(d[chosenXAxis]));

//   return circlesGroup;
// }

// function used for updating circles group with new tooltip
function updateToolTip(chosenXAxis, circlesGroup) {
    let label  = "";
    if (chosenXAxis === "ask") {
        label = "Deal Values ($):";
    }
    else {
        label = "Valuations ($):";
    }

    const toolTip = d3.tip()
        .attr("class", "tooltip")
        .offset([80, -60])
        .html(function(d) {
            return (`Stake: ${d.stake}<br>${label} ${d[chosenXAxis]}<br>${d.deal}`);
        });

    circlesGroup.call(toolTip);

    circlesGroup.on("mouseover", function(data) {
        toolTip.show(data, this);
    })
    // onmouseout event
    .on("mouseout", function(data, index) {
        toolTip.hide(data, this);
    });

  return circlesGroup;
}



// Retrieve data from the CSV file and execute everything below
(async function(){
    const sharkData = await d3.json("/sharks");

    // parse data
    sharkData.forEach(function(data) {
        data.ask = +data.ask;
        data.valuation = +data.valuation;
        data.stake = +data.stake;
    });

    // xLinearScale function above csv import
    var xLinearScale = xScale(sharkData, chosenXAxis);

    // Create y scale function
    const yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(sharkData, d => d.stake)])
        .range([height, 0]);

    // Create initial axis functions
    const bottomAxis = d3.axisBottom(xLinearScale);
    const leftAxis = d3.axisLeft(yLinearScale);

    // append x axis
    var xAxis = chartGroup.append("g")
        .classed("x-axis", true)
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);

    // append y axis
    chartGroup.append("g")
        .call(leftAxis);

    // append initial circles
    let circlesGroup = chartGroup.selectAll("circle")
        .data(sharkData)
        .enter()
        .append("circle")
        .attr("cx", d => xLinearScale(d[chosenXAxis]))
        .attr("cy", d => yLinearScale(d.stake))
        .attr("r", 8)
        .attr("fill", "lightblue")
        .attr("stroke", "black")
        .attr("opacity", ".5")

    // Create group for  2 x- axis labels
    const labelsGroup = chartGroup.append("g")
        .attr("transform", `translate(${(width - 100) / 2}, ${height + 40})`);

    const dealLabel = labelsGroup.append("text")
        .attr("x", 0)
        .attr("y", 15)
        .attr("value", "ask") // value to grab for event listener
        .classed("active", true)
        .text("Value of each Deal ($)");

    const valLabel = labelsGroup.append("text")
        .attr("x", 0)
        .attr("y", 35)
        .attr("value", "valuation") // value to grab for event listener
        .classed("inactive", true)
        .text("Valuation of pitch ($)");

    // append y axis
    chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 40 - margin.left)
        .attr("x", -30 - (height / 2))
        .attr("dy", "1em")
        .classed("axis-text", true)
        .text("Stake Offered (%)");

    // updateToolTip function above csv import
    circlesGroup = updateToolTip(chosenXAxis, circlesGroup);

    // x axis labels event listener
    labelsGroup.selectAll("text")
        .on("click", function() {
        // get value of selection
        const value = d3.select(this).attr("value");
        if (value !== chosenXAxis) {

            // replaces chosenXAxis with value
            chosenXAxis = value;

            // console.log(chosenXAxis)

            // functions here found above csv import
            // updates x scale for new data
            xLinearScale = xScale(sharkData, chosenXAxis);

            // updates x axis with transition
            xAxis = renderAxes(xLinearScale, xAxis);

            // updates circles with new x values
            circlesGroup = renderCircles(circlesGroup, xLinearScale, chosenXAxis, sharkData);

            // updates tooltips with new info
            circlesGroup = updateToolTip(chosenXAxis, circlesGroup);

            // changes classes to change bold text
            if (chosenXAxis === "ask") {
                dealLabel
                    .classed("active", true)
                    .classed("inactive", false);
                valLabel
                    .classed("active", false)
                    .classed("inactive", true);
            }
            else {
                dealLabel
                    .classed("active", false)
                    .classed("inactive", true);
                valLabel
                    .classed("active", true)
                    .classed("inactive", false);
            }
        }
    
        d3.select("#low").property("value", d3.min(sharkData, d => d[chosenXAxis]));
        d3.select("#high").property("value", d3.max(sharkData, d => d[chosenXAxis]));

    })

    const submit = d3.select("#apply");
    submit.on("click", applyFilters)
    
    function applyFilters() {
        d3.event.preventDefault();
        console.log("clicked!");
        const filterParams = {};
        filterParams.low = d3.select("#low").property("value");
        filterParams.high = d3.select("#high").property("value");
        filterParams.deal = "Deal Made";
        filterParams.nodeal = "No Deal Made";
        // filterParams.shape = d3.select("#shape").property("value").toLowerCase();

        var sharkData2 = sharkData;

        if (chosenXAxis === "ask") { 
            if (filterParams.low != "") {sharkData2 = sharkData2.filter(d => d.ask > filterParams.low)};
            if (filterParams.high != "") {sharkData2 = sharkData2.filter(d => d.ask < filterParams.high)};
        }
        else {
            if (filterParams.low != "") {sharkData2 = sharkData2.filter(d => d.valuation > filterParams.low)};
            if (filterParams.high != "") {sharkData2 = sharkData2.filter(d => d.valuation < filterParams.high)};
        }

        if (d3.select("#made").classed("active") && !d3.select("#rejected").classed("active")) {
            
            
            sharkData2 = sharkData2.filter(function(d) {
                 return d.deal === filterParams.deal;
                
            })
            // if (circlesGroup.attr("Deal") == "No Deal Made") {
            //     circlesGroup.remove()
            // }
            console.log(sharkData2)
        }

        if (!d3.select("#made").classed("active") && d3.select("#rejected").classed("active")) {
            sharkData2 = sharkData2.filter(d => d.deal === filterParams.nodeal);
            console.log(sharkData2)
        }

        var sharks = ["Barbara Corcoran", "Robert Herjavec", "Kevin O'Leary", "Mark Cuban", "Daymond John", "Lori Greiner"]

        if (d3.select("#barb").classed("img-border")) {
            sharks = arrayRemove(sharks, "Barbara Corcoran")
        }

        if (d3.select("#rob").classed("img-border")) {
            sharks = arrayRemove(sharks, "Robert Herjavec")
        }

        if (d3.select("#kevin").classed("img-border")) {
            sharks = arrayRemove(sharks, "Kevin O'Leary")
        }

        if (d3.select("#cuban").classed("img-border")) {
            sharks = arrayRemove(sharks, "Mark Cuban")
        }

        if (d3.select("#daymond").classed("img-border")) {
            sharks = arrayRemove(sharks, "Daymond John")
        }

        if (d3.select("#lori").classed("img-border")) {
            sharks = arrayRemove(sharks, "Lori Greiner")
        }

        console.log(sharks)
        sharkData2 = sharkData2.filter(function(el) {
            return (sharks.indexOf(el.dealshark1) >= 0) ||
                (sharks.indexOf(el.dealshark2) >= 0) ||
                (sharks.indexOf(el.dealshark3) >= 0) ||
                (sharks.indexOf(el.dealshark4) >= 0) ||
                (sharks.indexOf(el.dealshark5) >= 0);
        });
        console.log(sharkData2)
        
        
    
        // updates x scale for new data
        xLinearScale = xScale(sharkData2, chosenXAxis);

        // updates x axis with transition
        xAxis = renderAxes(xLinearScale, xAxis);

        // updates circles with new x values
        circlesGroup = renderCircles(circlesGroup, xLinearScale, chosenXAxis, sharkData2);

        // updates tooltips with new info
        circlesGroup = updateToolTip(chosenXAxis, circlesGroup);

    }
})()
}

// When the browser loads, makeResponsive() is called.
makeResponsive();

// When the browser window is resized, makeResponsive() is called.
d3.select(window).on("resize", makeResponsive);