document.getElementById("runButton").addEventListener("click", async function() {
    console.log("Run Button Clicked");

    try {
        const response = await fetch("https://your-render-app.com/run", {  // Replace with your Render URL
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: "print('Hello, World!')", language: "python" })
        });

        console.log("Response Status:", response.status);

        const data = await response.json();
        console.log("Response Data:", data);

        document.getElementById("output").innerText = data.output || "Error running code";
    } catch (error) {
        console.error("Fetch Error:", error);
        document.getElementById("output").innerText = "Network error!";
    }
});

