/* Set this to the public HTTPS URL of your deployed FastAPI service. */
const API_BASE = window.DOREMON_API_URL || '';
async function apiPost(path, payload) {
  if (!API_BASE) throw new Error('Python backend is not connected yet.');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(API_BASE.replace(/\/$/, '') + path, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload), signal: controller.signal
    });
    if (!response.ok) throw new Error('Backend returned ' + response.status);
    return await response.json();
  } finally { clearTimeout(timer); }
}
async function askTeacher() {
  const input = document.querySelector('#problem');
  const suggestion = document.querySelector('#suggestion');
  const text = input.value.trim();
  if (text.length < 2) { suggestion.textContent = 'Ask me a question first!'; return; }
  suggestion.textContent = '🤖 Professor Pocky is thinking...';
  try {
    const answer = await apiPost('/api/ask', {question:text});
    suggestion.textContent = '🤖 ' + answer.reply + ' ' + answer.hint;
    if (typeof openGadget === 'function' && answer.gadget) {
      const btn = document.createElement('button');
      btn.textContent = 'Open ' + answer.gadget + ' gadget →';
      btn.onclick = () => openGadget(answer.gadget);
      suggestion.append(document.createElement('p'), btn);
    }
  } catch (error) {
    suggestion.textContent = '🤖 The Python teacher is offline. You can still explore all the gadgets below!';
  }
}
async function loadQuizFromBackend(topic='general') {
  const host = document.querySelector('#activity');
  host.innerHTML = '<p>Loading your quiz...</p>';
  try {
    const data = await apiPost('/api/quiz', {topic,count:5});
    let current = 0, score = 0;
    function show() {
      host.replaceChildren();
      if (current >= data.questions.length) {
        const heading=document.createElement('h3');
        heading.textContent='🎉 Your score: '+score+' / '+data.questions.length;
        const again=document.createElement('button');
        again.textContent='Play again';
        again.onclick=()=>loadQuizFromBackend(topic);
        host.append(heading,again);
        return;
      }
      const q=data.questions[current], title=document.createElement('h3');
      title.textContent='Question '+(current+1)+': '+q.question;
      host.append(title);
      const feedback=document.createElement('p');
      feedback.setAttribute('role','status');
      q.options.forEach((answer,i)=>{
        const button=document.createElement('button');
        button.textContent=answer;
        button.onclick=()=>{
          if(i===q.answer) score++;
          feedback.textContent=(i===q.answer?'Correct! ':'Keep learning! ')+q.explanation;
          host.querySelectorAll('button').forEach(b=>b.disabled=true);
          next.disabled=false;
        };
        host.append(button);
      });
      const next=document.createElement('button');
      next.textContent='Next →';next.disabled=true;
      next.onclick=()=>{current++;show()};
      host.append(feedback,next);
    }
    show();
  } catch(error) {
    host.innerHTML='<p>The Python quiz service is offline. Use the built-in Brain Boost questions instead.</p>';
    const b=document.createElement('button');b.textContent='Open Brain Boost';
    b.onclick=()=>openGadget('quiz');host.append(b);
  }
}
