# Project 01 — Reflection

**Analyst:** Noah Bustard
**Date:** February 19, 2026

---

## Project Process & Experience

This project was a fantastic, hands-on introduction to the practical power of spatial data analysis. The process of moving from raw coordinates and threat parameters to a rich, multi-layered interactive map was both challenging and highly rewarding. The five-milestone structure provided a clear and logical progression, with each step building a new layer of understanding.

My process began with a thorough review of all provided materials, including the assignment description, the WDO Field Manual, and all micro-lessons. This initial investment was crucial for understanding the core requirements and the expected outputs. I decided to implement the entire project within a single, well-documented Jupyter Notebook to create a cohesive and reproducible narrative of the analysis.

## Challenges & Solutions

I encountered a few technical challenges during the implementation, each of which provided a valuable learning opportunity.

1.  **CRS-Aware Buffering:** The most significant challenge was correctly implementing the damage zone buffers in Milestone 5. My initial attempt to buffer directly on the `EPSG:4326` (WGS84) GeoDataFrame produced distorted, degree-based shapes rather than accurate, meter-based circles. 

    -   **Solution:** I corrected this by re-projecting the endpoint GeoDataFrame to a meter-based CRS (`EPSG:3857`, Web Mercator) before applying the `.buffer()` method. After buffering, I re-projected the data back to `EPSG:4326` for accurate visualization on the Folium map. This reinforced the critical importance of using the right CRS for the right operation.

2.  **Notebook Size Management:** After successfully executing the notebook, I discovered its size was nearly 50 MB. This was due to Folium embedding the full HTML and GeoJSON data for each of the five interactive maps directly into the notebook's output cells. Such a large file is unsuitable for version control with Git.

    -   **Solution:** I wrote a small Python script to programmatically parse the `.ipynb` JSON structure and strip out the large `text/html` data from the output cells. Since the maps were already saved as separate `.html` files in the `maps/` directory, no information was lost. The final notebook is a much more manageable 73 KB, containing all the code and text-based outputs while linking to the external maps.

3.  **Data Wrangling:** The initial `countries.geojson` file was very large (24 MB), which slowed down map rendering. I switched to the more reasonably sized `world_borders.geojson` (8.7 MB). This required updating column name references in my code (e.g., from `ADMIN` to `COUNTRY`), which was a good reminder to always inspect and understand the schema of a new dataset.

## What I Learned

-   **The Geospatial Workflow:** This project solidified my understanding of the end-to-end geospatial workflow: loading data, cleaning/transforming it, performing spatial calculations, conducting analysis (intersections, proximity, buffering), and creating compelling visualizations.
-   **The Power of GeoPandas:** GeoPandas is an incredibly powerful tool. The ability to perform complex spatial joins and operations with just a few lines of code is remarkable.
-   **CRS is King:** My experience with the buffering issue hammered home the lesson that Coordinate Reference Systems are not just metadata; they are fundamental to the accuracy and validity of any spatial analysis.
-   **Visualization as a Storytelling Tool:** A static table of numbers is informative, but an interactive map tells a story. Being able to layer trajectories, highlight affected countries, and display damage zones visually makes the threat assessment immediately intuitive and impactful.

## Future Improvements

If I were to extend this project, I would consider:

-   **3D Visualization:** Visualizing the orbital and airborne trajectories in 3D (e.g., using `pydeck` or `kepler.gl`) would provide a more accurate representation of their altitude and path.
-   **Time-Based Animation:** Animating the threat trajectories over time on the map would provide a dynamic, rather than static, view of the developing situation.
-   **More Sophisticated Proximity Analysis:** Instead of just checking the minimum distance, one could calculate the duration a threat spends within the defense perimeter.

Overall, this was an excellent project that provided a solid foundation in applied spatial data science.
