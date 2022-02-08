---
name: Bug report
about: Create a report to help us improve
title: "[BUG] Short description of the bug"
labels: status/grooming-needed, type/bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**How to reproduce**
Steps to reproduce the behavior:
1. execute `epicli init ... (with params)`
2. edit config file
3. execute `epicli apply ...`

**Expected behavior**
A clear and concise description of what you expected to happen.

**Config files**
If applicable, add config files to help explain your problem.

**Environment**
- Cloud provider: [AWS | Azure | All | None]
- OS: [e.g. Ubuntu 20.04.3 LTS, you can use `cat /etc/os-release`]

**epicli version**: [`epicli --version`]

**Additional context**
Add any other context about the problem here.

---

**DoD checklist**

- Changelog
  - [ ] updated
  - [ ] not needed
- COMPONENTS.md
  - [ ] updated
  - [ ] not needed
- Schema
  - [ ] updated
  - [ ] not needed
- Backport tasks
  - [ ] created
  - [ ] not needed
- Documentation
  - [ ] added
  - [ ] updated
  - [ ] not needed
- [ ] Feature has automated tests
- [ ] Automated tests passed (QA pipelines)
  - [ ] apply
  - [ ] upgrade
  - [ ] backup/restore
- [ ] Idempotency tested
- [ ] All conversations in PR resolved
