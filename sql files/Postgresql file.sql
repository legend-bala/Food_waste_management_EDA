select * from providers_data;

select * from receivers_data;

select * from claims_data;

select * from food_Listings_data;



select Distinct city from providers_data; (963)

select Distinct city from receivers_data; (966)

/* Query 1 */
SELECT count(provider_id) as Providers,city
FROM providers_data
group by city

SELECT count(receiver_id) as receivers,city
FROM receivers_data
group by city;

/* Query 1 */
SELECT count(provider_id) as Providers,p.city,Count(receiver_id) as Receivers,r.city
FROM providers_data as p
FULL OUTER join receivers_data as r
on p.city=r.city
group by p.city,r.city,r.receiver_id
Order by p.city;



/* Query 2 */

SELECT SUM(quantity)as total,provider_type from food_listings_data
GROUP BY provider_type
ORDER BY total DESC
LIMIT 1;


/* Query 3 */
SELECT Name, Type, Address, Contact
FROM providers_data
WHERE City = 'New Jessica';

/* Query 4 */

SELECT r.type,r.name, count(claim_id) as Total_Claims
FROM claims_data c
INNER JOIN receivers_data r
ON c.receiver_id=r.receiver_id
WHERE status='Completed'
GROUP BY r.type,r.name
ORDER BY Total_Claims DESC
LIMIT 5;

/* Query 5 */
SELECT SUM(quantity) AS Total_Quantity
FROM food_listings_data;





/* Query 6 */
SELECT Location, COUNT(*) AS Listings_Count
FROM food_listings_data
GROUP BY Location
ORDER BY Listings_Count DESC
LIMIT 1;


/* Query 7 */
SELECT Food_Type, COUNT(*) AS Count
FROM food_listings_data
GROUP BY Food_Type
ORDER BY Count DESC;

/* Query 8 */
SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Claim_Count
FROM claims_data c
JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
GROUP BY fl.Food_Name
ORDER BY Claim_Count DESC;

/* Query 9 */
SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims
FROM claims_data c
JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC
LIMIT 1;

/* Query 10 */
SELECT Status, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data), 2) AS Percentage
FROM claims_data
GROUP BY Status;

/* Query 11 */

SELECT r.Name, AVG(fl.Quantity) AS Avg_Quantity_Claimed
FROM claims_data c
JOIN receivers_data r ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
WHERE c.Status = 'Completed'
GROUP BY r.Name
ORDER BY Avg_Quantity_Claimed DESC;

/* Query 12  */
SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Claim_Count
FROM claims_data c
JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
WHERE c.Status = 'Completed'
GROUP BY fl.Meal_Type
ORDER BY Claim_Count DESC;

/* Query 13  */
SELECT p.Name, SUM(fl.Quantity) AS Total_Donated
FROM food_listings_data fl
JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;