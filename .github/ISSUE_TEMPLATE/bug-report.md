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
- OS: [e.g. Ubuntu 18.04.4 LTS, you can use `cat /etc/os-release`]

**epicli version**: [`epicli --version`]

**Additional context**
Add any other context about the problem here.

---

**DoD checklist**

* [ ] Changelog updated (if affected version was released)
* [ ] COMPONENTS.md updated / doesn't need to be updated
* [ ] Automated tests passed (QA pipelines)
  * [ ] apply
  * [ ] upgrade
* [ ] Case covered by automated test (if possible)
* [ ] Idempotency tested
* [ ] Documentation updated / doesn't need to be updated
* [ ] All conversations in PR resolved
