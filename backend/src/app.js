import dotenv from 'dotenv';
dotenv.config();
import express from "express";
import cors from "cors";
import { prisma } from './lib/prisma.js';
const app = express();
const PORT = process.env.PORT || 8000;
app.use(cors({ origin: "http://localhost:3000", credentials: true }));
app.use(express.json());
app.get("/", (req, res) => {
    res.json({ message: "Hello World" });
});
app.post('/users', async (req, res) => {
    try {
        const user = await prisma.user.create({
            data: {
                email: req.body.email,
                name: req.body.name,
                passwordHash: 'temp123' // We'll hash properly later
            }
        });
        res.json(user);
    }
    catch (error) {
        res.status(400).json({ error: error.message });
    }
});
// Error handler
app.use((err, req, res, next) => {
    console.error("Error:", err.message);
    res.status(500).json({ error: err.message });
});
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
//# sourceMappingURL=app.js.map