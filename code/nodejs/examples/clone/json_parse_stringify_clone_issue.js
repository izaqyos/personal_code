// Create an object with circular reference
const entityEntry = {
  name: "Entity1",
  details: {
    description: "This is an entity",
  },
};

// Create a circular reference
entityEntry.details.self = entityEntry;

try {
  // Attempt to clone the object with circular references
  const entityEntryClone = JSON.parse(JSON.stringify(entityEntry));
  console.log("Clone successful:", entityEntryClone);
} catch (error) {
  console.error("Error during cloning:", error.message);
}

