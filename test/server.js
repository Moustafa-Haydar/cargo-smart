import 'dotenv/config';
import { createServer } from 'http';
import app from './src/app.js';

const PORT = process.env.PORT || 3000;
const server = createServer(app);

server.listen(PORT, () => {
  console.log(`🚀 API ready at http://localhost:${PORT}`);
});
