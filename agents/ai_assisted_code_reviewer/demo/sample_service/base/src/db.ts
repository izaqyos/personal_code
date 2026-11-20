import { Pool } from "pg";
import { config } from "./config";

const pool = new Pool({ connectionString: config.databaseUrl });

export const db = {
  /** Parameterized query — the only approved way to run SQL with input. */
  async query<T = Record<string, unknown>>(sql: string, params: unknown[] = []): Promise<T[]> {
    const res = await pool.query(sql, params);
    return res.rows as T[];
  },
  /** Raw SQL, no parameters. For static DDL/maintenance only. */
  async raw<T = Record<string, unknown>>(sql: string): Promise<T[]> {
    const res = await pool.query(sql);
    return res.rows as T[];
  },
};
