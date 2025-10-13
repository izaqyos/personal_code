require("dotenv").config();
const { GoogleGenerativeAI } = require("@google/generative-ai");

// Access your API key as an environment variable (see "Set up your API key" above)
const genAI = new GoogleGenerativeAI(process.env.API_KEY);

async function run() {
  // For embeddings, use the embedding-001 model
  const model = genAI.getGenerativeModel({ model: "embedding-001"});

  const text = "C++ is one of the best OOP languages. It is performant and versatile";
  const text2 = "Java is one of the best OOP languages. It is performant and versatile";

  const result = await model.embedContent(text);
  const embedding = result.embedding;
  const result2 = await model.embedContent(text2);
  const embedding2 = result2.embedding;
  console.log("Compare the embeddings (floating points numbers representing your text) of two similar sentences:")
  console.log(`first sentance ${text}`);
  console.log(`second sentance ${text2}`);
  console.log("The first embeddings are :");
  console.log(embedding.values);
  console.log("The second embeddings are :");
  console.log(embedding2.values);
  console.log("Note the similarity between these two sentences")
}

run();