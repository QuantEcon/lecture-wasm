# TODO

## High Priority

### Automate Content Synchronization

**Issue:** Content sync from `lecture-python-intro/wasm` is currently manual via `update_lectures.py`

# TODO

## High Priority

### Automate Content Synchronization

**Current:** Manual sync via `python update_lectures.py`

**Goal:** Automatic sync when source repository updates

**Simple Implementation:**
- Add scheduled workflow (runs daily or weekly)
- Check for changes in `lecture-python-intro/wasm` branch
- Run `update_lectures.py` if changes detected
- Create PR with synced content for review

**Why:** Reduces manual maintenance, keeps content current

---

## Medium Priority

- Add issue templates (bug report, feature request)
- Create pull request template with checklist
- Test update_lectures.py with error handling improvements

---

## Low Priority

- Add FAQ section to docs
- Improve browser compatibility testing
- Document common WASM compatibility issues

---

*Last Updated: November 1, 2025*

**Implementation Options:**

1. **Repository Dispatch** (Recommended)
   - Add workflow trigger in `lecture-python-intro` that sends dispatch event
   - Workflow in this repo listens for dispatch and runs sync
   - Most reliable, requires coordination between repos

2. **Scheduled Sync**
   - Run sync check daily/weekly via cron schedule
   - Compare commit SHAs to detect changes
   - Simpler but less immediate

3. **Webhook**
   - Use GitHub webhook to detect pushes to wasm branch
   - More complex setup but real-time

**Files to Create:**
- `.github/workflows/sync-content.yml` - Sync automation workflow
- Document process in `docs/ARCHITECTURE.md`

**Benefits:**
- Eliminates manual sync step
- Ensures content stays current
- Reduces maintenance burden
- Prevents sync delays

**Risks to Mitigate:**
- Ensure WASM compatibility checks run before merge
- Test sync in PR preview environment
- Add manual approval step for safety

---

## Medium Priority

### Improve Build Performance
- Investigate incremental builds with mystmd
- Cache dependencies in CI/CD
- Optimize Pyodide loading in browser

### Enhanced Testing
- Add automated WASM compatibility tests
- Test code cell execution in headless browser
- Validate all external package imports

### Documentation Improvements
- Add video tutorial for local setup
- Create FAQ document
- Add troubleshooting decision tree

---

## Low Priority

### Developer Experience
- Create setup script for one-command installation
- Add pre-commit hooks for validation
- Improve error messages in update_lectures.py

### Community
- Add issue templates
- Create pull request template
- Set up GitHub Discussions

---

## Future Enhancements

### Progressive Web App
- Service worker for offline support
- Install to desktop capability
- Background computation via WebWorkers

### Performance Optimization
- Custom CDN for Pyodide packages
- Lazy loading of lecture content
- IndexedDB for persistent storage

### Analytics
- Track build times
- Monitor page load performance
- Error rate monitoring

---

*Last Updated: November 1, 2025*
