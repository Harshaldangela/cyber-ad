document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('backend');
  const save = document.getElementById('save');

  chrome.storage.sync.get(['cyberad_backend'], (res) => {
    input.value = res && res.cyberad_backend ? res.cyberad_backend : 'http://localhost:8007';
  });

  save.addEventListener('click', () => {
    const val = input.value.trim();
    chrome.storage.sync.set({ cyberad_backend: val }, () => {
      save.textContent = 'Saved!';
      setTimeout(() => (save.textContent = 'Save'), 1200);
    });
  });
});