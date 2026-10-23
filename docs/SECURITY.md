# Security & privacy checklist (Day 21)

- [ ] API keys only server-side (`.env`, never in the frontend or repo)
- [ ] Upload file type + size validated (`MAX_UPLOAD_MB`)
- [ ] Suspicious URLs never auto-opened
- [ ] No call/message monitoring without explicit user permission
- [ ] Uploads not persisted by default (temp file, deleted after check)
- [ ] Clear retention / deletion policy documented
- [ ] CORS restricted to known origins
