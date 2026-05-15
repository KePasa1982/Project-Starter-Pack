import "./style.css";

const app = document.querySelector<HTMLDivElement>("#app")!;
app.innerHTML = `
  <main class="shell">
    <h1>{{PROJECT_TITLE}}</h1>
    <p class="lede">Starter is live. Replace this with your design.</p>
  </main>
`;
