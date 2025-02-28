async function hacerPregunta() {
    let pregunta = document.getElementById("pregunta").value;
    
    let response = await fetch("/preguntar/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: pregunta })
    });

    let data = await response.json();
    document.getElementById("respuesta").innerText = data.respuesta;
}
