(function() {
    'use strict';

    var REPO_OWNER = 'MrMatt57';
    var REPO_NAME = 'MrMatt.io';
    var BRANCH = 'main';
    var ALLOWED_USER = 'MrMatt57';
    var SITE_TIME_ZONE = 'America/New_York';
    var SITE_DATE_FORMATTER = new Intl.DateTimeFormat('en-US', {
        timeZone: SITE_TIME_ZONE,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });

    var statusEl = document.getElementById('status');
    var authSection = document.getElementById('auth-section');
    var loginBtn = document.getElementById('login-btn');
    var uploadForm = document.getElementById('upload-form');
    var photoInput = document.getElementById('photo-input');
    var previewEl = document.getElementById('preview');
    var previewImg = document.getElementById('preview-img');
    var submitBtn = document.getElementById('submit-btn');
    var logoutBtn = document.getElementById('logout-btn');
    var userInfo = document.getElementById('user-info');
    var aiStatus = document.getElementById('ai-status');
    var aiTitle = document.getElementById('ai-title');
    var publishDateInput = document.getElementById('publish-date');
    var publishDateStatus = document.getElementById('publish-date-status');
    var aiAlt = document.getElementById('ai-alt');
    var aiDesc = document.getElementById('ai-description');
    var aiSection = document.getElementById('ai-section');
    var aiFeedback = document.getElementById('ai-feedback');
    var regenerateBtn = document.getElementById('regenerate-btn');

    var currentPhotoFile = null;
    var publishDateRequestId = 0;

    // --- Escape a string for use inside YAML double-quoted values ---
    function escapeYamlString(str) {
        return str.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
    }

    function slugify(str) {
        return (str || '')
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '')
            .slice(0, 40);
    }

    function getFileStem(name) {
        return (name || '').replace(/\.[^.]+$/, '');
    }

    function getSiteLocalDateString(date) {
        var parts = SITE_DATE_FORMATTER.formatToParts(date);
        var year = '';
        var month = '';
        var day = '';

        parts.forEach(function(part) {
            if (part.type === 'year') {
                year = part.value;
            } else if (part.type === 'month') {
                month = part.value;
            } else if (part.type === 'day') {
                day = part.value;
            }
        });

        return year + '-' + month + '-' + day;
    }

    function setPublishDateStatus(message, type) {
        publishDateStatus.textContent = message;
        publishDateStatus.className = 'field-help' + (type ? ' ' + type : '');
    }

    function setPublishDateValue(dateStr, source) {
        publishDateInput.value = dateStr;
        publishDateInput.dataset.source = source || 'manual';
        validatePublishDate();
    }

    function validatePublishDate() {
        var siteToday = getSiteLocalDateString(new Date());
        var dateStr = publishDateInput.value;
        var source = publishDateInput.dataset.source || 'manual';
        var message = '';

        publishDateInput.max = siteToday;

        if (!dateStr) {
            publishDateInput.classList.add('invalid');
            setPublishDateStatus('Choose a publish date in ' + SITE_TIME_ZONE + ' before uploading.', 'error');
            return { valid: false, dateStr: '' };
        }

        if (dateStr > siteToday) {
            publishDateInput.classList.add('invalid');
            setPublishDateStatus('This date is in the future for ' + SITE_TIME_ZONE + ' and Hugo would skip it during deploy. Pick today or earlier.', 'error');
            return { valid: false, dateStr: dateStr };
        }

        publishDateInput.classList.remove('invalid');
        if (source === 'exif') {
            message = 'Using EXIF date ' + dateStr + ' in ' + SITE_TIME_ZONE + '.';
        } else if (source === 'site-local') {
            message = 'Using the site-local date ' + dateStr + ' in ' + SITE_TIME_ZONE + '.';
        } else {
            message = 'Publish date will be saved as ' + dateStr + ' in ' + SITE_TIME_ZONE + '.';
        }
        setPublishDateStatus(message + ' Future dates are rejected because Cloudflare Pages does not auto-publish at midnight.', 'info');

        return { valid: true, dateStr: dateStr };
    }

    function prefillPublishDate(fileOrBlob) {
        var requestId = ++publishDateRequestId;
        publishDateInput.max = getSiteLocalDateString(new Date());
        return extractExifDate(fileOrBlob).then(function(exifDate) {
            if (requestId !== publishDateRequestId) {
                return;
            }
            setPublishDateValue(exifDate || getSiteLocalDateString(new Date()), exifDate ? 'exif' : 'site-local');
        });
    }

    function clearUploadForm() {
        publishDateRequestId += 1;
        photoInput.value = '';
        previewEl.classList.remove('visible');
        aiSection.style.display = 'none';
        window._sharedPhoto = null;
        currentPhotoFile = null;
        aiFeedback.value = '';
        aiTitle.value = '';
        publishDateInput.value = '';
        publishDateInput.dataset.source = 'manual';
        publishDateInput.classList.remove('invalid');
        setPublishDateStatus('Publish date uses ' + SITE_TIME_ZONE + '. Future dates are rejected because Cloudflare Pages does not auto-publish at midnight.', 'info');
        aiAlt.value = '';
        aiDesc.value = '';
    }

    // --- Extract EXIF date from JPEG ---
    function extractExifDate(file) {
        return new Promise(function(resolve) {
            if (file.type !== 'image/jpeg' && file.type !== 'image/jpg') {
                return resolve(null);
            }
            var reader = new FileReader();
            reader.onload = function() {
                try {
                    var buf = new DataView(reader.result);
                    // Check JPEG SOI marker
                    if (buf.getUint16(0) !== 0xFFD8) return resolve(null);

                    var offset = 2;
                    while (offset < buf.byteLength - 1) {
                        var marker = buf.getUint16(offset);
                        if (marker === 0xFFE1) { // APP1 (EXIF)
                            var date = parseExifSegment(buf, offset + 4);
                            return resolve(date);
                        }
                        // Skip non-APP1 markers
                        if ((marker & 0xFF00) !== 0xFF00) return resolve(null);
                        var segLen = buf.getUint16(offset + 2);
                        offset += 2 + segLen;
                    }
                    resolve(null);
                } catch (e) {
                    resolve(null);
                }
            };
            reader.onerror = function() { resolve(null); };
            // Read first 128KB — enough for EXIF
            reader.readAsArrayBuffer(file.slice(0, 131072));
        });
    }

    function parseExifSegment(buf, tiffStart) {
        // Verify "Exif\0\0" header
        if (buf.getUint32(tiffStart) !== 0x45786966 || buf.getUint16(tiffStart + 4) !== 0x0000) {
            return null;
        }
        var base = tiffStart + 6; // Start of TIFF header
        var endian = buf.getUint16(base);
        var le = (endian === 0x4949); // II = little-endian, MM = big-endian
        if (!le && endian !== 0x4D4D) return null;

        var ifdOffset = buf.getUint32(base + 4, le);
        var dateTime = null;
        var dateTimeOriginal = readIfdDate(buf, base, base + ifdOffset, le, 0x0132); // DateTime from IFD0

        // Find ExifIFD pointer (tag 0x8769)
        var exifIfdOffset = readIfdPointer(buf, base, base + ifdOffset, le, 0x8769);
        if (exifIfdOffset !== null) {
            var dto = readIfdDate(buf, base, base + exifIfdOffset, le, 0x9003); // DateTimeOriginal
            if (dto) return dto;
        }

        return dateTimeOriginal; // Fallback to DateTime
    }

    function readIfdPointer(buf, base, ifdStart, le, targetTag) {
        try {
            var count = buf.getUint16(ifdStart, le);
            for (var i = 0; i < count; i++) {
                var entryStart = ifdStart + 2 + (i * 12);
                var tag = buf.getUint16(entryStart, le);
                if (tag === targetTag) {
                    return buf.getUint32(entryStart + 8, le);
                }
            }
        } catch (e) {}
        return null;
    }

    function readIfdDate(buf, base, ifdStart, le, targetTag) {
        try {
            var count = buf.getUint16(ifdStart, le);
            for (var i = 0; i < count; i++) {
                var entryStart = ifdStart + 2 + (i * 12);
                var tag = buf.getUint16(entryStart, le);
                if (tag === targetTag) {
                    var type = buf.getUint16(entryStart + 2, le);
                    var numValues = buf.getUint32(entryStart + 4, le);
                    if (type !== 2) continue; // ASCII type
                    var valOffset = buf.getUint32(entryStart + 8, le);
                    var str = '';
                    for (var j = 0; j < numValues - 1; j++) {
                        str += String.fromCharCode(buf.getUint8(base + valOffset + j));
                    }
                    // EXIF date format: "YYYY:MM:DD HH:MM:SS"
                    var match = str.match(/^(\d{4}):(\d{2}):(\d{2})/);
                    if (match) {
                        return match[1] + '-' + match[2] + '-' + match[3];
                    }
                }
            }
        } catch (e) {}
        return null;
    }

    function getToken() {
        return localStorage.getItem('gh_token');
    }

    function setToken(token) {
        localStorage.setItem('gh_token', token);
    }

    function clearToken() {
        localStorage.removeItem('gh_token');
    }

    function showStatus(msg, type) {
        statusEl.textContent = msg;
        statusEl.className = 'status ' + (type || 'info');
        statusEl.style.display = 'block';
    }

    function hideStatus() {
        statusEl.style.display = 'none';
    }

    function showUploadForm() {
        authSection.style.display = 'none';
        uploadForm.classList.add('visible');
    }

    function showLoginForm() {
        authSection.style.display = 'block';
        uploadForm.classList.remove('visible');
        userInfo.style.display = 'none';
        logoutBtn.style.display = 'none';
    }

    // --- OAuth state parameter for CSRF protection ---
    function generateState() {
        var array = new Uint8Array(16);
        crypto.getRandomValues(array);
        return Array.from(array, function(b) { return b.toString(16).padStart(2, '0'); }).join('');
    }

    // --- OAuth callback ---
    function handleOAuthCallback() {
        var params = new URLSearchParams(window.location.search);
        var code = params.get('code');
        var returnedState = params.get('state');
        if (!code) return Promise.resolve(false);

        // Verify state parameter
        var savedState = localStorage.getItem('oauth_state');
        localStorage.removeItem('oauth_state');
        if (!savedState || savedState !== returnedState) {
            showStatus('Login failed: invalid state parameter (possible CSRF).', 'error');
            window.history.replaceState({}, '', '/upload/');
            return Promise.resolve(false);
        }

        showStatus('Completing authentication...', 'info');

        return fetch('/api/oauth-exchange', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, state: returnedState })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.token) {
                setToken(data.token);
                window.history.replaceState({}, '', '/upload/');
                return true;
            }
            throw new Error(data.error || 'OAuth exchange failed');
        })
        .catch(function(err) {
            showStatus('Login failed: ' + err.message, 'error');
            return false;
        });
    }

    // --- Fetch GitHub user and validate ---
    function fetchUser(token) {
        return fetch('https://api.github.com/user', {
            headers: { 'Authorization': 'token ' + token }
        })
        .then(function(r) {
            if (!r.ok) throw new Error('Invalid token');
            return r.json();
        })
        .then(function(user) {
            if (user.login !== ALLOWED_USER) {
                clearToken();
                throw new Error('Unauthorized: only ' + ALLOWED_USER + ' can upload photos.');
            }
            return user;
        });
    }

    // --- Shared photo from service worker ---
    function checkSharedPhoto() {
        var params = new URLSearchParams(window.location.search);
        if (!params.has('share-target')) return;

        caches.open('shared-photos').then(function(cache) {
            return Promise.all([
                cache.match('shared-photo-meta').then(function(r) { return r ? r.json() : null; }),
                cache.match('shared-photo-file').then(function(r) { return r ? r.blob() : null; })
            ]);
        }).then(function(results) {
            var meta = results[0];
            var blob = results[1];
            if (!blob) return;

            var url = URL.createObjectURL(blob);
            previewImg.src = url;
            previewEl.classList.add('visible');
            window._sharedPhoto = blob;

            caches.delete('shared-photos');
            window.history.replaceState({}, '', '/upload/');

            prefillPublishDate(blob);
            describePhoto(blob);
        });
    }

    // --- Convert any image to JPEG via Canvas ---
    function toJpegBase64(fileOrBlob) {
        return new Promise(function(resolve, reject) {
            var url = URL.createObjectURL(fileOrBlob);
            var img = new Image();
            img.onload = function() {
                var maxDim = 1024;
                var w = img.width;
                var h = img.height;
                if (w > maxDim || h > maxDim) {
                    if (w > h) {
                        h = Math.round(h * maxDim / w);
                        w = maxDim;
                    } else {
                        w = Math.round(w * maxDim / h);
                        h = maxDim;
                    }
                }
                var canvas = document.createElement('canvas');
                canvas.width = w;
                canvas.height = h;
                canvas.getContext('2d').drawImage(img, 0, 0, w, h);
                var dataUrl = canvas.toDataURL('image/jpeg', 0.85);
                URL.revokeObjectURL(url);
                resolve(dataUrl.split(',')[1]);
            };
            img.onerror = function() {
                URL.revokeObjectURL(url);
                reject(new Error('Could not load image'));
            };
            img.src = url;
        });
    }

    // --- AI photo description ---
    function describePhoto(fileOrBlob, feedback) {
        currentPhotoFile = fileOrBlob;
        aiSection.style.display = 'block';
        aiStatus.textContent = feedback ? 'Regenerating with your feedback...' : 'Analyzing photo...';
        aiStatus.style.display = 'block';
        aiTitle.value = '';
        aiAlt.value = '';
        aiDesc.value = '';
        regenerateBtn.disabled = true;

        toJpegBase64(fileOrBlob)
            .then(function(base64) {
                var requestBody = { image: base64, media_type: 'image/jpeg' };
                if (feedback) {
                    requestBody.feedback = feedback;
                }

                return fetch('/api/describe-photo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
            })
            .then(function(r) {
                if (!r.ok) throw new Error('API error: ' + r.status);
                return r.json();
            })
            .then(function(data) {
                if (data.error) throw new Error(data.error);
                aiStatus.style.display = 'none';
                aiTitle.value = data.title || '';
                aiAlt.value = data.alt || '';
                aiDesc.value = data.description || '';
                regenerateBtn.disabled = false;
            })
            .catch(function(err) {
                aiStatus.textContent = 'AI description unavailable: ' + err.message;
                regenerateBtn.disabled = false;
            });
    }

    // --- Login button: fetch client ID from API, then redirect ---
    loginBtn.addEventListener('click', function() {
        loginBtn.disabled = true;
        showStatus('Connecting to GitHub...', 'info');

        fetch('/api/oauth-client-id')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.error || !data.client_id) {
                    throw new Error(data.error || 'OAuth not configured');
                }
                var redirectUri = window.location.origin + '/upload/';
                var state = generateState();
                localStorage.setItem('oauth_state', state);
                var url = 'https://github.com/login/oauth/authorize' +
                    '?client_id=' + encodeURIComponent(data.client_id) +
                    '&redirect_uri=' + encodeURIComponent(redirectUri) +
                    '&scope=public_repo' +
                    '&state=' + encodeURIComponent(state);
                window.location.href = url;
            })
            .catch(function(err) {
                showStatus('Login failed: ' + err.message, 'error');
                loginBtn.disabled = false;
            });
    });

    // --- File input change ---
    photoInput.addEventListener('change', function() {
        var file = this.files[0];
        if (!file) return;
        window._sharedPhoto = null;
        var url = URL.createObjectURL(file);
        if (url.startsWith('blob:')) {
            previewImg.src = url;
        }
        previewEl.classList.add('visible');
        aiFeedback.value = '';
        prefillPublishDate(file);
        describePhoto(file);
    });

    publishDateInput.addEventListener('input', function() {
        publishDateInput.dataset.source = 'manual';
        validatePublishDate();
    });

    // --- Regenerate AI description with feedback ---
    regenerateBtn.addEventListener('click', function() {
        if (!currentPhotoFile) return;
        describePhoto(currentPhotoFile, aiFeedback.value.trim());
    });

    // --- Logout ---
    logoutBtn.addEventListener('click', function() {
        clearToken();
        showLoginForm();
        hideStatus();
        clearUploadForm();
    });

    // --- GitHub API helpers ---
    var API_BASE = 'https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME;

    function getMainSha(token) {
        return fetch(API_BASE + '/git/ref/heads/' + BRANCH, {
            headers: { 'Authorization': 'token ' + token }
        }).then(function(r) {
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return r.json();
        }).then(function(data) {
            return data.object.sha;
        });
    }

    function createBranch(token, branchName, sha) {
        return fetch(API_BASE + '/git/refs', {
            method: 'POST',
            headers: {
                'Authorization': 'token ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ref: 'refs/heads/' + branchName,
                sha: sha
            })
        }).then(function(r) {
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return r.json();
        });
    }

    function resourceExists(token, path) {
        return fetch(API_BASE + '/' + path, {
            headers: { 'Authorization': 'token ' + token }
        }).then(function(r) {
            if (r.status === 404) return false;
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return true;
        });
    }

    function branchExists(token, branchName) {
        return resourceExists(token, 'git/ref/heads/' + branchName);
    }

    function contentPathExists(token, path, branch) {
        return fetch(API_BASE + '/contents/' + path + '?ref=' + encodeURIComponent(branch), {
            headers: { 'Authorization': 'token ' + token }
        }).then(function(r) {
            if (r.status === 404) return false;
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return true;
        });
    }

    function findAvailableUploadTarget(token, dateStr, slugBase) {
        var attempt = 1;

        function candidateForAttempt(n) {
            var suffix = n === 1 ? '' : '-' + n;
            var folderName = dateStr + '-' + slugBase + suffix;
            return {
                folderName: folderName,
                basePath: 'content/photography/' + folderName,
                branchName: 'photo/' + folderName
            };
        }

        function checkNext() {
            var candidate = candidateForAttempt(attempt);
            return Promise.all([
                contentPathExists(token, candidate.basePath + '/index.md', BRANCH),
                branchExists(token, candidate.branchName)
            ]).then(function(results) {
                if (!results[0] && !results[1]) {
                    return candidate;
                }
                attempt += 1;
                return checkNext();
            });
        }

        return checkNext();
    }

    function commitFile(token, path, contentBase64, message, branch) {
        return fetch(API_BASE + '/contents/' + path, {
            method: 'PUT',
            headers: {
                'Authorization': 'token ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                content: contentBase64,
                branch: branch
            })
        }).then(function(r) {
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return r.json();
        });
    }

    function createPR(token, title, head, base) {
        return fetch(API_BASE + '/pulls', {
            method: 'POST',
            headers: {
                'Authorization': 'token ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                head: head,
                base: base
            })
        }).then(function(r) {
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return r.json();
        });
    }

    function enableAutoMerge(token, prNodeId) {
        return fetch('https://api.github.com/graphql', {
            method: 'POST',
            headers: {
                'Authorization': 'bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: 'mutation($id: ID!) { enablePullRequestAutoMerge(input: { pullRequestId: $id, mergeMethod: SQUASH }) { pullRequest { number } } }',
                variables: { id: prNodeId }
            })
        }).then(function(r) { return r.json(); });
    }

    // --- Submit upload ---
    submitBtn.addEventListener('click', function() {
        var file = window._sharedPhoto || (photoInput.files && photoInput.files[0]);
        if (!file) {
            showStatus('Please select a photo.', 'error');
            return;
        }

        var publishDate = validatePublishDate();
        if (!publishDate.valid) {
            showStatus('Pick a publish date that is today or earlier in ' + SITE_TIME_ZONE + '.', 'error');
            return;
        }

        var token = getToken();
        if (!token) {
            showStatus('Please log in first.', 'error');
            return;
        }

        submitBtn.disabled = true;
        showStatus('Uploading photo...', 'info');

        var title = aiTitle.value.trim();
        var alt = aiAlt.value.trim();
        var description = aiDesc.value.trim();
        var dateStr = publishDate.dateStr;
        var slug = slugify(title) || slugify(getFileStem(file.name)) || 'photo';

        var reader = new FileReader();
        reader.onload = function() {
            var base64 = reader.result.split(',')[1];
            var ext = file.type === 'image/png' ? 'png' : file.type === 'image/webp' ? 'webp' : 'jpg';
            var pageTitle = title || 'Photo ' + dateStr;
            var frontMatter = '---\n' +
                'title: "' + escapeYamlString(pageTitle) + '"\n' +
                'date: "' + dateStr + '"\n';
            if (alt) {
                frontMatter += 'alt: "' + escapeYamlString(alt) + '"\n';
            }
            if (description) {
                frontMatter += 'description: "' + escapeYamlString(description) + '"\n';
            }
            frontMatter += 'draft: false\n---\n';

            showStatus('Creating branch...', 'info');
            Promise.all([
                getMainSha(token),
                findAvailableUploadTarget(token, dateStr, slug)
            ])
                .then(function(results) {
                    var sha = results[0];
                    var target = results[1];
                    return createBranch(token, target.branchName, sha).then(function() {
                        return target;
                    });
                })
                .then(function(target) {
                    showStatus('Uploading photo...', 'info');
                    return commitFile(
                        token,
                        target.basePath + '/photo.' + ext,
                        base64,
                        'feat: add photo ' + target.folderName,
                        target.branchName
                    ).then(function() {
                        return target;
                    });
                })
                .then(function(target) {
                    showStatus('Saving metadata...', 'info');
                    return commitFile(
                        token,
                        target.basePath + '/index.md',
                        btoa(unescape(encodeURIComponent(frontMatter))),
                        'feat: add photo metadata ' + target.folderName,
                        target.branchName
                    ).then(function() {
                        return target;
                    });
                })
                .then(function(target) {
                    showStatus('Creating pull request...', 'info');
                    return createPR(token, 'feat: add photo ' + target.folderName, target.branchName, BRANCH);
                })
                .then(function(pr) {
                    return enableAutoMerge(token, pr.node_id).then(function() {
                        return pr;
                    });
                })
                    .then(function(pr) {
                        statusEl.innerHTML = 'Photo uploaded! <a href="' + pr.html_url + '" target="_blank" rel="noopener">View PR</a> — it will auto-merge after the build passes.';
                        statusEl.className = 'status success';
                        clearUploadForm();
                    })
                    .catch(function(err) {
                        showStatus('Upload failed: ' + err.message, 'error');
                    })
                    .finally(function() {
                        submitBtn.disabled = false;
                    });
        };
        reader.readAsDataURL(file);
    });

    publishDateInput.max = getSiteLocalDateString(new Date());
    publishDateInput.dataset.source = 'manual';

    // --- Initialize ---
    handleOAuthCallback().then(function(justLoggedIn) {
        var token = getToken();
        if (token) {
            fetchUser(token).then(function(user) {
                userInfo.textContent = 'Logged in as ' + user.login;
                userInfo.style.display = 'block';
                logoutBtn.style.display = 'inline';
                showUploadForm();
                if (justLoggedIn) {
                    showStatus('Logged in as ' + user.login, 'success');
                } else {
                    hideStatus();
                }
                checkSharedPhoto();
            }).catch(function(err) {
                clearToken();
                showLoginForm();
                showStatus(err.message || 'Session expired. Please log in again.', err.message && err.message.indexOf('Unauthorized') === 0 ? 'error' : 'info');
            });
        } else {
            showLoginForm();
        }
    });

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/upload/sw.js');
    }
})();
