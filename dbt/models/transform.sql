SELECT account_id,ad_id, r.name region,a.name area, ward_name,list_time,length,width,size,living_size,price,rooms,toilets,floors,c.name category
FROM cho_tot_db.public.all_posts p
JOIN cho_tot_db.public.area a
ON p.area_v2 = a.id
JOIN cho_tot_db.public.region r
ON p.region_v2 = r.id
JOIN cho_tot_db.public.category c
ON p.category = c.id
