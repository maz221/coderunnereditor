
document.getElementById('code-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const code = document.getElementById('code').value;
    const language = document.getElementById('language').value;

    const response = await fetch('/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language })
    });

    const result = await response.json();
    document.getElementById('output').innerText = result.output;
});
