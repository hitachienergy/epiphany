# Release policy

Epiphany Platform uses [semantic versioning](https://semver.org/).  
Example:  
Major release - 0.x.x  
Minor release - 0.2.x  
Patch release - 0.2.1  
Pre-release - 0.3.0rc1

Currently, we supporting quarterly minor releases. These minor releases also include patch releases.

# Epiphany Platform lifecycle

## Short-term Support (STS)

Versions will be released every quarter (except the quarter when the LTS version is published), and each STS version will be supported for up to 6 months.

## Long-term Support (LTS)

The LTS version will be released once a year and will be supported for up to 3 years. During support time, patch releases will be made to the LTS version. The patch version will be released immediately after critical bug fix, in case of minor issues the patch version will be released along with other releases (quarterly).

| Epiphany version | Release date | Latest version | Release date | End of support |
| ----------------------| --------------- | -------------|--------------------|--------------- |
| [0.2.x](../changelogs/CHANGELOG-0.2.md) | 19 Feb 2019 | 0.2.3 | 11 May 2019 | 06 Apr 2020 |
| [0.3.x](../changelogs/CHANGELOG-0.3.md) | 02 Aug 2019 | 0.3.2 | 21 May 2019 | 01 Jul 2020 |
| [0.4.x](../changelogs/CHANGELOG-0.4.md) | 11 Oct 2019 | 0.4.5 | 02 Oct 2020 | 22 Oct 2020 |
| [0.5.x](../changelogs/CHANGELOG-0.5.md) | 17 Jan 2020 | 0.5.6 | 04 Nov 2020 | 19 Jan 2021 |
| [0.6.x](../changelogs/CHANGELOG-0.6.md) | 06 Apr 2020 | 0.6.2 | 09 Apr 2021 | 01 Apr 2021 |
| [0.7.x](../changelogs/CHANGELOG-0.7.md) | 01 Jul 2020 | 0.7.4 | 17 May 2021 | 30 Jun 2021 |
| [0.8.x](../changelogs/CHANGELOG-0.8.md) | 22 Oct 2020 | 0.8.3 | 17 Apr 2021 | 30 Sep 2021 |
| [0.9.x](../changelogs/CHANGELOG-0.9.md) | 19 Jan 2021 | 0.9.2 | 14 May 2021 | 30 Dec 2021 |
| [1.0.x LTS](../changelogs/CHANGELOG-1.0.md) | 01 Apr 2021 | 1.0.1 | 16 Jul 2021 | 01 Apr 2024 |
| [1.1.x STS](../changelogs/CHANGELOG-1.1.md) | 30 Jun 2021 | 1.1.0 | 30 Jun 2021 | 30 Dec 2021 |
| [1.2.x STS](../changelogs/CHANGELOG-1.2.md) | 30 Sep 2021 | 1.2.0 | 30 Sep 2021 | 30 Mar 2022 |
| [1.3.x STS](../changelogs/CHANGELOG-1.3.md) | 19 Jan 2022 | 1.3.0 | 19 Jan 2022 | 30 Jun 2022 |
| [2.0.x LTS](../changelogs/CHANGELOG-2.0.md) | 09 May 2022 | 2.0.0 | 09 May 2022 | 09 May 2025 |
| :arrow_right: 2.0.1 LTS | est. 31 Aug 2022 | --- | --- | 09 May 2025 |
| :arrow_right: 2.0.2 LTS | est. 31 Oct 2022 | --- | --- | 09 May 2025 |

```mermaid
gantt
title Epiphany Platform lifecycle
dateFormat  YYYY-MM-DD
section 0.2.x
0.2.x support cycle     :a, 2019-02-19, 2020-04-06
section 0.3.x
0.3.x support cycle     :a, 2019-08-02, 2020-07-01
section 0.4.x
0.4.x support cycle     :a, 2019-10-11, 2020-10-22
section 0.5.x
0.5.x support cycle     :a, 2020-01-17, 2021-01-02
section 0.6.x
0.6.x support cycle     :a, 2020-04-06, 2021-04-01
section 0.7.x
0.7.x support cycle     :a, 2020-07-01, 2021-06-30
section 0.8.x
0.8.x support cycle     :a, 2020-10-22, 2021-09-30
section 0.9.x
0.9.x support cycle      :a, 2021-01-19, 2021-12-30
section 1.0.x
1.0.x support cycle (LTS - 3 years)    :crit, 2021-04-01, 2024-04-01
section 1.1.x
1.1.x - 6 months     :a, 2021-06-30, 2021-12-30
section 1.2.x
1.2.x - 6 months     :a, 2021-09-30, 2022-03-30
section 1.3.x
1.3.x - 6 months     :active, 2022-01-19, 2022-06-30
section 2.0.x
2.0.x support cycle (LTS - 3 years)     :crit, 2022-05-09, 2025-05-09
2.0.1 patch for LTS     :crit, 2022-08-31, 2025-05-09
2.0.2 patch for LTS     :crit, 2022-10-31, 2025-05-09
```
