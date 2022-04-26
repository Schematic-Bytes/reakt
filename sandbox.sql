-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 25, 2022 at 04:00 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sandbox`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat`
--

CREATE TABLE IF NOT EXISTS `chat` (
  `chatid` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(50) DEFAULT NULL,
  `receiver` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `chat`
--

INSERT INTO `chat` (`chatid`, `sender`, `receiver`, `date`, `message`) VALUES
(1, 'ak@mail.com', 'bibi@mail.com', '2022-03-28', 'Haii'),
(2, 'ak@mail.com', 'kay@mail.com', '2022-03-28', 'Hello'),
(3, 'ak@mail.com', 'kay@mail.com', '2022-03-28', 'Hello'),
(4, 'ak@mail.com', 'kay@mail.com', '2022-03-28', 'haii'),
(5, 'bibi@mail.com', 'ak@mail.com', '2022-03-28', 'Hello'),
(6, 'kay@mail.com', 'ak@mail.com', '2022-03-28', 'Whats Up'),
(7, 'bibi@mail.com', 'ak@mail.com', '2022-03-29', 'Got Fund'),
(8, 'ak@mail.com', 'bibi@mail.com', '2022-03-29', 'Okay'),
(9, 'bibi@mail.com', 'ak@mail.com', '2022-04-16', 'How are you');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE IF NOT EXISTS `comments` (
  `comid` int(11) NOT NULL AUTO_INCREMENT,
  `sfid` int(11) DEFAULT NULL,
  `ideaid` int(11) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`comid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`comid`, `sfid`, `ideaid`, `comment`, `date`) VALUES
(3, 2, 1, 'Great Idea...', NULL),
(4, 2, 1, 'Great Idea...', '2022-03-24'),
(5, 2, 1, 'lkdmsajn', '2022-03-29'),
(6, 1, 7, 'Great', '2022-04-16'),
(7, 3, 7, 'Good', '2022-04-16');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE IF NOT EXISTS `feedback` (
  `feedid` int(11) NOT NULL AUTO_INCREMENT,
  `sfid` int(11) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`feedid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`feedid`, `sfid`, `feedback`, `date`) VALUES
(1, 1, 'Better Place\r\n', '2022-03-25');

-- --------------------------------------------------------

--
-- Table structure for table `idea`
--

CREATE TABLE IF NOT EXISTS `idea` (
  `ideaid` int(11) NOT NULL AUTO_INCREMENT,
  `sfid` int(11) DEFAULT NULL,
  `idea` varchar(50) DEFAULT NULL,
  `desc` varchar(5000) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`ideaid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `idea`
--

INSERT INTO `idea` (`ideaid`, `sfid`, `idea`, `desc`, `date`) VALUES
(1, 1, 'We are facing water issues in kaduthuruthi', 'Its been two day since we got water supply in kaduthuruthi. we dont even have enough water to do our daily routins.', '2022-03-24'),
(2, 2, 'Waste dumbing near govt poly kaduthuruthi', 'We are currently facing waste dumbing near the GPTC kaduthuruti. it is becoming very hard to go to college.', '2022-03-24'),
(6, 2, 'AB -ve Blood needed', 'One of the patients in govt medical college kottayam needs 2 bottle of AB-ve blood. AB-ve is concidered as one of the most rarest human blood group, kindly share this news and help us in saving patients life.','2022-03-29'),
(7, 2, 'Roads are becoming ponds', 'The main roads which connects kaduthuruthi to thalayolaparamb are in critical condition. The holes in the roads have grown big and transportation has become nearly imposible. please share this news.', '2022-04-16');

-- --------------------------------------------------------

--
-- Table structure for table `investors`
--

CREATE TABLE IF NOT EXISTS `investors` (
  `invid` int(11) NOT NULL AUTO_INCREMENT,
  `inname` varchar(50) DEFAULT NULL,
  `inaddress` varchar(100) DEFAULT NULL,
  `inphone` varchar(50) DEFAULT NULL,
  `inemail` varchar(50) DEFAULT NULL,
  `indocument` varchar(200) DEFAULT NULL,
  `pin` int(11) NOT NULL,
  PRIMARY KEY (`invid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `investors`
--

INSERT INTO `investors` (`invid`, `inname`, `inaddress`, `inphone`, `inemail`, `indocument`, `pin`) VALUES
(1, 'Akhil', 'Ak Adrs\r\nVVV', '9090909099', 'ak@mail.com', '/media/07956f40-77c4-11e9-9073-657a85982e73.jpg', 683511),
(2, 'Vis', 'Vis\r\nAdrs', '9898989898', 'vis@mail.com', '/media/1level.jpg', 683510),
(3, 'Dil', 'Dil\r\nAdrs', '8989898989', 'dil@mail.com', '/media/bg_img.jpg', 683512);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `logid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `uname` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `utype` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`logid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`logid`, `uid`, `uname`, `password`, `utype`, `status`) VALUES
(1, 1, 'ak@mail.com', '12345', 'investor', 'Active'),
(2, 2, 'vis@mail.com', '12345', 'investor', 'Active'),
(3, 3, 'dil@mail.com', '12345', 'investor', 'Active'),
(4, 1, 'kay@mail.com', '12345', 'startup', 'Active'),
(5, 0, 'admin@gmail.com', 'admin', 'admin', 'Active'),
(6, 2, 'bibi@mail.com', '12345', 'startup', 'Active'),
(7, 3, 'malu@gmail.com', 'malu', 'startup', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `startpfounder`
--

CREATE TABLE IF NOT EXISTS `startpfounder` (
  `sfid` int(11) NOT NULL AUTO_INCREMENT,
  `sfname` varchar(50) DEFAULT NULL,
  `sfemail` varchar(50) DEFAULT NULL,
  `sfphone` varchar(50) DEFAULT NULL,
  `sfaddress` varchar(100) DEFAULT NULL,
  `sfdocument` varchar(200) DEFAULT NULL,
  `pin` int(11) NOT NULL,
  PRIMARY KEY (`sfid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `startpfounder`
--

INSERT INTO `startpfounder` (`sfid`, `sfname`, `sfemail`, `sfphone`, `sfaddress`, `sfdocument`, `pin`) VALUES
(1, 'Kay', 'kay@mail.com', '9090909099', 'Kay Adrs\r\n', '/media/bg_img_4lqyqSB.jpg', 683511),
(2, 'Bibi', 'bibi@mail.com', '8080808080', 'BIBI\r\nAdrs', '/media/pexels-josh-sorenson-976866.jpg', 683511),
(3, 'Malu', 'malu@gmail.com', '7896541230', 'Aluva', '/media/contact.jpg', 683511);

-- --------------------------------------------------------

--
-- Table structure for table `tbllike`
--

CREATE TABLE IF NOT EXISTS `tbllike` (
  `likeId` int(11) NOT NULL AUTO_INCREMENT,
  `ideaid` int(11) NOT NULL,
  `sfid` int(11) NOT NULL,
  `postaction` varchar(50) NOT NULL,
  PRIMARY KEY (`likeId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `tbllike`
--

INSERT INTO `tbllike` (`likeId`, `ideaid`, `sfid`, `postaction`) VALUES
(1, 1, 2, 'like'),
(2, 7, 1, 'like'),
(3, 7, 3, 'like');
