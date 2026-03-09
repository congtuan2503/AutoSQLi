═══════════════════════════════════════════════════════════════════════════
🤖 GITHUB ACTIONS BOT - AUTOMATIC PAYLOAD UPDATES
═══════════════════════════════════════════════════════════════════════════

Hệ thống tự động cập nhật SQL injection payloads trên GitHub mà không cần
thủ công. Bot sẽ chạy hàng ngày để cào dữ liệu mới, commit lên repository,
và push tự động.

═══════════════════════════════════════════════════════════════════════════

📋 CÓ GÌ ĐƯỢC SETUP:

1. **Daily Auto-Update Workflow** (.github/workflows/intelligence-update.yml)
   - Chạy hàng ngày lúc 2:00 AM UTC (9:00 AM Vietnam time)
   - Tự động scrape từ 4 sources
   - Commit & push nếu có dữ liệu mới
   - Auto-generate summary report

2. **Manual Test Workflow** (.github/workflows/manual-test-update.yml)
   - Trigger thủ công từ GitHub Actions tab
   - Dry-run option (test mà không commit)
   - Useful cho testing & debugging

═══════════════════════════════════════════════════════════════════════════

🚀 CÁC BƯỚC SETUP:

**STEP 1: Confirm GitHub Actions Enabled**
✓ Đã có sẵn - GitHub Actions enabled by default trên public repos

**STEP 2: Verify Workflow Files**
✓ Files đã được tạo:
  - .github/workflows/intelligence-update.yml
  - .github/workflows/manual-test-update.yml

**STEP 3: Commit & Push**
Chạy các commands sau:

  cd 'c:\Users\luaho\OneDrive - Home\Code\AutoSQLi'
  git add .github/
  git commit -m "Add GitHub Actions Bot for automatic intelligence updates"
  git push origin main

**STEP 4: Test Workflow**
- Vào GitHub: https://github.com/congtuan2503/AutoSQLi
- Click "Actions" tab
- Chọn "🤖 AutoSQLi Intelligence Auto-Update"
- Click "Run workflow" (nếu có nút)
- Hoặc click "🧪 Manual Intelligence Test Update" để test

═══════════════════════════════════════════════════════════════════════════

⏰ SCHEDULE INFORMATION:

Current Schedule: 0 2 * * * UTC
- Giờ: 2:00 AM UTC
- Vietnam time: 9:00 AM (UTC+7)
- Tần suất: Hàng ngày

Muốn thay đổi giờ?
Edit file: .github/workflows/intelligence-update.yml
  schedule:
    - cron: '0 2 * * *'  ← Thay đổi con số này
    
Cron format:
  ┌─────── minute (0 - 59)
  │ ┌───── hour (0 - 23)
  │ │ ┌─── day of month (1 - 31)
  │ │ │ ┌─ month (1 - 12)
  │ │ │ │ ┌ day of week (0 - 6) (Sunday to Saturday)
  │ │ │ │ │
  │ │ │ │ │
  * * * * *

Ví dụ:
  '0 9 * * *'   → 9:00 AM mỗi ngày
  '0 */6 * * *' → Mỗi 6 giờ
  '0 0 * * 1'   → Monday 0:00 AM

═══════════════════════════════════════════════════════════════════════════

📖 HOW IT WORKS:

1. **TRIGGER** (Daily or Manual)
   ↓
   GitHub Actions starts workflow

2. **SETUP** (Automated)
   ↓
   - Clone repository
   - Setup Python 3.10
   - Install requirements (requests, schedule, etc.)

3. **INTELLIGENCE UPDATE**
   ↓
   python main.py --update-database
   ↓
   Scrapes from:
   • OWASP PayloadsAllTheThings
   • GitHub security tools
   • PortSwigger Academy
   • CVE Databases

4. **DETECT CHANGES**
   ↓
   Check if data/payloads.json was updated

5. **COMMIT & PUSH** (If changes detected)
   ↓
   - git config user (AutoSQLi-Bot)
   - git add data/payloads*.json
   - git commit with message
   - git push origin main

6. **REPORT**
   ↓
   Generate summary:
   • Total payloads
   • Breakdown by source
   • Status (updated or no changes)

═══════════════════════════════════════════════════════════════════════════

🎮 HOW TO USE:

**Automatic Daily Updates:**
✓ Just wait! Bot runs everyday at 9:00 AM Vietnam time
✓ Check GitHub Actions tab to see logs
✓ Payloads auto-commit when new data found

**Manual Trigger:**
1. Go to: https://github.com/congtuan2503/AutoSQLi
2. Click "Actions" tab
3. Click "🤖 AutoSQLi Intelligence Auto-Update"
4. Click "Run workflow" button
5. Select branch (main)
6. Click "Run workflow"

