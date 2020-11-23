CREATE DATABASE  IF NOT EXISTS `smartfridge` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `smartfridge`;
-- MySQL dump 10.13  Distrib 8.0.15, for macos10.14 (x86_64)
--
-- Host: localhost    Database: smartfridge
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fridge`
--

DROP TABLE IF EXISTS `fridge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `fridge` (
  `idFridge` int(11) NOT NULL AUTO_INCREMENT,
  `temperature` int(11) DEFAULT NULL,
  PRIMARY KEY (`idFridge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fridge`
--

LOCK TABLES `fridge` WRITE;
/*!40000 ALTER TABLE `fridge` DISABLE KEYS */;
/*!40000 ALTER TABLE `fridge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fridge_has_products`
--

DROP TABLE IF EXISTS `fridge_has_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `fridge_has_products` (
  `fridge_idFridge` int(11) NOT NULL,
  `products_barcode` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expirationDate` datetime DEFAULT NULL,
  `amount` int(11) DEFAULT '1',
  PRIMARY KEY (`fridge_idFridge`,`products_barcode`),
  KEY `fk_fridge_has_products_products1_idx` (`products_barcode`),
  KEY `fk_fridge_has_products_fridge1_idx` (`fridge_idFridge`),
  CONSTRAINT `fk_fridge_has_products_fridge1` FOREIGN KEY (`fridge_idFridge`) REFERENCES `fridge` (`idFridge`),
  CONSTRAINT `fk_fridge_has_products_products1` FOREIGN KEY (`products_barcode`) REFERENCES `products` (`barcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fridge_has_products`
--

LOCK TABLES `fridge_has_products` WRITE;
/*!40000 ALTER TABLE `fridge_has_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `fridge_has_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `products` (
  `barcode` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`barcode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperatureHistory`
--

DROP TABLE IF EXISTS `temperatureHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `temperatureHistory` (
  `idtemperature` int(11) NOT NULL AUTO_INCREMENT,
  `temperature` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `idfridge` int(11) NOT NULL,
  PRIMARY KEY (`idtemperature`),
  KEY `fk_temperatureHistory_fridge1_idx` (`idfridge`),
  CONSTRAINT `fk_temperatureHistory_fridge1` FOREIGN KEY (`idfridge`) REFERENCES `fridge` (`idFridge`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperatureHistory`
--

LOCK TABLES `temperatureHistory` WRITE;
/*!40000 ALTER TABLE `temperatureHistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `temperatureHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'smartfridge'
--

--
-- Dumping routines for database 'smartfridge'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-05 14:52:40
