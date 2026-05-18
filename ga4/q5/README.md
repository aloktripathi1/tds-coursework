# Q5: OpenRefine — Supplier Spend Normalisation

## Task

Clean a noisy CSV of ERP invoices using **OpenRefine** to fix punctuation differences, remove duplicate `invoice_id`s, clean currency strings, and calculate the total Approved spend for "Helios Robotics" in the "Software" category.

---

## Requirements

* Load `q-openrefine-supplier-spend.csv`
* Trim whitespace on text columns
* Cluster `supplier_name` to merge variants into canonical names
* Remove duplicate `invoice_id`s (keep the first/cleanest one)
* Clean `amount_usd` using GREL: `value.replace(/[^0-9.]/, "")` and convert to number
* Filter: `supplier_name` = Helios Robotics, `category` = Software, `status` = Approved
* Calculate sum of `amount_usd`

---

## ELI15 Step-by-Step Solution

**ELI15** stands for "Explain Like I'm 15." Think of OpenRefine as a super-powered Excel that's built specifically for cleaning messy data. Here is exactly what you need to do, step by step:

### Part 1: Bring the Data In
1. **Download the file:** Get `q-openrefine-supplier-spend.csv` from the course portal.
2. **Start OpenRefine:** Open your terminal (or command prompt) and run `refine` to start the OpenRefine server. It should automatically open a tab in your browser at `http://127.0.0.1:3333`.
3. **Create the Project:** 
   - Click **Choose Files**, pick your CSV, and click **Next**.
   - Review the preview to make sure columns lined up correctly (it usually guesses CSVs perfectly).
   - In the top right, name your project something like "Q5 Invoices" and click **Create Project**.

### Part 2: The Cleanup Operations
1. **Trim Whitespace (getting rid of invisible spaces):**
   - Click the little downward arrow next to the `supplier_name` column header.
   - Go to **Edit cells** > **Common transforms** > **Trim leading and trailing whitespace**. 
   - *(Optional: Do this for `category` and `status` too, just to be safe!)*
2. **Cluster the Supplier Names (fixing typos):**
   - Click the arrow next to `supplier_name`.
   - Go to **Edit cells** > **Cluster and edit**.
   - A window pops up showing names that look similar (like "Helios Robotics" and "Helios Robotics, Inc.").
   - Check the **Merge?** box for any groups that are clearly the same company. Pick the best "New Cell Value" (e.g., just "Helios Robotics") and click **Merge Selected & Re-Cluster**.
   - Change the Method (e.g., to *nearest neighbor*) at the top to catch stealthier typos, merge those, then **Close**.
3. **Remove Duplicates (getting rid of resubmitted invoices):**
   - We only want one of each `invoice_id`. 
   - Click the arrow next to `invoice_id` > **Sort** > choose **text** and click OK.
   - *Crucial step:* Right now, it's just temporarily displaying sorted. Click the new **Sort** menu that appeared at the very top of the grid and click **Reorder rows permanently**.
   - Now click the arrow next to `invoice_id` > **Edit cells** > **Blank down**. This deletes the ID string for any row where the ID exactly matches the one above it.
   - Finally, click the arrow next to `invoice_id` > **Facet** > **Customized facets** > **Facet by blank**. 
   - In the facet box on the left, click `false`. This hides all those blanked-out (duplicate) rows!
4. **Clean the Money Column (turning "$1,200.50 USD" into just "1200.50"):**
   - Click the arrow next to `amount_usd` > **Edit cells** > **Transform**.
   - A box pops up asking for an expression. Type exactly this: `value.replace(/[^0-9.]/, "")`
   - This regex code translates to: "Find anything that is NOT a number (0-9) or a decimal point (.), and delete it."
   - Click **OK**.
   - The numbers are still considered "text" by OpenRefine. Click the arrow next to `amount_usd` > **Edit cells** > **Common transforms** > **To number**. They will turn green!

### Part 3: Getting the Final Answer
1. **Filter to what Leadership wants:**
   - Arrow next to `supplier_name` > **Text filter**. Type `Helios Robotics`.
   - Arrow next to `category` > **Text filter**. Type `Software`.
   - Arrow next to `status` > **Text filter**. Type `Approved`.
   - Now you should only see a few rows!
2. **Compute the Total Spend:**
   - Click the arrow next to `amount_usd` > **Facet** > **Numeric facet**.
   - In the facet box on the left, it won't sum them automatically, but because there are only a few rows left, you can either manually add the green numbers together on the screen, or export these specific rows to a CSV in the top right and sum them up in Excel to get your final answer.

