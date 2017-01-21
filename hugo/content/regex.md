+++
date = "2016-12-09T16:11:43-05:00"
title = "Regex Reference"
+++

### Everything before last forward or backward slash
```regex
^(.*[\\\/])
```
### Breakdown Header Tags
```regex
<h([\d])(.*)>([^<]+)<\/h([\d])>
```