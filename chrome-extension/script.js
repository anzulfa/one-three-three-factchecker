async function fetchData() {
    let response=await fetch ("http://127.0.0.1:5000/getisfact/")
        .then(response => response.json());
    document.getElementById("result").innerHTML = response.message;
    console.log(response.message)
}
fetchData();