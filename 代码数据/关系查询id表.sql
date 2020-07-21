SELECT * INTO [WHU].[dbo].hospital_dis_id FROM
(SELECT b.id building,h.id hospital,b.geometry.STCentroid().STDistance(h.geometry) distance
FROM [WHU].[dbo].building b,[WHU].[dbo].hospital h
)s

SELECT * INTO [WHU].[dbo].market_dis_id FROM
(SELECT b.id building,m.id market,b.geometry.STCentroid().STDistance(m.geometry) distance
FROM [WHU].[dbo].building b,[WHU].[dbo].market m
)s2

SELECT * INTO [WHU].[dbo].road_cross_id FROM
(SELECT b.id building,r.id road,b.geometry.STIntersection(r.geometry) intersection
FROM [WHU].[dbo].building b,[WHU].[dbo].road r
)s3