import express from "express";
import { requireAuth } from "./middleware/auth";
import { errorHandler } from "./errors";
import { usersRouter } from "./routes/users";

export const app = express();

app.use(express.json());
app.get("/healthz", (_req, res) => res.json({ ok: true }));

app.use("/users", requireAuth, usersRouter);

app.use(errorHandler);
