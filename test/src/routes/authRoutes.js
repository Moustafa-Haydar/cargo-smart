import { Router } from 'express';
import { login, verify, getProfile } from '../controllers/authController.js';
import { verifyToken } from '../middleware/auth.js';

const router = Router();

router.post('/login', login);
router.get('/verify', verifyToken, verify);
router.get('/profile', verifyToken, getProfile);

export default router;