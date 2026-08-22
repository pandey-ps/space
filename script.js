const h = document.querySelector(".clock-h");
const m = document.querySelector(".clock-m");
const ap = document.querySelector(".clock-ap");

function tick() {
  const now = new Date();
  let hours = now.getHours() % 12;
  if (hours === 0) hours = 12;
  h.textContent = hours;
  m.textContent = String(now.getMinutes()).padStart(2, "0");
  ap.textContent = now.getHours() >= 12 ? "pm" : "am";
}

tick();
setInterval(tick, 1000);

/* ---- player ---- */
const audio = new Audio();
let idx = 0;
let seeking = false;
let shuffle = true;
const history = [];

const playerEl = document.querySelector(".player");
const artEl = document.querySelector(".player-art");
const titleEl = document.querySelector(".player-title");
const artistEl = document.querySelector(".player-artist");
const barEl = document.querySelector(".player-bar");
const tCurEl = document.querySelector(".player-t-cur");
const tDurEl = document.querySelector(".player-t-dur");
const playBtn = document.querySelector(".pc-play");
const prevBtn = document.querySelector(".pc-prev");
const nextBtn = document.querySelector(".pc-next");
const shuffleBtn = document.querySelector(".pc-shuffle");

shuffleBtn.classList.add("on");

function nextIndex() {
  if (!shuffle || TRACKS.length < 2) return idx + 1;
  let n;
  do {
    n = Math.floor(Math.random() * TRACKS.length);
  } while (n === idx);
  return n;
}

function fmt(ms) {
  const s = Math.round(ms / 1000);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

function load(i, autoplay, pushHist) {
  if (pushHist && audio.src) history.push(idx);
  idx = ((i % TRACKS.length) + TRACKS.length) % TRACKS.length;
  const t = TRACKS[idx];
  artEl.src = t.cover;
  titleEl.textContent = t.title;
  artistEl.textContent = t.artist;
  tDurEl.textContent = fmt(Math.min(t.duration, 30000));
  audio.src = t.preview;
  if (autoplay) play();
}

function play() {
  if (!audio.src) load(idx, false, false);
  audio.play();
}

playBtn.addEventListener("click", () => {
  if (audio.paused) play();
  else audio.pause();
});

prevBtn.addEventListener("click", () => {
  if (audio.currentTime > 3) audio.currentTime = 0;
  else if (history.length) load(history.pop(), true, false);
  else load(idx - 1, true, false);
});

nextBtn.addEventListener("click", () => load(nextIndex(), true));

shuffleBtn.addEventListener("click", () => {
  shuffle = !shuffle;
  shuffleBtn.classList.toggle("on", shuffle);
});

barEl.addEventListener("input", () => {
  seeking = true;
  if (audio.duration) {
    tCurEl.textContent = fmt((barEl.value / 1000) * audio.duration * 1000);
  }
});

barEl.addEventListener("change", () => {
  if (audio.duration) audio.currentTime = (barEl.value / 1000) * audio.duration;
  seeking = false;
});

audio.addEventListener("play", () => playerEl.classList.add("playing"));
audio.addEventListener("pause", () => playerEl.classList.remove("playing"));

audio.addEventListener("timeupdate", () => {
  if (!seeking && audio.duration) {
    barEl.value = (audio.currentTime / audio.duration) * 1000;
    tCurEl.textContent = fmt(audio.currentTime * 1000);
  }
});

audio.addEventListener("ended", () => load(nextIndex(), true));

load(0, false, false);