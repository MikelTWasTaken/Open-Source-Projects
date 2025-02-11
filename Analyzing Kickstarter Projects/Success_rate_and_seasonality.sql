SELECT * FROM ks_data;

SELECT name, main_category, deadline, launched, goal, state
FROM ks_data
WHERE goal >=10000
LIMIT 50;

SELECT 
    CASE 
        WHEN goal < 20000 THEN 'Goal < 20K'
        WHEN goal BETWEEN 20000 AND 50000 THEN 'Goal 20K-50K'
        WHEN goal BETWEEN 50000 AND 100000 THEN 'Goal 50K-100K'
        ELSE 'Goal > 100K'
    END AS goal_range,
    state,
    COUNT(*) AS project_count
FROM ks_data
WHERE goal >= 10000
GROUP BY goal_range, state
ORDER BY goal_range, state;

SELECT 
    EXTRACT(YEAR FROM launched::timestamp) AS launch_year,
    EXTRACT(MONTH FROM launched::timestamp) AS launch_month,
    COUNT(CASE WHEN state = 'successful' THEN 1 END) AS successful_projects,
    COUNT(CASE WHEN state = 'failed' THEN 1 END) AS failed_projects,
    ROUND(AVG(pledged::numeric / goal::numeric) * 100, 2) AS avg_pct_pledged
FROM ks_data
WHERE goal >= 10000
GROUP BY launch_year, launch_month
ORDER BY launch_year, launch_month;

SELECT 
    main_category,
    EXTRACT(MONTH FROM launched::timestamp) AS launch_month,
    COUNT(CASE WHEN state = 'successful' THEN 1 END) AS successful_projects,
    COUNT(CASE WHEN state = 'failed' THEN 1 END) AS failed_projects,
    ROUND(AVG(pledged::numeric / goal::numeric) * 100, 2) AS avg_pct_pledged
FROM ks_data
WHERE goal >= 10000
GROUP BY main_category, launch_month
ORDER BY main_category, launch_month;


