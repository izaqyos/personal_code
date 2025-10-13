const puppeteer = require('puppeteer');
const { TeamsContext, TeamsSdkClient } = require('microsoft-teams-clientsdk');

async function sendMessage(message) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Set up the Teams context
  const context = new TeamsContext(page);
  await context.initialize();

  // Use the Teams SDK client to send the message
  const client = new TeamsSdkClient(context);
  await client.initialize();

  await client.tasks.submitTask({ text: message });

  await browser.close();
}

async function handleIncomingMessage(message) {
  // Handle the incoming message
  console.log('Received Message:', message);
}

async function main() {
  // Set up an event listener to handle incoming messages
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const context = new TeamsContext(page);
  await context.initialize();

  context.tasks.registerOnTaskModuleMessage(async (event) => {
    const message = event.message;
    await handleIncomingMessage(message);
  });

  // Continuously run the Node.js application
  // This will keep the event listener active
  await new Promise(() => {});
}

main().catch(console.error);

