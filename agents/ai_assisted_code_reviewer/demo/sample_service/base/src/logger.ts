type Fields = Record<string, unknown>;

function emit(level: string, msg: string, fields: Fields = {}) {
  process.stdout.write(JSON.stringify({ level, msg, ...fields, ts: new Date().toISOString() }) + "\n");
}

export const logger = {
  debug: (msg: string, f?: Fields) => emit("debug", msg, f),
  info: (msg: string, f?: Fields) => emit("info", msg, f),
  warn: (msg: string, f?: Fields) => emit("warn", msg, f),
  error: (msg: string, f?: Fields) => emit("error", msg, f),
};
