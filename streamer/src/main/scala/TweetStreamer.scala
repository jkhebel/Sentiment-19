package org.apache.spark.examples.streaming.twitter

import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types.{DoubleType, StringType, StructField, StructType}

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD

import org.apache.log4j.{Level, Logger}

import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.dstream.DStream 
import org.apache.spark.streaming.twitter.TwitterUtils

import twitter4j.Status
import twitter4j.TwitterObjectFactory

import com.typesafe.config.ConfigFactory

object TweetStreamer {
  def main(args: Array[String]) {

    val conf = ConfigFactory.load()

    val consumerKey = conf.getString("tokens.consumerKey")
    val consumerSecret = conf.getString("tokens.consumerSecret") 
    val accessToken = conf.getString("tokens.accessToken") 
    val accessTokenSecret = conf.getString("tokens.accessTokenSecret")

    System.setProperty("twitter4j.oauth.consumerKey", consumerKey)
    System.setProperty("twitter4j.oauth.consumerSecret", consumerSecret)
    System.setProperty("twitter4j.oauth.accessToken", accessToken)
    System.setProperty("twitter4j.oauth.accessTokenSecret", accessTokenSecret)

    val spark = SparkSession
      .builder
      .appName("TwitterStream")
      .master("local[*]")
      .getOrCreate();
    val ssc = new StreamingContext(spark.sparkContext, Seconds(10))

    val rootLogger = Logger.getRootLogger()
    rootLogger.setLevel(Level.ERROR)

    val filter = Array[String]("covid", "coronavirus")

    val tweets: DStream[Status] = TwitterUtils.createStream(ssc, None, filter)
    var validTweets = tweets.filter(_.getLang() == "en").filter(!_.isRetweet)

    val schema = new StructType()
      .add(StructField("id", StringType, true))
      .add(StructField("datetime", StringType, true))
      .add(StructField("user", StringType, true))
      .add(StructField("text", StringType, true))
      .add(StructField("geo", StringType, true))
      .add(StructField("location", StringType, true))

    validTweets.map(rdd => {
      spark.sparkContext.parallelize( 
        Seq(Row(
            rdd.getId(),
            rdd.getCreatedAt(),
            rdd.getUser(),
            rdd.getText(), 
            rdd.getGeoLocation(),
            rdd.getPlace()
      )))
    })

    validTweets.saveAsTextFiles("output/tweetStream")

    ssc.start()
    ssc.awaitTermination()
  }
}
