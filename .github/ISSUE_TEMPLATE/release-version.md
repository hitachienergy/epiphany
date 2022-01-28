---
name: Release version
about: Prepare and publish a release
title: "[RELEASE] vX.Y.Z"
labels: type/release
assignees: ''

---

#### Release checklist

* [ ] Default OS cloud images updated
* [ ] Support branch created
* [ ] CI pipelines for support branch created
* All automated tests passed (QA pipelines):
  * [ ] Standard apply (new cluster)
  * [ ] Standard apply (existing cluster)
  * [ ] Upgrade for V-1
  * [ ] Upgrade for V-2
  * [ ] Upgrade for V-3
  * [ ] Upgrade for V-4
  * [ ] k8s HA apply
  * [ ] Promote k8s to HA apply
  * [ ] Single machine apply
  * [ ] Offline mode apply
* Changelog:
  * [ ] Changelog updated (release date, known issues, breaking changes, deprecations)
  * [ ] Changelog for the next version created in develop branch
* Documentation:
  * [ ] Updated LIFECYCLE.md & LIFECYCLE_GANTT.md
  * [ ] Updated Testing Scenarios list
* [ ] Release pipeline performed
* [ ] GitHub release exists with correct content (links)
* [ ] `docker pull` command from the release description tested
* [ ] Version bumped to the next in develop branch (in VERSION file)
* [ ] Releases updated in ZenHub
