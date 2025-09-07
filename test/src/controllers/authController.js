import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { query } from '../utils/db.js';

export const login = async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password are required' });
        }

        // Get user from database
        const result = await query(
            'SELECT * FROM accounts_user WHERE username = $1',
            [username]
        );

        const user = result.rows[0];

        if (!user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // For now, accepting any password for testing
        // TODO: Implement proper password verification
        // const isPasswordValid = await bcrypt.compare(password, user.password);
        // if (!isPasswordValid) {
        //     return res.status(401).json({ error: 'Invalid credentials' });
        // }

        // Generate JWT token
        const token = jwt.sign(
            {
                id: user.id,
                username: user.username,
                email: user.email
            },
            process.env.JWT_SECRET || 'default-secret',
            { expiresIn: '24h' }
        );

        return res.json({
            token,
            user: {
                id: user.id,
                username: user.username,
                email: user.email
            }
        });

    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Server error' });
    }
};

export const verify = (req, res) => {
    res.json({ valid: true, user: req.user });
};

export const getProfile = async (req, res) => {
    try {
        const result = await query(
            'SELECT * FROM accounts_user WHERE id = $1',
            [req.user.id]
        );

        const user = result.rows[0];

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({
            user: {
                id: user.id,
                username: user.username,
                email: user.email
            }
        });
    } catch (error) {
        console.error('Profile error:', error);
        res.status(500).json({ error: 'Server error' });
    }
};