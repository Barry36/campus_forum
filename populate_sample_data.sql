USE socialNetwork;

DROP TABLE IF EXISTS `Tweets`;
CREATE TABLE `Tweets` (
  `tweet_id` bigint(20) DEFAULT NULL,
  `airline_sentiment` varchar(8) DEFAULT NULL,
  `airline_sentiment_confidence` decimal(5,4) DEFAULT NULL,
  `negativereason` varchar(27) DEFAULT NULL,
  `negativereason_confidence` varchar(6) DEFAULT NULL,
  `airline` varchar(14) DEFAULT NULL,
  `airline_sentiment_gold` varchar(8) DEFAULT NULL,
  `name` varchar(19) DEFAULT NULL,
  `negativereason_gold` varchar(39) DEFAULT NULL,
  `retweet_count` tinyint(4) DEFAULT NULL,
  `text` varchar(186) DEFAULT NULL,
  `tweet_coord` varchar(28) DEFAULT NULL,
  `tweet_created` varchar(25) DEFAULT NULL,
  `tweet_location` varchar(34) DEFAULT NULL,
  `user_timezone` varchar(27) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;