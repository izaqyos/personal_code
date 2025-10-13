const AdmZip = require('adm-zip'); // Install adm-zip: npm install adm-zip
const unzipper = require("unzipper");
const glob = require("glob");
const crypto = require("crypto");
const fs = require("fs");
const fsp = require("fs").promises;
const archiver = require("archiver");
const path = require("path");

async function printFile(filePath) {
  try {
    const fileData = await fsp.readFile(filePath, "utf-8");
    console.log(`${filePath} content:\n${fileData}`);
  } catch (error) {
    console.log("Error reading file", error);
  }
}

async function delete_files_noglob(filePattern) {
  //console.log(`got file pattern ${filePattern}`);
  const directoryPath = path.resolve();

  try {
    //console.log(`loading file in path ${directoryPath}`);
    const files = await fs.promises.readdir(directoryPath);

    const matchingFiles = files.filter((file) => {
      console.log(`checking ${file}`);
      const regex = new RegExp(filePattern.replace(/\*/g, ".*"));
      //console.log(`checking regex ${regex}`);
      return regex.test(file);
    });
    console.log(`files matching delete pattern ${matchingFiles}`);

    await Promise.all(
      matchingFiles.map((file) =>
        fs.promises.unlink(path.join(directoryPath, file))
      )
    );
    console.log("deleted all files");
  } catch (err) {
    console.error("Error reading directory:", err);
  }
}

function delete_files(filePattern) {
  return new Promise((res, rej) => {
    glob(filePattern, { cwd: path.resolve() }, (err, fileList) => {
      if (err) {
        rej(err);
        return;
      }
      const deletePromises = fileList.map((file) => {
        fs.unlink(path.join(path.resolve(), file));
        console.log(`deleted ${file}`);
      });
      Promise.all(deletePromises)
        .then(() => console.log("deleted all files"))
        .catch((delErr) => rej(delErr));
      res();
    });
  });
}

function delete_file(filePath) {
  fsp
    .access(filePath, fsp.constants.F_OK)
    .then(() => {
      console.log(`Deleting file ${filePath}`);
      return fsp.unlink(filePath);
    })
    .then(() => {
      console.log(` Successfully Deleted file ${filePath}`);
    })
    .catch((err) => {
      if (err.code === "ENOENT") {
        console.log(` ${filePath} doesn't exist`);
      } else {
        console.log(` ${filePath} can't delete`);
      }
    });
}

function generateChecksum(filePath, algorithm = "sha256") {
  console.log(`generating checksum for ${filePath}`);
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash(algorithm);
    const stream = fs.createReadStream(filePath);

    stream.on("error", (err) => reject(err));
    stream.on("data", (chunk) => hash.update(chunk));
    stream.on("end", () => resolve(hash.digest("hex")));
  });
}

async function zipFolder(folderPath) {
  console.log(`zipFolder(), zip ${folderPath}`);
  const folderPathTail = path.basename(folderPath);
  const zipFileName = `${folderPathTail}_${Date.now()}.zip`;
  const output = fs.createWriteStream(zipFileName);
  const archive = archiver("zip", { zlib: { level: 9 } });

  output.on("error", (err) => reject(err));

  return new Promise((resolve, reject) => {
    archive
      .directory(folderPath, false)
      .on("error", (err) => reject(err))
      .pipe(output);
    archive.on("end", () => {
      console.log(`zipFile() zip ${zipFileName} completed`);
      resolve(zipFileName);
    });
    archive.finalize();
  });
}

async function verifyChecksum(
  filePath,
  expectedChecksum,
  algorithm = "sha256"
) {
  const actualChecksum = await generateChecksum(filePath, algorithm);
  return actualChecksum === expectedChecksum;
}

// Example usage
const filePath = "your_zip_file.zip";

// generateChecksum(filePath)

//   .then(checksum => {
//     console.log(`Generated checksum: ${checksum}`);
//
//     // Store this checksum securely
//     // ...
//
//     // Later, when verifying the file:
//     verifyChecksum(filePath, checksum)
//       .then(isValid => {
//         if (isValid) {
//           console.log("File integrity verified!");
//         } else {
//           console.error("File has been tampered with!");
//         }
//       })
//       .catch(err => console.error('Error verifying checksum:', err));
//   })
//   .catch(err => console.error('Error generating checksum:', err));
//

async function test_external_checksum() {
  // zip, generate checksums, verify checksums unzip
  console.log("Testing external checksums...");

  const filePath = "mock_archive";
  //delete_file(filePath); // cleanup
  delete_files_noglob("mock_archive_*");
  const zipFileName = await zipFolder(filePath);

  let ret_sum = null;
  await generateChecksum(zipFileName).then((checksum) => {
    console.log(`Generated checksum: ${checksum}`);
    ret_sum = checksum;
  });
  console.log("Testing external checksums completed");
  return [ret_sum, zipFileName]; 
}

function insertStrIntoPath(fpath, str) {
  const dir = path.dirname(fpath);
  const extname = path.extname(fpath);
  const fname = path.basename(fpath, extname);
  return path.join(dir, `${fname}_${str}${extname}`);
}

