-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema register_login
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema register_login
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `register_login` DEFAULT CHARACTER SET utf8 ;
USE `register_login` ;

-- -----------------------------------------------------
-- Table `register_login`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `register_login`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(150) NULL DEFAULT NULL,
  `last_name` VARCHAR(150) NULL DEFAULT NULL,
  `email` VARCHAR(150) NULL DEFAULT NULL,
  `password` VARCHAR(240) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `register_login`.`quotes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `register_login`.`quotes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `author` VARCHAR(55) NULL DEFAULT NULL,
  `quote` VARCHAR(255) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `quotes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `register_login`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `register_login`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `register_login`.`likes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NULL DEFAULT NULL,
  `wish_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `wish_id` (`wish_id` ASC) VISIBLE,
  CONSTRAINT `likes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `register_login`.`users` (`id`),
  CONSTRAINT `likes_ibfk_2`
    FOREIGN KEY (`wish_id`)
    REFERENCES `register_login`.`quotes` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 20
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
