import express, { Application, Request, Response } from 'express';
import userRoutes from './routes/users';
import { connectDatabase } from './config/database';
import morgan from 'morgan';

const app: Application = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(morgan('combined'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rotas
app.use('/', userRoutes);

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({ 
    status: 'healthy',
    service: 'Node.js Users API',
    timestamp: new Date().toISOString()
  });
});

// Iniciar servidor
const startServer = async () => {
  try {
    await connectDatabase();
    
    app.listen(PORT, () => {
      console.log(`🚀 Servidor Node.js rodando na porta ${PORT}`);
      console.log(`📊 Health check: http://localhost:${PORT}/health`);
    });
  } catch (error) {
    console.error('❌ Erro ao iniciar servidor:', error);
    process.exit(1);
  }
};

startServer();