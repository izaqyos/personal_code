import { config } from "../config";
import { logger } from "../logger";

interface Invoice {
  id: string;
  customer_id: string;
}

async function sendReminder(inv: Invoice): Promise<void> {
  const res = await fetch("https://api.stripe.com/v1/invoices/" + inv.id + "/send", {
    method: "POST",
    headers: { Authorization: `Bearer ${config.stripeKey}` },
  });
  if (!res.ok) throw new Error(`stripe ${res.status}`);
}

export async function sendReminders(invoices: Invoice[]): Promise<void> {
  invoices.forEach(async (inv) => {
    await sendReminder(inv);
    logger.info("reminder sent", { invoiceId: inv.id });
  });
}
