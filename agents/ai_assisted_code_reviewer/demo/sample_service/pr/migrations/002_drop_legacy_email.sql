-- up
ALTER TABLE users DROP COLUMN legacy_email;
CREATE INDEX idx_invoices_status ON invoices(status);
