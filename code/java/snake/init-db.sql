CREATE TABLE IF NOT EXISTS player_scores (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster querying of top scores
CREATE INDEX IF NOT EXISTS idx_player_scores_score ON player_scores(score DESC);

-- Sample data (will be commented out in production)
-- INSERT INTO player_scores (player_name, score) VALUES 
--    ('Player1', 100),
--    ('Player2', 200),
--    ('Player3', 150); 