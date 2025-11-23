import { Request, Response } from 'express';
import User from '../models/User';

export class UserController {
  // POST /users - cria usuário
  async create(req: Request, res: Response): Promise<void> {
    try {
      const { name, email, username, password } = req.body;

      if (!name || !email || !username || !password) {
        res.status(400).json({ 
          error: 'Todos os campos são obrigatórios: name, email, username, password' 
        });
        return;
      }

      const newUser = await User.create({ name, email, username, password });
      res.status(201).json(newUser);
    } catch (error: any) {
      if (error.name === 'SequelizeUniqueConstraintError') {
        res.status(409).json({ error: 'Email ou username já cadastrado' });
        return;
      }
      console.error('Erro ao criar usuário:', error);
      res.status(500).json({ error: 'Erro ao criar usuário' });
    }
  }

  // GET /users - busca todos os usuários
  async list(req: Request, res: Response): Promise<void> {
    try {
      const users = await User.findAll({
        order: [['id', 'ASC']],
      });
      res.status(200).json(users);
    } catch (error) {
      console.error('Erro ao listar usuários:', error);
      res.status(500).json({ error: 'Erro ao listar usuários' });
    }
  }

  // GET /users/:id - busca usuario por ID
  async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await User.findByPk(id);

      if (!user) {
        res.status(404).json({ error: 'Usuário não encontrado' });
        return;
      }

      res.status(200).json(user);
    } catch (error) {
      console.error('Erro ao buscar usuário:', error);
      res.status(500).json({ error: 'Erro ao buscar usuário' });
    }
  }

  // PUT /users/:id - atualiza usuario
  async update(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const { name, email, username, password } = req.body;

      const userToUpdate = await User.findByPk(id);

      if (!userToUpdate) {
        res.status(404).json({ error: 'Usuário não encontrado' });
        return;
      }

      await userToUpdate.update({
        name: name || userToUpdate.name,
        email: email || userToUpdate.email,
        username: username || userToUpdate.username,
        password: password || userToUpdate.password,
      });

      res.status(200).json(userToUpdate);
    } catch (error: any) {
      if (error.name === 'SequelizeUniqueConstraintError') {
        res.status(409).json({ error: 'Email ou username já cadastrado' });
        return;
      }
      console.error('Erro ao atualizar usuário:', error);
      res.status(500).json({ error: 'Erro ao atualizar usuário' });
    }
  }

  // DELETE /users/:id - deleta usuario baseado no ID
  async delete(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await User.findByPk(id);

      if (!user) {
        res.status(404).json({ error: 'Usuário não encontrado' });
        return;
      }

      await user.destroy();
      res.status(204).send();
    } catch (error) {
      console.error('Erro ao deletar usuário:', error);
      res.status(500).json({ error: 'Erro ao deletar usuário' });
    }
  }
}