CREATE TABLE `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `user_ip` VARCHAR(45) NOT NULL,
  `filename` VARCHAR(255) DEFAULT NULL,
  `comments` INT(11) DEFAULT NULL,
  `posts` INT(11) DEFAULT NULL,
  `lots` INT(11) DEFAULT NULL,
  `popcorns` INT(11) DEFAULT NULL,
  `reg_date` DATETIME DEFAULT CURRENT_TIMESTAMP(),
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
)

CREATE TABLE `reports` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `post_id` INT(11) NOT NULL,
  `writer_id` VARCHAR(255) NOT NULL,
  `reporter_id` VARCHAR(255) NOT NULL,
  `movie_title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `reason_code` INT(11) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`),
  KEY `fk_reports_post` (`post_id`),
  CONSTRAINT `fk_reports_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`)
) 


CREATE TABLE `posts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `userid` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `content` TEXT NOT NULL,
  `rating` INT(11) NOT NULL,
  `spoiler` TINYINT(1) NOT NULL,
  `filename` VARCHAR(255) DEFAULT NULL,
  `movie_title` VARCHAR(255) DEFAULT NULL,
  `views` INT(11) DEFAULT 0,
  `recommend` INT(11) DEFAULT 0,
  `report` INT(11) DEFAULT 0,
  `comment` INT(11) DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `movie_id` INT(11) DEFAULT NULL,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_posts_user` (`userid`),
  KEY `fk_posts_movie_id` (`movie_id`),
  CONSTRAINT `fk_posts_movie_id` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  CONSTRAINT `fk_posts_user` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`)
)


CREATE TABLE `movies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `rank` INT(11) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `genres` VARCHAR(255) NOT NULL,
  `director` VARCHAR(200) NOT NULL,
  `nations` VARCHAR(200) NOT NULL,
  `rating` FLOAT DEFAULT NULL,
  `reviews` INT(11) DEFAULT NULL,
  `t_audience` BIGINT(20) NOT NULL,
  `c_audience` BIGINT(20) NOT NULL,
  `t_sales` BIGINT(20) NOT NULL,
  `c_sales` BIGINT(20) NOT NULL,
  `filename` VARCHAR(255) NOT NULL DEFAULT 'noimage.jpg',
  `release_date` DATETIME NOT NULL,
  `input_date` DATETIME DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`)
)


CREATE TABLE `lots` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `movie_id` INT(11) DEFAULT NULL,
  `movie_title` VARCHAR(255) DEFAULT NULL,
  `user_id` VARCHAR(255) DEFAULT NULL,
  `popcorns` INT(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_lots` (`movie_id`),
  KEY `FK_lots_user` (`user_id`),
  CONSTRAINT `FK_lots` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  CONSTRAINT `FK_lots_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
)

CREATE TABLE `comments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `post_id` INT(11) NOT NULL,
  `user_id` VARCHAR(255) NOT NULL,
  `user_name` VARCHAR(255) NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_commentss_user` (`user_id`),
  KEY `fk_comments_post` (`post_id`),
  CONSTRAINT `fk_comments_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`),
  CONSTRAINT `fk_commentss_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
)

SET GLOBAL time_zone = '+9:00';
SET time_zone = '+9:00';
SELECT NOW();