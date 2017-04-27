-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: tattood
-- ------------------------------------------------------
-- Server version	5.7.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `has_tag`
--

DROP TABLE IF EXISTS `has_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `has_tag` (
  `tattoo_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tattoo_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `has_tag`
--

LOCK TABLES `has_tag` WRITE;
/*!40000 ALTER TABLE `has_tag` DISABLE KEYS */;
INSERT INTO `has_tag` VALUES (99,13,24),(99,16,24),(99,17,24),(99,23,24),(99,26,24),(99,27,24);
/*!40000 ALTER TABLE `has_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `user_id` int(11) NOT NULL,
  `tattoo_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`tattoo_id`),
  KEY `tattoo_id` (`tattoo_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`tattoo_id`) REFERENCES `tattoo` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (24,99),(24,106);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `token` text,
  PRIMARY KEY (`id`),
  CONSTRAINT `login_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (24,'eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwNjRmMDkxODNiODA0OGY4ODFlYTZmMDMzNmJkOGE5OGVkYmFlOWQifQ.eyJhenAiOiI4NzY5OTc1NzgxNzUtM212bjQ0NDdoY3ZkcHI0bnI3dm1sMW90ajhvdHRhZDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4NzY5OTc1NzgxNzUtaGtvcXIzamhlODd2cnQzbW5mbDY2ZGIwMDNmbWV0MGouYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTA3NjgwODQwNTY1NjAzMDg1OTgiLCJlbWFpbCI6ImJxa2Q4MDR6Y0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDkzMzA1NzIwLCJleHAiOjE0OTMzMDkzMjAsIm5hbWUiOiJGdXJrYW4gVXN0YSIsInBpY3R1cmUiOiJodHRwczovL2xoNi5nb29nbGV1c2VyY29udGVudC5jb20vLWRqbkpITnVLQXFvL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUlzL2pPMmRHazRDVGRjL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiJGdXJrYW4iLCJmYW1pbHlfbmFtZSI6IlVzdGEiLCJsb2NhbGUiOiJ0ciJ9.X5_fyPZX8ITTQvf0zuoh33zxw_4u9aj-Y9swRALGVghKhoKr4Di22egvGMkxZeTqPE-EpEl7Y_RtHlsannmxr7dY0D9ZYe1NUpsYa-ZoTCy2QFAQ8UDWffy_YNxuRC0aInem6jkxgrWUA-F6BscDZGbwwFaJSVFBxWGLAsWvh3wOOvZcBEHmt-E1RKapsrDKysvtWW4_w-2-DDycVLP8bZsVpqq6ZjhvuuUZ15DZNcksgcx4Jg5IhVBVv_0zVLCc-zxxFNZvTfVzd-x91ow1SWvM3sT0mBjzffeQw4l77ci9Q_61V4Eskx9oZev_jqR9dempplKUY3CK16UGk5qIOA'),(25,'eyJhbGciOiJSUzI1NiIsImtpZCI6IjhjYmJiNTU1NTZmODcyMThiMjI4Y2NkZjkyODExNjFhNmNlMzI3MmQifQ.eyJhenAiOiI4NzY5OTc1NzgxNzUtM212bjQ0NDdoY3ZkcHI0bnI3dm1sMW90ajhvdHRhZDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4NzY5OTc1NzgxNzUtaGtvcXIzamhlODd2cnQzbW5mbDY2ZGIwMDNmbWV0MGouYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDc4Nzk3NTkzOTk5MzU0ODYyNjMiLCJlbWFpbCI6Im5hemxpLnVjYW5AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsImlhdCI6MTQ5MzA0NDgyMSwiZXhwIjoxNDkzMDQ4NDIxLCJuYW1lIjoiTmF6bMSxIMOWemdlIFXDp2FuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS8tMXRMbENoWXpMUEEvQUFBQUFBQUFBQUkvQUFBQUFBQUFDSTAvZ2NxUWN3S21IZWcvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6Ik5hemzEsSDDlnpnZSIsImZhbWlseV9uYW1lIjoiVcOnYW4iLCJsb2NhbGUiOiJ0ciJ9.eJZ28mPvr2GOhkOCiOB-rKYAUY2goyEeLWbsV0lncF7K0UuA5npQ_DkQP5j1Xyxflhukkn8jYTZhJQeoFyRxtqKGgQwubqmd6xNZxo2f7xn3YQnrlB18YdVnUtbC3ff3cUfrpcjnAfpAIp-dopnt2IPiygfJn9A10LaCqZh268wqRM2r-5iHfRVKhN53EffHba_c8LYE9wfjB3H-xzXEdqNSyaW3Fs_AbggIx5moENIxEU9QF5sLgSgsLb3kId6DAr0i2pSn3ZonSQtQ0cqP9PtbhLRghzthheC72KZMCE2cTDBbU0imWw9C0UnekJKOFUxp0jc-ZJEWhE0htLcv5w');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `desc` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (3,'['),(4,']'),(6,'4'),(7,','),(8,' '),(9,'5'),(10,'6'),(11,'45'),(12,'66'),(13,'123'),(16,'asd'),(17,'qwe'),(18,'ejderya'),(19,'pati'),(20,'java'),(21,'tiger'),(22,'flower '),(23,'zxc'),(24,'zzz'),(25,'aaa'),(26,'456'),(27,'zaa'),(28,'cat');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tattoo`
--

DROP TABLE IF EXISTS `tattoo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tattoo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `private` tinyint(1) NOT NULL DEFAULT '1',
  `uploaded` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `tattoo_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tattoo`
--

LOCK TABLES `tattoo` WRITE;
/*!40000 ALTER TABLE `tattoo` DISABLE KEYS */;
INSERT INTO `tattoo` VALUES (99,24,0,'2017-04-25 18:29:32'),(106,24,0,'2017-04-26 14:00:35');
/*!40000 ALTER TABLE `tattoo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `photo` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mail` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (24,'Eksi','bqkd804zc@gmail.com','https://lh6.googleusercontent.com/-djnJHNuKAqo/AAAAAAAAAAI/AAAAAAAAAIs/jO2dGk4CTdc/s96-c/photo.jpg'),(25,'nozge','nazli.ucan@gmail.com','https://lh3.googleusercontent.com/-1tLlChYzLPA/AAAAAAAAAAI/AAAAAAAACI0/gcqQcwKmHeg/s96-c/photo.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-27 21:53:55
