CREATE DATABASE  IF NOT EXISTS `ojt_project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ojt_project`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: ojt_project
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_table`
--

DROP TABLE IF EXISTS `user_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_table` (
  `id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` text NOT NULL,
  `profile` varchar(255) NOT NULL,
  `type` varchar(1) NOT NULL DEFAULT '1',
  `phone` varchar(20) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `create_user_id` int NOT NULL,
  `updated_user_id` int NOT NULL,
  `deleted_user_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_table`
--

LOCK TABLES `user_table` WRITE;
/*!40000 ALTER TABLE `user_table` DISABLE KEYS */;
INSERT INTO `user_table` VALUES (1,'admin','admin@gmail.com','$2b$12$blqtfUtfDUB5YJW0kMYCMePOZcMDjWhPo3lIhn0fb0VTwCZsouOma','de4','1','09234551','ygn','2001-09-24',3,4,5,'2011-03-02 00:00:00','2022-01-01 00:00:00','2022-02-09 00:00:00'),(2,'jame','jamen@gmail.com','$2b$12$jyRInQgSV6GzzYa4yQcfaO9MlrjUvbLhs8Rgo/gBpO/mZrZbPZ8Py','de4','0','09234551','ygn','2001-09-24',3,4,5,'2011-03-02 00:00:00','2022-01-01 00:00:00','2022-02-09 00:00:00'),(3,'john','john@gmail.com','pbkdf2:sha256:260000$v0jILKxXCfqllKzO$e39bf691a999ab8e77aff6c0c1d41e0ea91f27c496fe7051aa29cbdef321bd6d','de4','0','09234551','ygn','2001-09-24',3,4,5,'2011-03-02 00:00:00','2022-01-01 00:00:00','2022-02-09 00:00:00'),(4,'kane','kane@gmail.com','$2b$12$Pb1TYWlZtNDlOAHqVDS.5.ZYI/FIgc7BX8YHyeYC/8.g5dNwP/Lp2','de4','0','09234551','ygn','2001-09-24',3,4,5,'2011-03-02 00:00:00','2022-01-01 00:00:00','2022-02-09 00:00:00');
/*!40000 ALTER TABLE `user_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-26  9:36:29
