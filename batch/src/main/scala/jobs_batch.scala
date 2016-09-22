import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql._
import org.elasticsearch.spark._
import org.elasticsearch.spark.rdd.EsSpark

object jobs_batch {
   def main(args: Array[String]) {

      // setup the Spark Context named sc
      val conf = new SparkConf().setAppName("jobs_batch")
      conf.set("es.index.auto.create", "true")
      conf.set("es.resource", "dashboard/jobs")
      conf.set("es.nodes", "localhost:9200")
      //conf.set("es.nodes", "awsHost:9200")
      //conf.set("spark.serializer", classOf[KryoSerializer].getName)
      //conf.set("es.query", "?q=firstname:Daniel")

      //val sc = new SparkContext(conf)
      val sc = new SparkContext(conf)
      //.hadoopConfiguration.set("fs.s3a.access.key", sys.env.getOrElse("AWS_ACCESS_KEY_ID", sys.error("missing AWS_ACCESS_KEY_ID")
      //.hadoopConfiguration.set("fs.s3a.secret.key", sys.env.getOrElse("AWS_SECRET_ACCESS_KEY", sys.error("missing AWS_SECRET_ACCESS_KEY")

      val csqlContext = new SQLContext(sc)
      import csqlContext.implicits._
      
      // folder on HDFS to pull the data from
      val diceFile = "hdfs://ec2-52-89-46-245.us-west-2.compute.amazonaws.com:9000/camus/exec/history/2016-09-16*"
      val diceFileS3 = "s3a://giovanna-insight/raw_logs/secor_backup/diceFeed/"
      

      // construct RDD[Sting]
      val indeedStaticFile = sc.parallelize(
         """{"snippet": "The <b>data</b> science team is the core of 6sense <b>engineering</b>. Our <b>data</b> scientists are not optimizing software; We’re growing quickly and want to expand our <b>data</b>...", "city": "San Francisco", "state": "CA", "date": "Mon, 18 Jul 2016 05:47:44 GMT", "url": "http://www.indeed.com/viewjob?jk=231996de16f8c0a0&qd=w-2ovI1tcnsfYPwo0sLkH9zbhbnue5uotyVhKGbVyKMWZG2Qcqk4kcnEktztFnFoBz9U92JvRWUwZzl66iD44zxoxgsbBlaVUvGtwJ4oKEZSI4CmH9UzR8aTbSGPezp5qbUCPeLOQ7Dzs0cmDHOdgA&indpubnum=9693529091171604&atk=1astii41qburm805", "country": "US", "formattedLocation": "San Francisco, CA", "jobtitle": "Data Scientist", "company": "6sense", "formattedLocationFull": "San Francisco, CA"}""" :: Nil)
         //"""{"snippet": "The data science team is the core of 6sense engineering. Our data scientists are not optimizing software; We’re growing quickly and want to expand our data...", "city": "San Francisco", "state": "CA", "date": "Mon, 18 Jul 2016 05:47:44 GMT", "url": "http://www.indeed.com/viewjob?jk=231996de16f8c0a0&qd=w-2ovI1tcnsfYPwo0sLkH9zbhbnue5uotyVhKGbVyKMWZG2Qcqk4kcnEktztFnFoBz9U92JvRWUwZzl66iD44zxoxgsbBlaVUvGtwJ4oKEZSI4CmH9UzR8aTbSGPezp5qbUCPeLOQ7Dzs0cmDHOdgA&indpubnum=9693529091171604&atk=1astii41qburm805", "country": "US", "formattedLocation": "San Francisco, CA", "jobtitle": "Data Scientist", "company": "6sense", "formattedLocationFull": "San Francisco, CA"}""" :: Nil)
         //"""{"snippet": "", "city": "San Francisco", "state": "CA", "date": "Mon, 18 Jul 2016 05:47:44 GMT", "url": "http://www.indeed.com/viewjob?jk=231996de16f8c0a0&qd=w-2ovI1tcnsfYPwo0sLkH9zbhbnue5uotyVhKGbVyKMWZG2Qcqk4kcnEktztFnFoBz9U92JvRWUwZzl66iD44zxoxgsbBlaVUvGtwJ4oKEZSI4CmH9UzR8aTbSGPezp5qbUCPeLOQ7Dzs0cmDHOdgA&indpubnum=9693529091171604&atk=1astii41qburm805", "country": "US", "formattedLocation": "San Francisco, CA", "jobtitle": "Data Scientist", "company": "6sense", "formattedLocationFull": "San Francisco, CA"}""" :: Nil)

      val diceStaticFile = sc.parallelize(
         """{"date": "2016-09-09", "jobTitle": "Data and Application Engineering Manager", "company": "EPE Innovations", "location": "Dallas, TX", "detailUrl": "http://www.dice.com/job/result/90955654/637266?src=19"}""" :: 
         """{"date": "2016-09-09", "jobTitle": "Data and Application Engineering Manager", "company": "EPE Innovations", "location": "Dallas, TX", "detailUrl": "http://www.dice.com/job/result/90955654/637266?src=19"}""" ::
        Nil)

      // read the files
   /**
      val indeedSchema = (new StructType).add("snippet", StringType).add("city", StringType).add("state", StringType).add("date", StringType).add("url", StringType).add("country", StringType).add("formattedLocation", StringType).add("jobtitle", StringType).add("company", StringType).add("formattedLocationFull", StringType)
      val diceSchema = (new StructType).add("date", StringType).add("jobTitle", StringType).add("company", StringType).add("location", StringType).add("detailUrl", StringType)
      val dfIndeed = csqlContext.read.schema(indeedSchema).json(indeedStaticFile)
      val dfDice = csqlContext.read.schema(diceSchema).json(diceStaticFile)
   */

      val indeedDF = csqlContext.read.json(indeedStaticFile)
      val diceDF = csqlContext.read.json(diceStaticFile)

      //val diceS3DF = csqlContext.read.json(diceFileS3)

      indeedDF.show
      diceDF.show
      indeedDF.printSchema()
      diceDF.printSchema()

      indeedDF.registerTempTable("indeedTBL")
      diceDF.registerTempTable("diceTBL")

      val newIndeedDF = csqlContext.sql("SELECT jobtitle, company, url, formattedLocation as location, date, snippet FROM indeedTBL")
      val newDiceDF = csqlContext.sql("SELECT jobTitle as jobtitle, company, detailUrl as url, location, date , detailUrl as snippet FROM diceTBL")
      newIndeedDF.registerTempTable("newIndeedTBL")
      newDiceDF.registerTempTable("newDiceTBL")

      // Join both DF contents
      //val combinedDF = csqlContext.sql("SELECT jobtitle, company, url, location, date, snippet INTO newDiceTBL FROM newIndeedTBL")
      val combinedDF = csqlContext.sql("SELECT jobtitle, company, url, location, date, snippet FROM newDiceTBL UNION ALL SELECT jobtitle, company, url, location, date, snippet FROM newIndeedTBL")
      combinedDF.registerTempTable("combinedTBL")

      // Dedup rows
      val combinedDedupDF = csqlContext.sql("SELECT jobtitle, company, first(url), location, first(date), first(snippet) FROM combinedTBL GROUP BY jobtitle, company, location")   
      combinedDedupDF.show

      combinedDedupDF.rdd.saveToEs("dashboard/jobs")
      //sc.makeRDD(combinedDedupDF).saveToEs("dashboard/jobs")
      val finalRDD = combinedDedupDF.rdd
      EsSpark.saveToEs(finalRDD, "dashboard/jobs")

      combinedDedupDF.show

      // Send Data to Elasticsearch	
      //combinedDedupDF.foreachRDD { rdd => {
	// rdd.saveToEs("dashboard/jobs")
	// }
      //}

      //EsSpark.saveJsonToEs(combinedDedupDF.rdd, "jobs/myApp")
      
      //val cRDD: org.apache.spark.rdd.RDD[org.apache.spark.sql.Row] = combinedDedupDF.rdd
      //cRDD.saveToEs("job")
      //val es_df = csqlContext.read.format("org.elasticsearch.spark.sql").load("jobs")
      //es_df.show
     
   }
}   
