// const JSZip = import('jszip');
// const fs = import('fs');
import JSZip from 'jszip';
import fs from 'fs';


async function addFilesToZip(zip, basePath) {
  const files = await fs.promises.readdir(basePath);

  for (const file of files) {
    const fullPath = `${basePath}/${file}`;
    const stat = await fs.promises.stat(fullPath);

    if (stat.isDirectory()) {
      await addFilesToZip(zip.folder(file), fullPath);
    } else {
      const data = await fs.promises.readFile(fullPath);
      zip.file(file, data);
    }
  }
}
async function compressDirectory(directoryPath, zipFilePath) {
  const zip = new JSZip();
  await addFilesToZip(zip, directoryPath);
  const content = await zip.generateAsync({ type: 'nodebuffer' });
  await fs.promises.writeFile(zipFilePath, content);
}
compressDirectory(process.cwd(), process.cwd()+'/output.zip');


