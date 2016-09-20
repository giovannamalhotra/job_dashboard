name := "jobs_batch"

version := "1.0"

scalaVersion := "2.10.5"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "1.6.1" % "provided",
"org.apache.spark" %% "spark-sql" % "1.6.1",
"com.databricks" %% "spark-csv" % "1.5.0"
)
libraryDependencies += "org.elasticsearch" % "elasticsearch-spark_2.10" % "2.3.2"

//libraryDependencies += "org.elasticsearch" % "elasticsearch-hadoop" % "2.2.0" % "compile"
//resolvers ++= Seq("clojars" at "https://clojars.org/repo",
//                  "conjars" at "http://conjars.org/repo",
//                  "plugins" at "http://repo.spring.io/plugins-release",
//                  "sonatype" at "http://oss.sonatype.org/content/groups/public/")


assemblyMergeStrategy in assembly := {
case PathList("META-INF", xs @ _*) => MergeStrategy.discard
case x => MergeStrategy.first
}
