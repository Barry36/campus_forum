/*
-- Query: select t1.account_ID,t1.account_Name, t2.account_ID as follower_ID,t2.account_Name
from Account t1
INNER JOIN Account t2 ON t1.account_ID = t2.account_ID + 2
where t1.account_ID % 5 = 0
LIMIT 0, 1000

-- Date: 2020-04-10 16:44
*/
INSERT INTO `Follower` (`account_ID`,`account_Name`,`follower_ID`,`follower_Name`) VALUES (10,'JetBlueNews',8,'bawang2'),(20,'markhlyon',18,'mrshossruns'),(25,'rjp1208',23,'gwaki'),(30,'twinkletaters',28,'BritishAirNews'), (35,'Tinygami',33,'DonnyYardas'), (40,'MMKuderka',38,'kabell87'), (45,'scherzva',43,'elowthers'), (50,'Jamie_Fisher886',48,'Raven_TheGreat'), (55,'lauralscott',53,'CBSsoxfan'), (65,'MyMissus',63,'Jack_Kairys'), (75,'DaFuente',73,'momof43s'), (85,'faithfabulous',83,'christooma'), (100,'Forsyth_Factor',98,'tonyapoe'), (105,'crshipferling',103,'kat_volk')
