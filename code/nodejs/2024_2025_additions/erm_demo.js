const fs = require('fs/promises');

class DisposableFile {
    constructor(filePath, mode) {
        this.filePath = filePath;
        this.mode = mode;
        this.fileHandle = null;
        console.log(`DisposableFile: Creating instance for ${filePath}`);
    }

    async open() {
        if (!this.fileHandle) {
            this.fileHandle = await fs.open(this.filePath, this.mode);
            console.log(`DisposableFile: Opened file handle for ${this.filePath}`);
        }
        return this.fileHandle;
    }

    // This is the key for async disposal
    async [Symbol.asyncDispose]() {
        if (this.fileHandle) {
            await this.fileHandle.close();
            console.log(`DisposableFile: Async disposed (closed) file handle for ${this.filePath}`);
            this.fileHandle = null; // Clear the handle after closing
        }
    }
}

async function readFileWithExplicitResourceManagement(filePath) {
    // The 'await using' declaration ensures DisposableFile.asyncDispose is called
    await using file = new DisposableFile(filePath, 'r');
    const handle = await file.open();
    const content = await handle.readFile({ encoding: 'utf8' });
    console.log("File content (ERM):", content.substring(0, 50) + '...');
    return content;
    // When this function scope exits, `file[Symbol.asyncDispose]()` is automatically awaited.
}

// --- Example Usage ---

// Create a dummy file for demonstration
(async () => {
    const dummyFilePath = 'temp_erm_file.txt';
    await fs.writeFile(dummyFilePath, 'This is some sample content for the Explicit Resource Management demonstration. It is a longer string to show substring.');

    console.log('\n--- Running readFileWithExplicitResourceManagement ---');
    try {
        await readFileWithExplicitResourceManagement(dummyFilePath);
    } catch (error) {
        console.error("Error during ERM file read:", error);
    } finally {
        // Clean up the dummy file
        await fs.unlink(dummyFilePath);
        console.log(`\nCleaned up ${dummyFilePath}`);
    }

    console.log('\n--- Demonstrating synchronous `using` ---');

    class SyncResource {
        constructor(id) {
            this.id = id;
            console.log(`SyncResource ${this.id}: Created`);
        }

        [Symbol.dispose]() {
            console.log(`SyncResource ${this.id}: Synchronously disposed`);
        }
    }

    function useSyncResource() {
        using res1 = new SyncResource(1);
        console.log('Inside useSyncResource function, after res1 creation');
        // When this function exits, res1[Symbol.dispose]() is automatically called.
    }

    useSyncResource();
    console.log('Outside useSyncResource function, after its call.');

})();
