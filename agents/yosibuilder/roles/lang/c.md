Language notes (C): compile clean with the card's warning flags; check every allocation and every return code;
no undefined behaviour (bounds, overflow, uninitialised reads, aliasing); free on every path; const for inputs;
static for file-local functions; errors as return codes, never exit() in library code.
