# Motivation

In real-world applications, relational tables can be much larger than an LLM’s context window. Directly prompting an LLM with the full table may be infeasible or perform poorly. Designing **pagination strategies** tailored to LLMs could enable efficient and accurate querying while respecting context limitations.

Research Questions:

* How do different pagination strategies impact accuracy, cost, and latency of LLM answers?

# Pagination strategies

“Create a table with the detailed information about the achievements of Susen Tiedtke from 1987 to 2000”. Columns year, competition, venue, position  
The key columns in the table are year, competition

1. Full table (no pagination) \-   
   * Provide the entire table to the LLM in a single chunk.  
   * Query: Select \* from t   
   * Limitation: Only feasible for small tables within the context window.  
2. Row by row  
   * Iterate through each row independently.  
   * Keys \= select distinct year, competition from t  
   * For each key (year y , competition c) \- select \* from t where year \= y and competition \= t  
   * Limitation:   
     * costly and inefficient.   
     * Loses global context.   
     * Need a separate key fetching process  
   * Method:  
     * First phase: fetch all values for the primary key  
     * Second phase: series of prompts, fetches one row per set of key values  
3. Attribute-based   
   * Key could be \- year, competition, venue or position  (or any combination of them)  
   * For year:   
     * Years \= Select distinct year from t  
     * For each year y \- select \* from t where year \= y   
   * Advantages: Preserves semantic grouping (e.g., events by year/competition).  
   * Challenges: Requires a priori key selection; some keys (like position) may not be meaningful for partitioning. Key quality strongly impacts retrieval quality.  
   * Method:  
     * Ask the LLM for which column to use as pagination criteria  
     * First discover the values for this column, get a set of pages to fetch  
     * Fetch each page separately (possibly in parallel)  
4. Classic pagination (offset):  
   * Use database-style offsets  
   * SELECT \* FROM t ORDER BY primary\_key where primary\_key\>last\_pk LIMIT k;  
     * k \= page size (number of rows per page)  
     * Last\_pk is the value of the last primary key retrieved.   
   * Advantages: Generic, works on any table.  
   * Challenges: Arbitrary row boundaries may split semantically related rows; may confuse the LLM without explicit linking across pages.  
   * Method:  
     * Prompt specifies columns, primary key columns and sorting order for the primary key columns  
     * First ask for the first k rows  
     * Iteratively ask for the next k rows starting from the last key provided last time  
5. Range based pagination  
   * range-based partitioning of rows using string or numeric ranges on a key column.  
   * E.g.: SELECT \* FROM t WHERE venue LIKE 'A%'; (then B, C, … Z)  
   * Note: can work on textual or numeric key columns. No need to fetch or know the key values in advance. Need to a-priori choose key and bucketing criteria (e.g. group years into decades (1900-1910, 1910-1920, …), or family name by first two characters, etc.  
   * Method:  
     * Ask the LLM for which column to use as pagination criteria and mapping criteria, may combine several columns  
     * Fetch the set of results for each mapping (possibly in parallel)  
6. Hybrid approaches

Use tables with \>200 cells up to 10 columns  
Experiment with page size: 5, 10, 20  
May later paginate the columns  
May refine dataset later e.g document-based, long context

