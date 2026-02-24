(function() {
    'use strict';

    var REPO_OWNER = 'MrMatt57';
    var REPO_NAME = 'MrMatt.io';
    var BRANCH = 'main';
    var ALLOWED_USER = 'MrMatt57';

    var statusEl = document.getElementById('status');
    var authSection = document.getElementById('auth-section');
    var loginBtn = document.getElementById('login-btn');
    var uploadForm = document.getElementById('upload-form');
    var photoInput = document.getElementById('photo-input');
    var captionInput = document.getElementById('caption-input');
    var previewEl = document.getElementById('preview');
    var previewImg = document.getElementById('preview-img');
    var submitBtn = document.getElementById('submit-btn');
    var logoutBtn = document.getElementById('logout-btn');
    var userInfo = document.getElementById('user-info');
    var aiStatus = document.getElementById('ai-status');
    var aiTitle = document.getElementById('ai-title');
    var aiAlt = document.getElementById('ai-alt');
    var aiDesc = document.getElementById('ai-description');
    var aiSection = document.getElementById('ai-section');

    // AI-generated metadata stored here
    var aiMeta = { title: '', alt: '', description: '' };

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
        var savedState = sessionStorage.getItem('oauth_state');
        sessionStorage.removeItem('oauth_state');
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

            if (meta && meta.caption) {
                captionInput.value = meta.caption;
            }

            caches.delete('shared-photos');
            window.history.replaceState({}, '', '/upload/');

            // Auto-describe shared photo
            describePhoto(blob);
        });
    }

    // --- AI photo description ---
    function describePhoto(fileOrBlob) {
        aiSection.style.display = 'block';
        aiStatus.textContent = 'Generating AI description...';
        aiStatus.style.display = 'block';
        aiTitle.textContent = '';
        aiAlt.textContent = '';
        aiDesc.textContent = '';

        var reader = new FileReader();
        reader.onload = function() {
            var base64 = reader.result.split(',')[1];
            var mediaType = fileOrBlob.type || 'image/jpeg';

            fetch('/api/describe-photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64, media_type: mediaType })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.error) throw new Error(data.error);
                aiMeta.title = data.title || '';
                aiMeta.alt = data.alt || '';
                aiMeta.description = data.description || '';
                aiStatus.style.display = 'none';
                aiTitle.textContent = aiMeta.title;
                aiAlt.textContent = aiMeta.alt;
                aiDesc.textContent = aiMeta.description;
                // Pre-fill caption if empty
                if (!captionInput.value.trim() && aiMeta.title) {
                    captionInput.value = aiMeta.title;
                }
            })
            .catch(function(err) {
                aiStatus.textContent = 'AI description unavailable: ' + err.message;
                aiMeta = { title: '', alt: '', description: '' };
            });
        };
        reader.readAsDataURL(fileOrBlob);
    }

    // --- Login button with state parameter ---
    loginBtn.addEventListener('click', function() {
        var clientId = loginBtn.dataset.clientId;
        var redirectUri = window.location.origin + '/upload/';
        var state = generateState();
        sessionStorage.setItem('oauth_state', state);
        var url = 'https://github.com/login/oauth/authorize' +
            '?client_id=' + encodeURIComponent(clientId) +
            '&redirect_uri=' + encodeURIComponent(redirectUri) +
            '&scope=public_repo' +
            '&state=' + encodeURIComponent(state);
        window.location.href = url;
    });

    // --- File input change ---
    photoInput.addEventListener('change', function() {
        var file = this.files[0];
        if (!file) return;
        window._sharedPhoto = null;
        var url = URL.createObjectURL(file);
        previewImg.src = url;
        previewEl.classList.add('visible');
        describePhoto(file);
    });

    // --- Logout ---
    logoutBtn.addEventListener('click', function() {
        clearToken();
        showLoginForm();
        hideStatus();
    });

    // --- Submit upload ---
    submitBtn.addEventListener('click', function() {
        var file = window._sharedPhoto || (photoInput.files && photoInput.files[0]);
        if (!file) {
            showStatus('Please select a photo.', 'error');
            return;
        }

        var token = getToken();
        if (!token) {
            showStatus('Please log in first.', 'error');
            return;
        }

        submitBtn.disabled = true;
        showStatus('Uploading photo...', 'info');

        var caption = captionInput.value.trim();
        var now = new Date();
        var dateStr = now.toISOString().slice(0, 10);
        var slug = caption
            ? caption.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '').slice(0, 40)
            : 'photo-' + now.getTime().toString(36);
        var folderName = dateStr + '-' + slug;
        var basePath = 'content/photography/' + folderName;

        var reader = new FileReader();
        reader.onload = function() {
            var base64 = reader.result.split(',')[1];
            var ext = file.type === 'image/png' ? 'png' : file.type === 'image/webp' ? 'webp' : 'jpg';
            var imagePath = basePath + '/photo.' + ext;

            var title = caption || aiMeta.title || 'Photo ' + dateStr;
            var frontMatter = '---\n' +
                'title: "' + title.replace(/"/g, '\\"') + '"\n' +
                'date: "' + dateStr + '"\n';
            if (aiMeta.alt) {
                frontMatter += 'alt: "' + aiMeta.alt.replace(/"/g, '\\"') + '"\n';
            }
            if (aiMeta.description) {
                frontMatter += 'description: "' + aiMeta.description.replace(/"/g, '\\"') + '"\n';
            }
            frontMatter += 'draft: false\n---\n';

            var indexPath = basePath + '/index.md';

            commitFile(token, imagePath, base64, 'feat: add photo ' + folderName)
                .then(function() {
                    return commitFile(token, indexPath, btoa(unescape(encodeURIComponent(frontMatter))), 'feat: add photo metadata ' + folderName);
                })
                .then(function() {
                    showStatus('Photo uploaded! It will appear on the site after the next deploy.', 'success');
                    photoInput.value = '';
                    captionInput.value = '';
                    previewEl.classList.remove('visible');
                    aiSection.style.display = 'none';
                    window._sharedPhoto = null;
                    aiMeta = { title: '', alt: '', description: '' };
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

    function commitFile(token, path, contentBase64, message) {
        return fetch('https://api.github.com/repos/' + REPO_OWNER + '/' + REPO_NAME + '/contents/' + path, {
            method: 'PUT',
            headers: {
                'Authorization': 'token ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                content: contentBase64,
                branch: BRANCH
            })
        }).then(function(r) {
            if (!r.ok) return r.json().then(function(d) { throw new Error(d.message); });
            return r.json();
        });
    }

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
