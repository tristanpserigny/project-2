function clickImg(x) {
    if (!d3.select(x).classed("img-border")) {
        d3.select(x).classed("img-border",true);
    }
    else {
        d3.select(x).classed("img-border",false);
    }
}

function arrayRemove(arr, value) {

    return arr.filter(function(ele){
        return ele != value;
    });
 
 }