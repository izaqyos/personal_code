const mermaid = require('mermaid');
const fs = require('fs');
const puppeteer = require('puppeteer');
const path = require('path');

const diagramDefinition = `
graph TD
    A[Start] --> B{Decision};
    B -- Yes --> C[Process 1];
    B -- No --> D[Process 2];
`;

(async () => {
    const browser = await puppeteer.launch({ headless: "new" }); // Use new headless mode
    const page = await browser.newPage();

    // Create a minimal HTML file to load Mermaid
    const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Mermaid Renderer</title>
      <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        window.mermaid = mermaid; // Expose mermaid to window
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
      </script>
    </head>
    <body>
      <div class="mermaid">${diagramDefinition}</div>
    </body>
    </html>
    `;

    const tempHtmlPath = path.join(__dirname, 'temp.html');
    fs.writeFileSync(tempHtmlPath, htmlContent);

    // Load the local HTML file
    await page.goto(`file://${tempHtmlPath}`, { waitUntil: 'domcontentloaded' });

    // Wait for Mermaid to be fully initialized
    await page.waitForFunction(() => {
      return window.mermaid && window.mermaid.parse && typeof window.mermaid.parse === 'function';
    });
    
    // 2. Render the diagram and get the SVG:
    const svg = await page.evaluate(async (diagramDefinition) => {
        // Render the diagram
        const { svg } = await window.mermaid.render('my-svg', diagramDefinition);
        return svg;
      }, diagramDefinition);

    // 3. Save the SVG to a file:
    fs.writeFileSync('diagram.svg', svg);

    console.log('Diagram generated: diagram.svg');
    await browser.close();

    // Clean up the temporary HTML file
    fs.unlinkSync(tempHtmlPath);
})();

