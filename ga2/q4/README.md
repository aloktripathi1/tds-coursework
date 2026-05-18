# Q4 Solution: GitHub Pages Portfolio

## Objective
Publish a portfolio page using GitHub Pages with a shielded email address.

## Steps Taken

1.  **File Creation**:
    -   Created `index.html` with the required content.
    -   Inserted the email address wrapped in the special comment tag:
        ```html
        <!--email_off-->your-student-id<!--/email_off-->
        ```

2.  **Repository Setup**:
    -   Created a `docs/` directory and moved `index.html` into it (optional, but good for cleanliness).
    -   Initialized a new Git repository in `ga2/q4`.
    -   Added the remote: `https://github.com/aloktripathi1/tds-assignment-q14`.

3.  **Deployment**:
    -   Committed the `index.html` file.
    -   Pushed the code to the `main` branch of the remote repository.

4.  **GitHub Pages Configuration (Manual Step)**:
    -   Go to Repository Settings -> Pages.
    -   Select Source: `Deploy from a branch`.
    -   Select Branch: `main`, Folder: `/docs` (if using docs folder) or `/` (root).
    -   Save.