**Manual Test (Dry Run):**
1. Click "🧪 Manual Intelligence Test Update"
2. Select "dry_run: true"
3. Click "Run workflow"
4. Test without committing changes

═══════════════════════════════════════════════════════════════════════════

📊 MONITORING:

**View Workflow Status:**
https://github.com/congtuan2503/AutoSQLi/actions

**Check Logs:**
1. Click workflow run
2. Click "update-payloads" job
3. Expand each step to see details

**View Database Changes:**
1. Click "Commits"
2. Look for commits by "AutoSQLi-Bot"
3. Check what changed in data/payloads.json

**View Summary Report:**
1. Click workflow run
2. Scroll down to "Summary" section
3. Shows total payloads & breakdown

═══════════════════════════════════════════════════════════════════════════

🔧 CONFIGURATION:

**Change Update Hour:**

File: .github/workflows/intelligence-update.yml
  schedule:
    - cron: '0 2 * * *'  ← Change '2' to desired hour (0-23)

Examples:
  '0 0 * * *'  → Midnight UTC (7:00 AM VN)
  '0 9 * * *'  → 9:00 AM UTC (4:00 PM VN)
  '0 12 * * *' → Noon UTC (7:00 PM VN)

**Change Frequency:**

Daily:
  - cron: '0 2 * * *'

Twice daily:
  - cron: '0 2 * * *'
  - cron: '0 14 * * *'

Every 6 hours:
  - cron: '0 */6 * * *'

Weekly (Monday):
  - cron: '0 2 * * 1'

**Disable Workflow:**
1. Go to Actions tab
2. Click workflow
3. Click "..." menu
4. Click "Disable workflow"

═══════════════════════════════════════════════════════════════════════════

⚠️ IMPORTANT NOTES:

✓ **GitHub Token**: Uses default GITHUB_TOKEN (auto-provided by GitHub)
  - No need to manually create tokens
  - Auto-revoked after workflow completes
  - Secure & safe

✓ **Commit Name**: "AutoSQLi-Bot"
  - Commits marked as from bot
  - Easy to distinguish from manual commits

✓ **Skip CI**: Commits have [skip ci] tag
  - Prevents infinite loops
  - Avoids triggering other workflows

✓ **Rate Limiting**: 
  - GitHub API has rate limits
  - Workflow continues even if APIs are slow
  - Uses "continue-on-error: true"

✓ **Permissions**:
  - Workflow has "write" permission for contents
  - Can only modify its repo
  - Safe & isolated

═══════════════════════════════════════════════════════════════════════════

🔍 TROUBLESHOOTING:

**Workflow doesn't run:**
→ Check Actions tab for errors
→ Verify branch is 'main'
→ Check cron syntax (https://crontab.guru)

**No commits created:**
→ Maybe no new data found (normal)
→ Check logs to see if scraper ran successfully
→ Try manual trigger with dry_run=false

**Permissions denied:**
→ Verify workflow has 'contents: write' permission
→ Check repository settings allow Actions

**API errors:**
→ Check scraper logs (GitHub Actions output)
→ APIs might be rate-limited
→ Workflow continues anyway (non-blocking)

═══════════════════════════════════════════════════════════════════════════

💡 ADVANCED CUSTOMIZATION:

**Send Notifications on Updates**

Add this step to intelligence-update.yml:

  - name: 📧 Send notification
    if: steps.check_changes.outputs.has_changes == 'true'
    uses: actions/github-script@v6
    with:
      script: |
        console.log('New payloads found!')
        // Could send email, webhook, etc.

**Update Other Sources**

Extend scrapers by:
1. Create new scraper in scrapers/
2. Add to core/updater.py
3. Commit to repo
4. Bot automatically uses new scraper next run

**Parallel Scraping**

Modify core/updater.py to use:
  - Concurrent.futures
  - asyncio
  - Threading
For faster updates

═══════════════════════════════════════════════════════════════════════════

🎯 WORKFLOW DIAGRAM:

GitHub Actions (Timer)
        ↓
    (2:00 AM UTC)
        ↓
    Checkout code
        ↓
    Setup Python
        ↓
    Install deps
        ↓
    Run Scraper
    ├─ OWASP
    ├─ GitHub
    ├─ PortSwigger
    └─ CVE
        ↓
    Update payloads.json
        ↓
    Detect changes?
    ├─ Yes → Commit & Push
    └─ No → Skip commit
        ↓
    Generate Report
        ↓
    Done! ✅

═══════════════════════════════════════════════════════════════════════════

📌 SUMMARY:

✅ Automatic daily intelligence gathering
✅ No manual intervention needed
✅ GitHub handles all execution
✅ Auto-commit & push new payloads
✅ Manual trigger available
✅ Dry-run testing option
✅ Detailed logs & reports
✅ Secure & safe (no exposed credentials)

Result: Tool gets smarter every day automatically! 🚀

═══════════════════════════════════════════════════════════════════════════
