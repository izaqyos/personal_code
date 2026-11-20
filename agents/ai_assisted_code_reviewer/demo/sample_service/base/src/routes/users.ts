import { Router } from "express";
import { z } from "zod";
import { db } from "../db";
import { HttpError } from "../errors";

export const usersRouter = Router();

const Params = z.object({ id: z.string().uuid() });

usersRouter.get("/:id", async (req, res, next) => {
  try {
    const { id } = Params.parse(req.params);
    const [user] = await db.query<{ id: string; name: string }>(
      "SELECT id, name FROM users WHERE id = $1 AND tenant_id = $2",
      [id, req.user.tenantId],
    );
    if (!user) return next(new HttpError(404, "not found"));
    res.json(user);
  } catch (e) {
    next(e);
  }
});
