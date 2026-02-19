# Setup — Phase 1: Initialize Modern Hugo Site

Execute the full Phase 1 setup for the MrMatt.io rebuild. Work through each step sequentially, committing progress along the way.

## Steps

### 1. Tag the current state
- Tag current HEAD as `v1-archive` so the old site is preserved

### 2. Remove legacy build toolchain files
Delete all of these:
- `gulp/` directory
- `src/` directory
- `gulpfile.js`
- `package.json`
- `deploy.sh`
- `.travis.yml`
- `.codeclimate.yml`
- `.csslintrc`
- `.eslintrc`
- `.eslintignore`
- `.pa11yci`
- `staticman.yml`
- `public-pgp.asc`
- Old `README.md` (will be recreated in polish phase)

Commit: `chore: remove legacy build toolchain and config files`

### 3. Initialize fresh Hugo site
- Run `hugo new site . --force` in the repo root to scaffold Hugo structure
- This should create `archetypes/`, `hugo.toml`, etc. without clobbering existing content

Commit: `feat: initialize fresh Hugo site structure`

### 4. Add PaperMod theme as git submodule
- Run: `git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod`

Commit: `feat: add PaperMod theme as git submodule`

### 5. Configure hugo.toml
Create the site configuration with these settings:
- baseURL: https://mrmatt.io/
- title: Matt Walker
- theme: PaperMod
- defaultTheme: auto (system-following with toggle)
- ShowReadingTime, ShowPostNavLinks, ShowCodeCopyButtons: true
- ShowShareButtons, comments: false
- Home info with bio: "Software engineer in the Baltimore/DC Metro area..."
- Social icons: GitHub (MrMatt57), LinkedIn (mrmatt)
- Menu: Journal (/posts/), Now (/now/), Gear (/gear/), About (/about/)
- Outputs: HTML, RSS, JSON (for PaperMod search)
- Taxonomies: tags, categories
- Markup highlight style: monokai

See the hugo.toml baseline in CLAUDE.md / the project spec for exact values.

Commit: `feat: configure hugo.toml for PaperMod theme`

### 6. Verify Hugo builds and serves
- Run `hugo` to verify a clean build with no errors
- Report the result — do NOT start `hugo server` (it blocks)

### 7. Final status
- Run `git log --oneline -10` to show the commits made
- Report what was done and what the next phase is (`/feature content-migration`)
