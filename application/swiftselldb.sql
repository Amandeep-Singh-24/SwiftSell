-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`registered_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`registered_user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `registration_date` DATETIME NULL DEFAULT current_timestamp,
  `last_login` DATETIME NULL DEFAULT current_timestamp,
  `account_status` VARCHAR(45) NULL,
  `username` VARCHAR(255) NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categories` (
  `categories_id` INT NOT NULL,
  `category_name` VARCHAR(45) NULL,
  PRIMARY KEY (`categories_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`items_for_sale`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`items_for_sale` (
  `item_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `description` MEDIUMTEXT NULL,
  `price` DECIMAL(8,2) NULL,
  `live` BIT(1) NOT NULL DEFAULT 0,
  `listed_date` DATETIME NOT NULL,
  `availability` VARCHAR(45) NULL,
  `seller` INT NOT NULL,
  `category_id` INT NOT NULL,
  `photo_path` VARCHAR(4096) NOT NULL,
  `thumbnail` VARCHAR(4096) NOT NULL,
  PRIMARY KEY (`item_id`),
  INDEX `fk_items_for_sale_registered_user_idx` (`seller` ASC) VISIBLE,
  INDEX `fk_items_for_sale_categories1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_for_sale_registered_user`
    FOREIGN KEY (`seller`)
    REFERENCES `mydb`.`registered_user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_items_for_sale_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`categories` (`categories_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`message` (
  `message_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(255) NULL,
  `message_date` DATETIME NULL DEFAULT current_timestamp,
  `sender_id` INT NOT NULL,
  `item_id` INT UNSIGNED NOT NULL,
  `seller_id` INT NOT NULL,
  PRIMARY KEY (`message_id`),
  INDEX `fk_message_registered_user1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_message_items_for_sale1_idx` (`item_id` ASC) VISIBLE,
  INDEX `fk_message_items_for_sale2_idx` (`seller_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_registered_user1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `mydb`.`registered_user` (`user_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_message_items_for_sale1`
    FOREIGN KEY (`item_id`)
    REFERENCES `mydb`.`items_for_sale` (`item_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_items_for_sale2`
    FOREIGN KEY (`seller_id`)
    REFERENCES `mydb`.`items_for_sale` (`seller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