async function generateAndSaveChecksum(zipFilePath, checksumFilePath) {
  console.log(
    `generateAndSaveChecksum() zip ${zipFilePath}, cksum file ${checksumFilePath}`
  );

  try {
    const finalZipFilePath = insertStrIntoPath(zipFilePath, "hex");
    const output = fs.createWriteStream(finalZipFilePath);
    const archive = archiver("zip", { zlib: { level: 9 } });

    console.log(
      "generateAndSaveChecksum - Create a PassThrough stream to calculate the checksum"
    );
    const hashStream = crypto.createHash("sha256");

    archive.on("error", (err) => {
      throw err;
    }); // Still throw errors from archiver

    // Pipe through the hash stream before writing to the archive
    archive.pipe(hashStream).pipe(output);
    // Stream existing entries and calculate checksum
    const parseStream = unzipper.Parse();

    console.log("generateAndSaveChecksum - process unzipped entries");
    parseStream.on('data', (chunk) => console.log(chunk.toString())); 

    //parseStream.on("entry", (entry) => {
    //  console.log("reading entry: ");
    //  console.dir(entry, { depth: 3, colors: true });
    //  console.log("-".repeat(100));
    //  if (entry.path !== checksumFilePath) {
    //    entry.pipe(hashStream, { end: false }); // Don't end the hash stream yet
    //    entry.pipe(archive.append(entry, { name: entry.path }));
    //  } else {
    //    entry.autodrain(); // Discard existing checksum file
    //  }
    //});

    await parseStream.promise();

    const checksum = hashStream.digest("hex");
    archive.append(checksum, { name: checksumFilePath });
    console.log(`Checksum: ${checksum}, checksumFilePath ${checksumFilePath} `);

    await archive.finalize();
    hashStream.end();

    console.log(
      `Checksum generated and saved to ${checksumFilePath} within the ZIP.`
    );
  } catch (err) {
    console.error("Error:", err);
  }
}

// async function generateAndSaveChecksum(zipFilePath, checksumFilePath) {
//     console.log(`generateAndSaveChecksum() zip ${zipFilePath}, cksum file ${checksumFilePath}`);
//   try {
//     const finalZipFilePath = insertStrIntoPath(zipFilePath, 'hex');
//     const output = fs.createWriteStream(finalZipFilePath);
//     const archive = archiver('zip', { zlib: { level: 9 } });
//     const hash = crypto.createHash('sha256');
//
//     archive.on('error', err => { throw err; });
//     archive.pipe(output);
//
//     // Stream existing entries and calculate checksum
//     fs.createReadStream(zipFilePath)
//       .pipe(unzipper.Parse())
//       .on('entry', entry => {
//         console.log('reading entry: ');
//         console.dir(entry, {depth: 3, colors: true});
//         console.log('-'.repeat(100));
//         if (entry.path !== checksumFilePath) {
//           entry.pipe(hash);
//           entry.pipe(archive.append('path', { name: entry.path }));
//         } else {
//           entry.autodrain(); // Discard existing checksum file
//         }
//       })
//       .on('error', err => {
//         if (err.message == 'FILE_ENDED') {
//           console.log('error, zip file incomplete or corrupt')
//         } else {
//           console.log('error processing zip', zip);
//         }
//       })
//       .promise()
//       .then(async () => {
//         const checksum = hash.digest('hex');
//         archive.append(checksum, { name: checksumFilePath });
//         await archive.finalize();
//         console.log(`Checksum generated and saved to ${checksumFilePath} within the ZIP.`);
//       })
//       .catch(err => console.error('Error:', err));
//   } catch (err) {
//     console.error('Error:', err);
//   }
// }

// this approach doesn't work, using private function of archiver :(
//async function generateAndSaveChecksum(zipFilePath, checksumFilePath) {
//  try {
//    console.log(`generateAndSaveChecksum() zip ${zipFilePath}, cksum file ${checksumFilePath}`);
//    const output = fs.createWriteStream(zipFilePath);
//    const archive = archiver("zip", { zlib: { level: 9 } });
//
//    const hash = crypto.createHash("sha256");
//    console.log(`generateAndSaveChecksum() archiver and hash created`);
//
//    archive.on("entry", (entry) => {
//      if (entry.name !== checksumFilePath) {
//        hash.update(entry.getData());
//      }
//    });
//
//    archive.on("error", (err) => {
//      throw err;
//    });
//
//    archive.pipe(output);
//
//    const existingZip = new archiver.ZipArchiveEntry(zipFilePath);
//    for (const entry of existingZip.entries.values()) {
//      if (entry.name !== checksumFilePath) {
//        archive.append(entry.getData(), { name: entry.name });
//      }
//    }
//
//    const checksum = hash.digest("hex");
//
//    printFile(checksumFilePath);
//    archive.append(checksum, { name: checksumFilePath });
//
//    await archive.finalize();
//
//    console.log(
//      `Checksum generated and saved to ${checksumFilePath} within the ZIP.`
//    );
//  } catch (err) {
//    console.error("Error:", err);
//  }
//}

async function test_internal_checksum() {
  console.log("Testing internal checksums...");

  const filePath = "mock_archive";
  delete_files_noglob("mock_archive_*");
  const zipFileName = await zipFolder(filePath);
  const cksFilePath = "cksum.txt";
  generateAndSaveChecksum(zipFileName, cksFilePath);

  console.log("Testing internal checksums completed");
}


async function addChecksumToZip(zipFilePath, checksumFilename = 'checksum.txt') {
    try {
        const hash = crypto.createHash('sha256');
        const zipData = await fs.promises.readFile(zipFilePath);
        hash.update(zipData);
        const checksum = hash.digest('hex');

        const checksumFilePath = zipFilePath.replace('.zip', `_${checksumFilename}`);
        await fs.promises.writeFile(checksumFilePath, checksum);

        const zip = new AdmZip(zipFilePath);
        zip.addLocalFile(checksumFilePath);

        zip.writeZip(zipFilePath); // Overwrites the original zip

        await fs.promises.unlink(checksumFilePath);

        console.log(`Checksum added to ${zipFilePath}`);
    } catch (error) {
        console.error('Error adding checksum:', error);
        throw error;
    }
}

async function main() {
  const [cksum, zipFileName] = await test_external_checksum();
  await addChecksumToZip(zipFileName,'checksum.txt');
  //test_internal_checksum();
}

main();
