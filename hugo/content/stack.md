+++
title = "This site's Stack"
date = "2016-12-09T16:11:43-05:00"
+++

*Source avaialable on Github: [MrMatt57/MrMatt.io](https://github.com/MrMatt57/MrMatt.io)*

### Website Optimization Guidelines
- Make it fast!
- Fewest number of resource files
- One network route to all resource files

### Development Build Toolchain
- Gulp Task Runner
- SASS compiler
- CSS vender autoprefix, cleaned and concat
- Asset Fingerprinting 
- Hugo Build
- ImagMagick thumbnail creation
- BrowserSync

### Continuous Integration and Deployment
- Travis CI
- Gulp Tasks
- Pa11y WCAG 2.0 AA accessibility testing
- S3Cmd Sync
- KeyCDN Cache Expiration

### Hosting
- Google Domains - Registrar 
- DNS Made Easy - DNS
- Amazon S3 - Orgin 
- KeyCDN - Edge Servers
- Let's Encrypt TLS

### Operations
- Staticman - Comment Processing
- StatusCake Monitoring - [Site Status](http://status.mrmatt57.org/)
- Pushbullet Notifications
- GSuite - Email/Calendar/Docs/Drive
- CrashPlan Workstation Backups

Have suggestions on how I can make the site/stack better? [Let me know](https://github.com/MrMatt57/MrMatt.io/issues/new).

Special thanks to:

- [hugulp](https://github.com/jbrodriguez/hugulp) project for much of gulp workflow I am using.
- [Michael Rose](https://mademistakes.com/) for creative inspiration and much of my Staticman implemenation.