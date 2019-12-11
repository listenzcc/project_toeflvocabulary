var query_word = 0
randomWord()

function randomWord() {
    d3.json("vocabulary5000_all_words.json").then(function(data) {
        // Random fetch word
        query_word = data[parseInt(d3.randomUniform(data.length)())]
        console.log(query_word)
    })
}

function checkout(word = query_word, delay = 2000) {
    // Setup objects
    d3.select("#QueryWord")
        .text(word)
    d3.select("#TransFrame")
        .style("visibility", "hidden")
        .attr("src", "https://cn.bing.com/dict/search?q=" + word)

    // Step for timer
    var line = d3.select("#TimerLine")
        .attr("x1", 0)
        .attr("y1", 20)
        .attr("x2", 300)
        .attr("y2", 20)

    line.transition()
        .duration(delay)
        .attr("x2", 0)

    // Draw answer after 5 seconds
    setTimeout(function() {
        d3.select("#TransFrame")
            .style("visibility", "visible")
    }, delay)
}

function filterWordButtons(val) {
    console.log(val)
    var wbs = d3.selectAll(".WordButton")._groups[0]
    wbs.forEach(function(d) {
        if (d.textContent.startsWith(val)) {
            d3.select(d).style("display", "")
        } else {
            d3.select(d).style("display", "none")
        }
    })
}

d3.json("vocabulary5000_all_words.json").then(function(data) {
    d3.select("#SideDiv")
        .append("div")
        .append("button")
        .text("[Random]")
        .attr("onclick", "randomWord(); checkout()")

    d3.select("#SideDiv")
        .append("input")
        .attr("id", "wordFilter")
        .attr("onchange", "filterWordButtons(this.value)")

    var div = d3.select("#SideDiv")
        .append("div")

    for (var i = 0; i < data.length; i++) {
        div.append("button")
            .text(data[i])
            .attr("class", "WordButton")
            .attr("onclick", "checkout(\"" + data[i] + "\", 100)")
    }
})