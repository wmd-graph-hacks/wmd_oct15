const button = document.querySelector('#google-sign-in');
const errorBox = document.querySelector('#auth-error');
const errors = {
  'auth/popup-closed-by-user': 'The sign-in window was closed. You can try again whenever you’re ready.',
  'auth/popup-blocked': 'Your browser blocked the sign-in window. Allow pop-ups for this site, then try again.',
  'auth/unauthorized-domain': 'Google sign-in is not configured for this address. Please use the app’s approved address.',
  'auth/network-request-failed': 'We couldn’t reach Google. Check your connection and try again.',
  'auth/cancelled-popup-request': 'A sign-in window is already open. Please finish there.',
};
try {
  const [{initializeApp}, firebase] = await Promise.all([
    import('https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js'),
    import('https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js'),
  ]);
  const config = JSON.parse(document.querySelector('#firebase-config').textContent);
  if (!config.apiKey || !config.projectId) throw new Error('Google sign-in is not configured yet.');
  const auth = firebase.getAuth(initializeApp(config));
  await firebase.setPersistence(auth, firebase.inMemoryPersistence);
  button.disabled = false;
  button.textContent = 'Continue with Google';
  button.addEventListener('click', async () => {
    button.disabled = true;
    button.textContent = 'Connecting to Google…';
    errorBox.textContent = '';
    try {
      const result = await firebase.signInWithPopup(auth, new firebase.GoogleAuthProvider());
      button.textContent = 'Opening your study space…';
      const idToken = await result.user.getIdToken();
      const response = await fetch('/auth/session', {
        method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type':'application/json'}, body: JSON.stringify({id_token:idToken}),
        signal: AbortSignal.timeout(20000),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'We couldn’t finish signing in. Please try again.');
      await firebase.signOut(auth);
      location.assign(data.next || '/agent');
    } catch (error) {
      errorBox.textContent = errors[error.code] || (error.name === 'TimeoutError' ? 'Sign-in took too long. Please try again.' : error.message || 'Sign-in failed. Please try again.');
      button.disabled = false;
      button.textContent = 'Continue with Google';
    }
  });
} catch (error) {
  errorBox.textContent = 'Secure sign-in could not load. Check your connection and reload this page.';
  button.textContent = 'Reload sign-in';
  button.disabled = false;
  button.onclick = () => location.reload();
}
