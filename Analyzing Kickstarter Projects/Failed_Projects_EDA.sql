SELECT * FROM ks_data

SELECT main_category, goal, backers, pledged, state
FROM ks_data
LIMIT 10;

SELECT main_category, goal, backers, pledged, state
FROM ks_data
WHERE state IN ('failed','canceled','suspended')
LIMIT 10;

SELECT main_category, goal, backers, pledged, state
FROM ks_data
WHERE state IN ('failed', 'canceled', 'suspended')
  AND backers >= 100
  AND pledged >= 20000
LIMIT 10;

SELECT main_category, 
	   goal, 
	   backers, 
	   pledged,
	   ROUND((pledged::numeric / goal::numeric) * 100, 2) AS pct_pledged, 
	   state
FROM ks_data
WHERE state IN ('failed', 'canceled', 'suspended')
  AND backers >= 100
  AND pledged >= 20000
ORDER BY main_category ASC, pct_pledged DESC
LIMIT 10;

SELECT main_category, 
	   goal, 
	   backers, 
	   pledged,
	   ROUND((pledged::numeric / goal::numeric) * 100, 2) AS pct_pledged, 
	   state
FROM ks_data
WHERE state ='failed'
  AND backers >= 100
  AND pledged >= 20000
ORDER BY main_category ASC, pct_pledged DESC
LIMIT 10;

SELECT main_category, goal, backers, pledged,
	   ROUND((pledged::numeric/ goal::numeric), 2) AS pct_pledged,
	   CASE
			WHEN (pledged::numeric / goal::numeric) >=1 THEN 'Fully Funded'
			WHEN (pledged::numeric / goal::numeric) >=.75 THEN 'Nearly Funded'
			ELSE 'Not Nearly Funded'
	   END AS funding_status,
	   state
FROM ks_data
WHERE state = 'failed'
	AND backers >= 100
	AND Pledged >= 20000
ORDER BY main_category ASC, pct_pledged DESC
LIMIT 10;

-- Why are these projects failing? Initial observations indicate for the top 10 failed projects,
-- 50% are Nearly funded and 50% are Not Nearly Funded. In the upper 50%, ther are enough backers and they are all close
-- to achieving the goal. A potential hypothesis as to why, could be related to the category type as it is the most common attribute
-- across all funding statuses. More accurately, failure wasn’t necessarily due to a lack of interest but possibly due to 
-- setting overly ambitious funding goals.

