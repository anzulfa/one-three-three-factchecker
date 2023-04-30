function myFunction(response) {
    document.getElementById("loader-container").style.display = "none"
    document.getElementById("result-container").style.display = "block"
    document.getElementById("result-grade").innerHTML = response.grade;
    console.log(response)
    console.log(response.accuratePoints[0])
}

async function fetchData() {
    // let response1=await fetch ("http://103.82.93.200:8081/check-fact", {
    //     method: "POST",
    //     headers: {
    //       'Accept': '*/*',
    //       'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify(
    //         {
    //             pageUrl: "https://edition.cnn.com/2021/06/09/tech/robot-zaps-weeds-spc-intl/index.html"
    //         }
    //     )
    // })
    //     .then(response1 => response1.json())
    //     .then(response1Json => console.log(response1Json));

    await fetch ("http://127.0.0.1:5000/getisfact/")
        .then(response => response.json())
        .then(responseJson => this.myFunction(responseJson))
 
}

fetchData();