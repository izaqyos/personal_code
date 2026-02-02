# Microsoft Graph API Access Request

## ⚠️ UPDATED: You Need Azure Portal Access First

**Current Issue:** You don't have access to Azure Portal (Error 401), so you cannot create the app registration yourself.

**Two Options:**
1. **Request Azure Portal access** (so you can create and manage the app yourself)
2. **Ask admin to create the app for you** (faster, but less control)

---

## Option 1: Request Azure Portal Access (Recommended)

**Subject:** Request for Azure Portal Access

**Email Body:**

Hi [Admin Name],

I'm requesting access to Azure Portal to create a Microsoft Graph API app registration for AI assistant integration with my work email, calendar, and files through Cursor IDE.

**Current Issue:**
When I try to access Azure Portal (portal.azure.com), I get an "Access Denied" error (401).

**What I Need:**
- Access to Azure Portal
- Permission to create App Registrations in Microsoft Entra ID
- Ability to configure API permissions (with your approval)

**Why I Need This:**
I'm setting up an AI coding assistant (Cursor IDE) that integrates with Microsoft 365 to help me:
- Quickly search and reference emails during development
- Check my calendar availability when scheduling meetings
- Access project documents stored in OneDrive
- Look up team member contact information

This is similar to how Microsoft Copilot works, but integrated into my development environment.

**Security:**
- I'll only create app registrations for my personal use
- All API permissions will still require your admin consent
- I'll follow organizational security policies

Let me know if you'd prefer to create the app registration for me instead, or if you have any questions!

Thanks,
[Your Name]

---

## Option 2: Ask Admin to Create App for You (Faster)

**Subject:** Request: Create Microsoft Graph API App Registration

**Email Body:**

Hi [Admin Name],

I need a Microsoft Graph API app registration created for AI assistant integration with Outlook/Calendar/OneDrive through Cursor IDE.

Since I don't have Azure Portal access, could you create this for me?

**App Registration Specifications:**

**Basic Settings:**
- **App Name:** microsoft-mcp
- **Supported account types:** Accounts in this organizational directory only
- **Redirect URI:** None (uses device code flow)
- **Allow public client flows:** Yes (required for device code authentication)

**Required API Permissions (Microsoft Graph - Delegated):**
- `Mail.ReadWrite` - Read and manage my emails
- `Calendars.ReadWrite` - Read and manage my calendar events
- `Files.ReadWrite` - Read and manage my OneDrive files
- `Contacts.Read` - Read my contacts
- `People.Read` - Read directory information
- `User.Read` - Read my basic profile

**Setup Instructions for Admin:**

1. Go to Azure Portal → Microsoft Entra ID → App registrations
2. Click "New registration"
3. Name: `microsoft-mcp`
4. Supported account types: "Accounts in this organizational directory only"
5. Click "Register"
6. Go to "Authentication" → Advanced settings → Set "Allow public client flows" to "Yes"
7. Go to "API permissions" → Add permissions → Microsoft Graph → Delegated permissions
8. Add: Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite, Contacts.Read, People.Read, User.Read
9. Click "Grant admin consent for [Organization]"
10. Send me the Application (client) ID

**Why I Need This:**
AI assistant integration for productivity - search emails, check calendar, access OneDrive files during development.

### Security & Compliance

✅ **Delegated Permissions Only:** These permissions only work when I'm signed in - they're user-scoped, not tenant-wide

✅ **No Admin Access:** The app cannot access other users' data or make tenant-level changes

✅ **OAuth 2.0 Authentication:** Uses Microsoft's standard device code flow with token refresh

✅ **Open Source:** The MCP server is open source and auditable: https://github.com/elyxlz/microsoft-mcp

**After Creation:**
Please send me the Application (client) ID so I can complete the setup.

### Questions?

Happy to discuss any security concerns or provide additional details. I can also share the open-source code for the integration: https://github.com/elyxlz/microsoft-mcp

Thanks for your help!

Best regards,
[Your Name]

---

## Alternative: Slack/Teams Message Template

For a quick message:

```
Hi [Admin],

Quick request: I need admin consent for a Microsoft Graph API app registration 
to integrate my AI coding assistant with Outlook/Calendar/OneDrive.

App: microsoft-mcp
App ID: [your-app-id]
Permissions: Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite, 
             Contacts.Read, People.Read, User.Read

These are delegated (user-only) permissions - no tenant-wide access.

Azure Portal: Microsoft Entra ID → App registrations → microsoft-mcp → 
              API permissions → Grant admin consent

Let me know if you have any questions!

Thanks!
```

---

## What to Include When Sending

1. ✅ Your actual Application (client) ID from Azure Portal
2. ✅ Link to your specific app registration in Azure Portal
3. ✅ Your contact info for follow-up questions
4. ✅ (Optional) Screenshot of the permissions page showing what you're requesting

---

## Expected Timeline

- **Typical approval time:** 1-3 business days
- **If urgent:** Mention your use case and timeline
- **If no response:** Follow up after 2-3 days

---

## After Approval

You'll know it's approved when:
1. You receive a notification (if admin sends one)
2. In Azure Portal, permissions show **"Granted for [Organization]"** in green
3. You can successfully authenticate without the "needs admin approval" error

Then proceed to Step 2 in `TODO_MICROSOFT_MCP.md`.

---

**Created:** 2026-01-28
**Status:** Ready to send (fill in your App ID first)
