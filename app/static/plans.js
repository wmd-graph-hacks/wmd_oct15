const host = document.querySelector('#saved-learning');
const esc = s => String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function load() {
  try {
    const response = await fetch('/api/learning/plans', {credentials:'same-origin', signal:AbortSignal.timeout(15000)});
    if(response.status===401){location.assign('/login');return;}
    if(!response.ok)throw new Error('Your saved plans could not load.');
    const {plans} = await response.json();
    const active = plans.find(p=>!p.finished);
    const resume = active ? `<p class="welcome-label">PICK UP WHERE YOU LEFT OFF · WEEK ${active.next.week}</p><h2>${esc(active.next.title.replace(' — study lesson',''))}</h2><p class="muted">${esc(active.goal)} · About ${active.next.minutes} minutes</p><a class="continue-link" href="${esc(active.next.url)}">Continue learning ↗</a><p class="muted progress-label">${active.completed} of ${active.total} lessons studied</p><progress value="${active.completed}" max="${active.total}" aria-label="Lessons studied"></progress>`
      : `<p class="welcome-label">${plans.length?'NICE WORK':'YOUR NEXT STEP'}</p><h2>${plans.length?'You’ve studied every lesson in your saved plans.':'Give your next study session a direction.'}</h2><p class="muted">${plans.length?'Revisit a lesson, try its quiz, or choose your next learning goal.':'Enter a goal below, then approve a proposed plan to save it here.'}</p><button id="choose-goal">${plans.length?'Choose another goal':'Create my first plan'} ↗</button>`;
    host.innerHTML = `<div class="card resume-card">${resume}</div><div class="card saved-card"><h2>Saved study plans <span class="badge">${plans.length}</span></h2>${plans.length?plans.map(p=>`<details class="saved-plan"><summary>${esc(p.goal)} <span class="muted">${p.completed}/${p.total} studied${p.finished?' · Finished':''}</span></summary><ol>${p.items.map(i=>`<li><a href="${esc(i.url)}">${i.done?'✓ ':''}${esc(i.title.replace(' — study lesson',''))}</a><small>Week ${i.week} · ${i.minutes} min${i.done?' · Studied':''}</small></li>`).join('')}</ol></details>`).join(''):'<p class="muted">Your approved plans stay here across visits. Draft proposals are saved after you approve them.</p>'}</div>`;
    document.querySelector('#choose-goal')?.addEventListener('click',()=>{document.querySelector('#goal').focus();document.querySelector('#goal').scrollIntoView({behavior:'smooth',block:'center'});});
  } catch(error) {
    host.innerHTML='<div class="card"><p>Your saved plans are temporarily unavailable.</p><button id="retry-plans" class="ghost">Try again</button></div>';
    document.querySelector('#retry-plans').onclick=load;
  }
}
window.addEventListener('plans-updated',load);
load();
