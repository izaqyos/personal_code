import request from "supertest";
import { app } from "../src/app";
import { auth, seed } from "./helpers";

describe("GET /users/:id", () => {
  it("returns a user in the caller's tenant", async () => {
    const { userA } = await seed();
    const res = await request(app).get(`/users/${userA.id}`).set(auth(userA));
    expect(res.status).toBe(200);
    expect(res.body.id).toBe(userA.id);
  });

  it("returns 404 for a user in another tenant", async () => {
    const { userA, userB } = await seed();
    const res = await request(app).get(`/users/${userB.id}`).set(auth(userA));
    expect(res.status).toBe(404);
  });

  it("returns 401 without a token", async () => {
    const res = await request(app).get("/users/00000000-0000-0000-0000-000000000000");
    expect(res.status).toBe(401);
  });
});
