scalaVersion := "2.12.8"

// ============================================================================

// Note, it's not required for you to define these three settings. These are
// mostly only necessary if you intend to publish your library's binaries on a
// place like Sonatype or Bintray.

libraryDependencies += "org.apache.spark" % "spark-sql_2.12" % "2.4.0"
libraryDependencies += "org.apache.spark" % "spark-streaming_2.12" % "2.4.0" 
libraryDependencies += "org.apache.bahir" %% "spark-streaming-twitter" % "2.4.0"
libraryDependencies += "com.typesafe" % "config" % "1.4.0"
