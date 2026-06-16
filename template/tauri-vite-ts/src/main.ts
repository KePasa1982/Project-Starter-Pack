import "./style.css";

const app = document.querySelector<HTMLDivElement>("#app")!;
app.innerHTML = `
  <main class="shell">
    <h1>{{PROJECT_TITLE}}</h1>
    <p class="lede">Desktop starter is live. Replace this with your design.</p>
    <p class="hint">Run <code>npm run tauri:dev</code> to open the native app window.</p>
  </main>
`;
