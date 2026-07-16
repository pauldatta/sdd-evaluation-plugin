# Google Docs Integration Reference

How to acquire an SDD from Google Docs using the Google Workspace MCP tools.

## Prerequisites

The Google Workspace extension must be installed. See the plugin README for per-platform setup instructions.

## Reading a Google Doc

### From a URL

The user provides a URL like `https://docs.google.com/document/d/1a2b3c4d/edit`.

**All workspace tools accept URLs directly** — do not manually extract the document ID.

```
docs.getText({ documentId: "https://docs.google.com/document/d/1a2b3c4d/edit" })
```

### From a Document Name

The user says "evaluate the SDD called Project Alpha Design Doc."

1. Search for it:
```
drive.search({
  query: "mimeType='application/vnd.google-apps.document' and name contains 'Project Alpha Design Doc'"
})
```

2. Read the matching document:
```
docs.getText({ documentId: "<id-or-url-from-search-result>" })
```

### Multi-Tab Documents

- `docs.getText` with no `tabId` returns all tabs as a JSON array with `tabId`, `title`, `content`, and `index`
- If the SDD spans multiple tabs, read all tabs and concatenate for evaluation
- If only one tab exists, you get plain text directly

## Handling Images in Google Docs

Google Docs may contain embedded images (architecture diagrams, flowcharts, screenshots). The `docs.getText` tool returns text content only — it does not extract embedded images as binary data.

**What to do:**

1. **Note the presence of images.** The text content will include inline object markers or surrounding context that references diagrams. Acknowledge these in your evaluation.
2. **Describe from context.** Use the surrounding text, captions, and section headings to infer what the diagrams depict.
3. **Credit the author.** If the document references diagrams, score Dimension 2 (Architecture) and Dimension 6 (Clarity) accounting for the fact that visual aids exist — even if you can't see the image content directly.
4. **Ask if ambiguous.** If the presence or content of a diagram is critical to scoring and you can't determine it from context, ask the user: "Your doc references an architecture diagram in Section X — can you describe what it shows?"

## Handling Comments and Suggestions

If the SDD is under review and has comments or suggested edits:

- Use `drive.getComments({ fileId: "<doc-id>" })` to read reviewer comments — these provide additional context about known gaps
- Use `docs.getSuggestions({ documentId: "<doc-id>" })` to see pending edits
- Do **not** evaluate suggested edits as if they are accepted content — evaluate the current document state

## Fallback: No Workspace MCP Available

If the Google Workspace MCP is not configured:

1. Ask the user to export the Google Doc as Markdown: **File → Download → Markdown (.md)**
2. Have the user place the exported file in their workspace
3. Read the local Markdown file instead

This fallback works on all platforms (Antigravity, Gemini CLI, Claude Code) without any MCP dependency.
