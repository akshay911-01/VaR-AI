// main.js
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const ttsToggle = document.getElementById('ttsToggle');
const status = document.getElementById('status');

const API_STREAM_URL = (text) => `/stream?text=${encodeURIComponent(text)}`; // expects GET SSE

// TTS state
let ttsEnabled = true;
let currentUtterance = null;

// Append message utility
function appendMessage(text, who='bot', streaming=false){
  const d = document.createElement('div');
  d.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
  d.dataset.streaming = streaming ? '1' : '0';
  d.innerHTML = (who === 'user' ? `<b>You</b>: ` : `<b>Assistant</b>: `) + (streaming ? `<span class="stream-text">${escapeHtml(text)}</span>` : escapeHtml(text));
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
  return d;
}

function escapeHtml(s){ return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }

// Speech synthesis (browser TTS) - speak chunks as they arrive
function speakChunk(chunk){
  if (!ttsEnabled || !('speechSynthesis' in window)) return;
  
  // Stop any current speech
  if (currentUtterance) {
    window.speechSynthesis.cancel();
  }
  
  const utter = new SpeechSynthesisUtterance(chunk);
  // optional: pick a voice
  const voices = window.speechSynthesis.getVoices();
  if (voices && voices.length) utter.voice = voices.find(v=>v.lang.includes('en')) || voices[0];
  utter.rate = 1.0;
  utter.volume = 0.8;
  
  currentUtterance = utter;
  window.speechSynthesis.speak(utter);
}

// Streaming handler using EventSource (SSE)
function startStream(userText, botMsgElem){
  status.textContent = 'Streaming response...';
  const url = API_STREAM_URL(userText);
  const es = new EventSource(url, { withCredentials: false });

  // accumulate for fallback final
  let accumulated = '';

  es.onmessage = (e) => {
    const data = e.data;
    if (!data) return;

    if (data === '[END]'){
      status.textContent = 'Done';
      es.close();
      return;
    }
    // append token/chunk to the streaming element
    accumulated += data;
    const span = botMsgElem.querySelector('.stream-text');
    if (span) span.textContent = accumulated;
    else botMsgElem.querySelector('b').insertAdjacentHTML('afterend', `<span class="stream-text">${escapeHtml(accumulated)}</span>`);

    // optional: speak each chunk
    speakChunk(data);
    chat.scrollTop = chat.scrollHeight;
  };

  es.onerror = (err) => {
    console.error('SSE error', err);
    status.textContent = 'Connection error';
    es.close();
  };

  return es;
}

// Send message (text)
async function sendText(){
  const text = input.value.trim();
  if (!text) return;
  appendMessage(text, 'user');
  input.value = '';
  // create bot placeholder with streaming flag
  const botEl = appendMessage('', 'bot', true);
  // start SSE stream
  startStream(text, botEl);
}

// Basic Microphone STT using Web Speech API (client-side)
let recognition = null;
let listening = false;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'en-IN';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => { listening = true; micBtn.classList.add('active'); status.textContent = 'Listening...'; }
  recognition.onend = () => { listening = false; micBtn.classList.remove('active'); status.textContent = 'Idle'; }
  recognition.onerror = (e) => { console.error(e); status.textContent = 'Speech recognition error'; }

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    input.value = transcript;
    sendText();
  };
} else {
  micBtn.disabled = true;
  micBtn.title = 'Speech Recognition not supported in this browser';
}

// TTS Toggle functionality
function toggleTTS() {
  ttsEnabled = !ttsEnabled;
  
  if (ttsEnabled) {
    ttsToggle.textContent = '🔊';
    ttsToggle.classList.add('active');
    ttsToggle.classList.remove('disabled');
    ttsToggle.title = 'Text-to-Speech: ON (Click to disable)';
  } else {
    ttsToggle.textContent = '🔇';
    ttsToggle.classList.remove('active');
    ttsToggle.classList.add('disabled');
    ttsToggle.title = 'Text-to-Speech: OFF (Click to enable)';
    // Stop any current speech
    if (currentUtterance) {
      window.speechSynthesis.cancel();
    }
  }
}

// Initialize TTS toggle
function initTTSToggle() {
  if ('speechSynthesis' in window) {
    ttsToggle.style.display = 'block';
    ttsToggle.classList.add('active');
    ttsToggle.title = 'Text-to-Speech: ON (Click to disable)';
  } else {
    ttsToggle.style.display = 'none';
  }
}

// Event listeners
sendBtn.addEventListener('click', sendText);
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendText();
});
micBtn.addEventListener('click', () => {
  if (!recognition) return;
  if (listening) recognition.stop();
  else recognition.start();
});
ttsToggle.addEventListener('click', toggleTTS);

// Initialize everything
initTTSToggle();

// initial status
status.textContent = 'Idle';
