import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql._

object jobs_batch {
 def main(args: Array[String]) {

   // setup the Spark Context named sc
   val conf = new SparkConf().setAppName("jobs_batch")
   val sc = new SparkContext(conf)
   val sqlcontext = SQLContext(sc)

   // folder on HDFS to pull the data from
   val filename = "hdfs://ec2-52-89-46-245.us-west-2.compute.amazonaws.com:9000/camus/exec/history/2016-09-16*"
   #val df = sc.textFile(filename)
   val df = sqlcontext.read.json(filename)
   #df.show(10)
   df.printSchema()

 }
}
