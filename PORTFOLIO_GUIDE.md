# Portfolio Maintenance Guide

A reference for editing this portfolio and a record of how it was personalized for Likitha Tadakala. Use this when you need to update a section, add a project, or explain how the site was built.

---

## 1. What This Site Is

- Personal portfolio at the root of this repo.
- Forked from Brittany Chiang's `bchiang7/v4` template.
- Built with **Gatsby** (React static site generator), **styled-components** for styling, and Markdown files for content.
- Deployed as a static site (HTML, CSS, JS in `public/` after `gatsby build`).

Why this matters: content lives in Markdown files, layout and styles live in React components. To change words, edit Markdown. To change layout or text that lives inside a section component, edit the matching `.js` file.

---

## 2. How To Run It Locally

From the project root:

```
npm install          # first time only
npm start            # runs gatsby develop on http://localhost:8000
npm run build        # production build into public/
npm run clean        # clear Gatsby cache if something goes weird
```

Pre-commit runs `prettier` and `eslint --fix` automatically via lint-staged.

---

## 3. Where Things Live

```
v4/
├── content/
│   ├── featured/      Featured project markdown (3 cards on home page)
│   ├── jobs/          Work experience tabs (Experience section)
│   ├── projects/      Other Noteworthy Projects grid
│   └── posts/         Blog posts (not currently surfaced on home)
├── src/
│   ├── components/
│   │   └── sections/  One file per home section
│   │       ├── hero.js          The big intro
│   │       ├── about.js         About + tech list
│   │       ├── jobs.js          Pulls from content/jobs
│   │       ├── featured.js      Pulls from content/featured
│   │       ├── projects.js      Pulls from content/projects
│   │       ├── publications.js  Publications block
│   │       └── contact.js       Final "Let's Connect" section
│   ├── config.js      Email, social links, nav links, colors
│   ├── pages/         Top-level routes (index, archive, 404, etc.)
│   └── styles/        Theme, variables, mixins
├── static/            Files served as is (resume.pdf, favicon, etc.)
└── gatsby-config.js   Site metadata (title, description, siteUrl)
```

Rule of thumb:

- **Text inside a Markdown file** -> edit `content/...`
- **Text hardcoded in JSX** (hero, about intro, contact copy) -> edit `src/components/sections/<name>.js`
- **Email, social links, navigation** -> edit `src/config.js`
- **Resume PDF** -> replace `static/resume.pdf`

---

## 4. Common Edits

### Update hero greeting or name

`src/components/sections/hero.js` holds the five hero lines (greeting, name, tagline, blurb, CTA button). Change the strings in JSX.

### Update About section paragraph or skills list

`src/components/sections/about.js`. The bullet list of technologies is the `skills` array at the top of the component.

### Add or edit a job

1. Open `content/jobs/`.
2. Create or edit a file. The filename's leading number controls order (lower number = more recent / appears first).
3. Frontmatter fields: `date`, `title`, `company`, `location`, `range`, `url`. Body is Markdown bullet points.

### Add a featured project (the big 3 cards)

1. Add an image to `content/featured/<slug>/`.
2. Create `content/featured/N-<slug>.md` where N is the order number.
3. Frontmatter: `date`, `title`, `cover`, `github`, `external`, `cta`, `tech` (list).
4. Body becomes the description.

### Add an "other" project (grid below featured)

1. Create `content/projects/<slug>.md`.
2. Frontmatter: `date`, `title`, `github`, `external`, `tech`, `showInProjects: true`.
3. Body is the description.

### Change email or social links

`src/config.js`. The `email` export is the single source of truth used by the contact section and other components.

### Replace the resume

Drop a new `resume.pdf` into `static/`. The link works automatically.

---

## 5. Git Workflow Used

Branch: `main`. The site is small and personal, so changes go straight to main.

Standard sequence:

```
git status
git diff
git add <specific files>
git commit -m "Short imperative message"
git push
```

Pre-commit hook runs prettier and eslint and may modify files before the commit lands. That is expected.

---

## 6. History Of Changes Made

A record of what was customized from the upstream template. Useful when answering "how did you make it yours?"

### Phase 1: Initial personalization (commits `dbe4e23`, `8942cfa`)

- Rewrote `src/config.js` with personal email, GitHub, LinkedIn.
- Updated `gatsby-config.js` site metadata (title, description, siteUrl).
- Rewrote hero, about, and contact JSX with personal copy.
- Replaced `content/jobs/` with current roles (ART, CodesOnBytes, Ozibook, Intel).
- Replaced `content/featured/` with three featured projects: SmartClean AI, YouTube Learning Chatbot, Vision For The Blind.
- Replaced `content/projects/` with three projects: Deepfake Detection, Road Object Detection, Brain Tumor Detection.
- Added project cover images under `content/featured/<slug>/` and `content/projects/images/`.
- Replaced `static/resume.pdf` with the current resume.

### Phase 2: Contact section rewrite (commit `93c681c`)

File: `src/components/sections/contact.js`.

- Changed the big title from "Get In Touch" to "Let's Connect".
- Replaced the "not currently looking for opportunities" paragraph with active job search copy targeting ML Engineering, Data Science, and Data Analytics.
- Added a visible `mailto:` link showing the email address above the existing "Say Hello" button.
- Added a new `.email-inline` styled rule to the styled-component for that link.
- Kept the section ID (`#contact`), the "Say Hello" button, animations, and surrounding components untouched.

Also fixed in the same commit:

- `content/featured/1-smartclean.md`: filled in the empty `github:` frontmatter with `https://github.com/likithatadakala/SmartCleanAI`.
- Verified all 6 project GitHub URLs against the live repos via `gh repo view`. All exist and are public.

### Phase 3: Contact layout fix (commit `f46fba8`)

- Changed `.email-inline` from `display: inline-block` to `display: block` so the "Say Hello" button always sits on its own row below the email line, instead of risking sitting beside it on wider viewports.

### Final order of the contact section

1. Kicker: "What's Next?"
2. Title: "Let's Connect"
3. Body paragraph (active job search copy).
4. Visible email link (mailto).
5. "Say Hello" button (mailto).

---

## 7. Verifying Changes Before Pushing

For content edits:

1. `npm start` and check the section in the browser at `http://localhost:8000`.
2. Check the relevant section both desktop width and mobile width (resize the browser).

For external link changes (GitHub URLs, social, resume):

1. Click each updated link in the dev preview.
2. For project GitHub links, you can batch verify with:
   ```
   for repo in SmartCleanAI AI_Chatbot VISION DeepFakeDetection Road_Object_Detection Brain_Tumor_Detection; do
     gh repo view likithatadakala/$repo --json name,url,visibility
   done
   ```

---

## 8. Quick Answer To "How Did You Build It?"

Forked Brittany Chiang's open source Gatsby portfolio template (`bchiang7/v4`), then personalized it by:

1. Rewriting `src/config.js` with my own email, GitHub, and LinkedIn.
2. Replacing all the content Markdown files in `content/jobs`, `content/featured`, and `content/projects` with my real work, featured projects, and other projects.
3. Updating the hardcoded JSX text in the hero, about, and contact section components to reflect my background as an ML and data science engineer.
4. Rewriting the contact section to position myself as actively looking for ML Engineering, Data Science, and Data Analytics roles, with a visible email link above the call to action button.
5. Replacing the resume PDF and cover images.
6. Verifying every external link (GitHub repos, social profiles, resume) resolves correctly.

Stack: Gatsby, React, styled-components, Markdown content, deployed as a static site.
