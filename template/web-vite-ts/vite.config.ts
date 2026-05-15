import { defineConfig } from "vite";

export default defineConfig({
  root: ".",
  server: {
    // Unique per project (assigned at bootstrap). strictPort avoids serving the wrong app on a shared port.
    // Default 5200 for factory CI; bootstrap rewrites to a unique port per child project.
    port: 5200,
    strictPort: true,
    // Listen on all local interfaces so http://localhost:PORT and http://127.0.0.1:PORT both work
    // (default "localhost" alone can bind IPv6-only on some Linux setups).
    host: true,
    // Explicit local URL (with host: true, a bare boolean open can pick the wrong address on some setups).
    // Bootstrap rewrites the port per project. Set to false for SSH-only workflows.
    open: "http://127.0.0.1:5200/",
  },
});
