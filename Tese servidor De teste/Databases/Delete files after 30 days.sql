CREATE DEFINER = CURRENT_USER TRIGGER `mydb`.`Principle Files_AFTER_UPDATE` AFTER UPDATE ON `Principle Files` FOR EACH ROW
BEGIN
DELETE FROM `Priciple Files` WHERE `Created` < GETDATE() - 30;
END