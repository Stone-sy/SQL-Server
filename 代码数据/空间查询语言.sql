/****** SSMS 的 SelectTopNRows 命令的脚本  ******/
/*
--1.  查询每栋建筑物的边界
--空间结果型（STEnvelope）
SELECT geometry.STEnvelope()
FROM building

--文本型（STEnvelope）
SELECT geometry.STEnvelope().STAsText()
FROM building
--空间结果型（STBoundary）
SELECT geometry.STBoundary()
FROM building

--文本型（STBoundary）
SELECT geometry.STBoundary().STAsText()
FROM building



--2.计算每条道路的长度(STLength)
SELECT geometry.STLength()
From road


--3.  为每条道路构建缓冲区（STBuffer，缓冲距离为20m）
SELECT geometry.STBuffer(20)
FROM road
SELECT geometry.STBuffer(20).STAsText()
FROM road



--4.  每条道路构建缓冲区后会影响到哪些建筑物？
SELECT b.geometry.STIntersection(r.geometry.STBuffer(20))
FROM building b,road r
WHERE b.geometry.STIntersects(r.geometry.STBuffer(20))=1

SELECT b.geometry.STIntersection(r.geometry.STBuffer(20)).STAsText()
FROM building b,road r
WHERE b.geometry.STIntersects(r.geometry.STBuffer(20))=1


--5.  查询道路穿越建筑物的部分(STIntersection)
SELECT b.geometry.STIntersection(r.geometry)
FROM building b,road r
WHERE b.geometry.STIntersects(r.geometry)=1

SELECT b.geometry.STIntersection(r.geometry).STAsText()
FROM building b,road r
WHERE b.geometry.STIntersects(r.geometry)=1
*/

--6.  找出距离“4号教学楼”最近的超市和最近的医院（STDistance）
SELECT m.name
FROM (SELECT geometry FROM building WHERE name='4号楼') b,market m
WHERE b.geometry.STCentroid().STDistance(m.geometry)<
ALL(
SELECT b.geometry.STCentroid().STDistance(m2.geometry)
FROM market m2
WHERE m.name<>m2.name
)

SELECT h.name
FROM (SELECT geometry FROM building WHERE name='4号楼') b,hospital h
WHERE b.geometry.STCentroid().STDistance(h.geometry)<
ALL(
SELECT b.geometry.STCentroid().STDistance(h2.geometry)
FROM hospital h2
WHERE h.name<>h2.name
)

