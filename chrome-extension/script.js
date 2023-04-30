async function fetchData(pageUrl) {
    let response=await fetch ("http://103.82.93.200:8081/check-fact", {
        method: "POST",
        headers: {
          'Accept': '*/*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                pageUrl: pageUrl
            }
        )
    })
        .then(response => response.json())
        .then(responseJson => this.displayResult(responseJson));
}

function displayResult(response) {
    var score = parseInt(response.result.score)
    var pie = document.getElementById("pie-score")
    pie.style.setProperty('--p', score <= 0 ? 3 : score)
    pie.style.setProperty('--c', score == 100 ? "rgb(144, 247, 144)" : (score > 0 ? "rgb(255, 236, 113)" : "rgb(255, 108, 108)"))

    document.getElementById("loader-container").style.display = "none"
    document.getElementById("result-container").style.display = "block"
    document.getElementById("result-score").innerHTML = score.toString().concat('%')
    document.getElementById("result-final").style.color = score == 100 ? "#48b31b" : (score > 0 ? "#d6a11a" : "darkred");
    document.getElementById("result-grade").innerHTML = score == 100 ? "correct" : 
        (score > 0 ? "partially Correct" : "either incorrect or not available for facts analysis"); 
    document.getElementById("result-summary").innerHTML = response.result.summary;

    var processChainList = document.getElementById("result-process-chain-list")
    for (let i = 0; i < response.result.processChain.length; i++) {
        var entry = document.createElement('li');

        var obsv = document.createElement('span');
        obsv.classList.add("font-bold")
        obsv.appendChild(document.createTextNode("Observation: "))
        var obsvContent = document.createElement('p');
        obsvContent.appendChild(document.createTextNode(response.result.processChain[i].observation))
        obsvContent.classList.add("no-margin")
        entry.appendChild(obsv);
        entry.appendChild(obsvContent);

        var thought = document.createElement('span');
        thought.classList.add("font-bold")
        thought.appendChild(document.createTextNode("Thought: "))
        var thoughtContent = document.createElement('p');
        thoughtContent.appendChild(document.createTextNode(response.result.processChain[i].thought))
        thoughtContent.classList.add("no-margin")
        entry.appendChild(thought);
        entry.appendChild(thoughtContent);

        processChainList.appendChild(entry);
    }
}

function getCurrentTabUrl(callback) {  
    var queryInfo = {
      active: true, 
      currentWindow: true
    };
  
    chrome.tabs.query(queryInfo, function(tabs) {
      var tab = tabs[0]; 
      var url = tab.url;
      callback(url);
    });
}
  
document.addEventListener('DOMContentLoaded', function() {
    getCurrentTabUrl(function(url) {
        fetchData(url); 
    });
});
fetchData();