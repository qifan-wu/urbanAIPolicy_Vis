async function loadTopics() {
  const res = await fetch('/data/topic_index.json');
  const data = await res.json();
  const select = document.getElementById('topicSelect');
  Object.keys(data).forEach(topic => {
    const opt = document.createElement('option');
    opt.value = topic;
    opt.innerText = topic.replace(/_/g, ' ');
    select.appendChild(opt);
  });
}

async function showResults() {
  const topic = document.getElementById('topicSelect').value;
  const res = await fetch('/data/topic_index.json');
  const data = await res.json();
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  data[topic].forEach(entry => {
    const section = document.createElement('section');
    section.innerHTML = `
      <h3>${entry.title}</h3>
      <p><strong>Highlight:</strong> ${entry.highlight}</p>
      <a href="/pdfs/${entry.filename}" target="_blank">View PDF</a>
      <hr>`;
    resultsDiv.appendChild(section);
  });
}

document.addEventListener('DOMContentLoaded', loadTopics);
