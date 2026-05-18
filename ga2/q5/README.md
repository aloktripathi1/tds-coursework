# Q5 Solution: Static JSON API

## Objective
Host a static JSON API for the StaticShop product catalog on GitHub Pages.

## Steps Taken

1.  **Data Creation**:
    -   Created `products.json` containing:
        -   Metadata with email (`your-student-id`) and version (`f13b771b`).
        -   List of 18 products with specific details.
        -   Aggregations for the `home` category (count: 3, inventoryValue: 85353.16).

2.  **Repository Setup**:
    -   Initialized a new Git repository in `ga2/q5`.
    -   Added the remote: `https://github.com/aloktripathi1/q-github-pages-json-api`.

3.  **Deployment**:
    -   Committed `products.json`.
    -   Pushed to the `main` branch of the remote repository.

4.  **GitHub Pages Configuration (Manual Step)**:
    -   Go to Repository Settings -> Pages.
    -   Select Source: `Deploy from a branch`.
    -   Select Branch: `main`, Folder: `/` (root).
    -   Save.
    -   Verify the URL: `https://aloktripathi1.github.io/q-github-pages-json-api/products.json`.
