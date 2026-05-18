# Q12: GitHub Gist Hosting

## Task

Host a file on **GitHub Gist** that showcases your work and includes your email address (`your-student-id`) in the page's HTML.

**Challenge:** GitHub Gists are served via Cloudflare, which may obfuscate email addresses. You must include the email in a way that remains visible in the HTML source or rendered output.

---

## Solution

We use `portfolio.html` which uses multiple methods to ensure the email is detectable:

1.  **Meta Tags**: `<meta name="author" content="...">`
2.  **HTML Comments**: `<!-- Contact Email: ... -->`
3.  **CSS Content**: `.contact::after { content: "..."; }`
4.  **Data Attributes**: `data-email="..."`
5.  **JavaScript**: `const studentEmail = "...";`

---

## Instructions

1.  **Open GitHub Gist**
    *   Go to [https://gist.github.com/](https://gist.github.com/)
    *   Log in to your GitHub account.

2.  **Create New Gist**
    *   **Gist Description**: `Data Science Portfolio - GA2`
    *   **Filename**: `index.html`
    *   **Content**: Copy the **entire** content of `portfolio.html` from this directory into the Gist editor.

3.  **Publish**
    *   Click **Create public gist**.

4.  **Get URL**
    *   Copy the URL from your browser address bar.
    *   Format: `https://gist.github.com/[YOUR_USERNAME]/[GIST_ID]`

## Verification

If the grading script fails to find the email due to caching, add `?v=1` to the URL.

## submission

Submit the **public Gist URL**.
