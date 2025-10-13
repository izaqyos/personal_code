const PgBoss = require('pg-boss');
const pg = require('pg');

const config = {
  // Use the values from docker-compose.yml
  host: 'localhost', // Or the IP address of your Docker host if not on Linux
  port: 5432,      // The port we mapped in docker-compose.yml
  user: 'myuser',      // POSTGRES_USER
  password: 'mypassword',  // POSTGRES_PASSWORD
  database: 'mydb',      // POSTGRES_DB

  // Connection pool settings
  min: 5,
  max: 20,
  // idleTimeoutMillis: 30000

  // ... other PgBoss specific options ...
};

const boss = new PgBoss(config);

boss.on('error', error => console.error(error));

async function startBoss() {
    try {
        await boss.start();
        console.log('PgBOS started successfully!');
        // Example: Add a job to the queue
        await boss.send('my-job', { data: 'some data' });
        console.log('Job added to queue');

         // Example: Consume the job (in a real app, this would be in a separate worker process)
         await boss.work('my-job', job => {
            console.log('Job received:', job.data);
            return Promise.resolve(); // Acknowledge the job
        });


    }
    catch(error) {
        console.error('Error starting PgBOS', error)
    }
}

startBoss();
